# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "LICENSE.txt" file accompanying this file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied.
# See the License for the specific language governing permissions and limitations under the License.
import datetime
import logging
import time

import boto3
import pytest
import utils
from assertpy import assert_that
from botocore.exceptions import ClientError
from cfn_stacks_factory import CfnStack
from remote_command_executor import RemoteCommandExecutor
from retrying import retry
from time_utils import minutes, seconds
from troposphere import Ref, Template, ec2
from troposphere.fsx import FileSystem, LustreConfiguration, OpenZFSConfiguration, OntapConfiguration, \
    StorageVirtualMachine, Volume, VolumeOntapConfiguration, VolumeOpenZFSConfiguration, RootVolumeConfiguration, \
    NfsExports, ClientConfigurations

BACKUP_NOT_YET_AVAILABLE_STATES = {"CREATING", "TRANSFERRING", "PENDING"}
# Maximum number of minutes to wait past when an file system's automatic backup is scheduled to start creating.
# If after this many minutes past the scheduled time backup creation has not started, the test will fail.
MAX_MINUTES_TO_WAIT_FOR_AUTOMATIC_BACKUP_START = 5
# Maximum number of minutes to wait for a file system's backup to finish being created.
MAX_MINUTES_TO_WAIT_FOR_BACKUP_COMPLETION = 7


@pytest.mark.parametrize(
    (
        "deployment_type",
        "per_unit_storage_throughput",
        "auto_import_policy",
        "storage_type",
        "drive_cache_type",
        "storage_capacity",
        "imported_file_chunk_size",
        "data_compression_type",
    ),
    [
        ("PERSISTENT_1", 200, "NEW_CHANGED", None, None, 1200, 1024, None),
        ("SCRATCH_1", None, "NEW", None, None, 1200, 1024, "LZ4"),
        ("SCRATCH_2", None, "NEW_CHANGED_DELETED", None, None, 1200, 1024, "LZ4"),
        ("PERSISTENT_1", 40, None, "HDD", None, 1800, 512, "LZ4"),
        ("PERSISTENT_1", 12, None, "HDD", "READ", 6000, 1024, "LZ4"),
        ("PERSISTENT_2", 250, None, "SSD", None, 1200, 2048, "LZ4"),
    ],
)
@pytest.mark.usefixtures("os", "instance", "scheduler")
def test_fsx_lustre_configuration_options(
    deployment_type,
    per_unit_storage_throughput,
    auto_import_policy,
    region,
    pcluster_config_reader,
    s3_bucket_factory,
    clusters_factory,
    test_datadir,
    scheduler_commands_factory,
    storage_type,
    drive_cache_type,
    data_compression_type,
    storage_capacity,
    imported_file_chunk_size,
):
    mount_dir = "/fsx_mount_dir"
    bucket_name = None
    if deployment_type != "PERSISTENT_2":
        # Association to S3 is currently not supported with Persistent 2 because it is not supported by CloudFormation.
        # FSx is working on supporting it through CloudFormation
        bucket_name = s3_bucket_factory()
        bucket = boto3.resource("s3", region_name=region).Bucket(bucket_name)
        bucket.upload_file(str(test_datadir / "s3_test_file"), "s3_test_file")
    weekly_maintenance_start_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).strftime("%u:%H:%M")
    cluster_config = pcluster_config_reader(
        bucket_name=bucket_name,
        mount_dir=mount_dir,
        deployment_type=deployment_type,
        per_unit_storage_throughput=per_unit_storage_throughput,
        auto_import_policy=auto_import_policy,
        storage_type=storage_type,
        drive_cache_type=drive_cache_type,
        data_compression_type=data_compression_type,
        storage_capacity=storage_capacity,
        imported_file_chunk_size=imported_file_chunk_size,
        weekly_maintenance_start_time=weekly_maintenance_start_time,
    )
    cluster = clusters_factory(cluster_config)
    _test_fsx_lustre_configuration_options(
        cluster,
        region,
        scheduler_commands_factory,
        mount_dir,
        bucket_name,
        storage_type,
        auto_import_policy,
        deployment_type,
        data_compression_type,
        weekly_maintenance_start_time,
        imported_file_chunk_size,
        storage_capacity,
    )


def _test_fsx_lustre_configuration_options(
    cluster,
    region,
    scheduler_commands_factory,
    mount_dir,
    bucket_name,
    storage_type,
    auto_import_policy,
    deployment_type,
    data_compression_type,
    weekly_maintenance_start_time,
    imported_file_chunk_size,
    storage_capacity,
):
    _test_fsx_lustre(cluster, region, scheduler_commands_factory, [mount_dir], bucket_name)
    remote_command_executor = RemoteCommandExecutor(cluster)
    fsx_fs_id = get_fsx_fs_ids(cluster, region)[0]
    fsx = boto3.client("fsx", region_name=region).describe_file_systems(FileSystemIds=[fsx_fs_id])

    _test_storage_type(storage_type, fsx)
    _test_deployment_type(deployment_type, fsx)
    if bucket_name:
        _test_auto_import(auto_import_policy, remote_command_executor, mount_dir, bucket_name, region)
        _test_imported_file_chunch_size(imported_file_chunk_size, fsx)
    _test_storage_capacity(remote_command_executor, mount_dir, storage_capacity)
    _test_weekly_maintenance_start_time(weekly_maintenance_start_time, fsx)
    _test_data_compression_type(data_compression_type, fsx)


@pytest.mark.usefixtures("os", "instance", "scheduler")
def test_fsx_lustre(
    region,
    pcluster_config_reader,
    s3_bucket_factory,
    clusters_factory,
    test_datadir,
    scheduler_commands_factory,
):
    """
    Test all FSx Lustre related features.

    Grouped all tests in a single function so that cluster can be reused for all of them.
    """
    mount_dir = "/fsx_mount_dir"
    bucket_name = s3_bucket_factory()
    bucket = boto3.resource("s3", region_name=region).Bucket(bucket_name)
    bucket.upload_file(str(test_datadir / "s3_test_file"), "s3_test_file")
    cluster_config = pcluster_config_reader(
        bucket_name=bucket_name,
        mount_dir=mount_dir,
        storage_capacity=1200,
    )
    cluster = clusters_factory(cluster_config)
    _test_fsx_lustre(
        cluster,
        region,
        scheduler_commands_factory,
        [mount_dir],
        bucket_name,
    )


def _test_fsx_lustre(
    cluster,
    region,
    scheduler_commands_factory,
    mount_dirs,
    bucket_name,
):
    remote_command_executor = RemoteCommandExecutor(cluster)
    scheduler_commands = scheduler_commands_factory(remote_command_executor)
    fsx_fs_ids = get_fsx_fs_ids(cluster, region)
    logging.info("Checking the length of mount dirs is the same as the length of FSXIDs")
    assert_that(len(mount_dirs)).is_equal_to(len(fsx_fs_ids))
    for mount_dir, fsx_fs_id in zip(mount_dirs, fsx_fs_ids):
        logging.info("Checking %s on %s", fsx_fs_id, mount_dir)
        if get_file_system_type(fsx_fs_id, region) == "LUSTRE":
            assert_fsx_lustre_correctly_mounted(remote_command_executor, mount_dir, region, fsx_fs_id)
        assert_fsx_correctly_shared(scheduler_commands, remote_command_executor, mount_dir)
        if bucket_name:
            _test_import_path(remote_command_executor, mount_dir)
            _test_export_path(remote_command_executor, mount_dir, bucket_name, region)
            _test_data_repository_task(remote_command_executor, mount_dir, bucket_name, fsx_fs_id, region)


@pytest.mark.usefixtures("os", "instance", "scheduler")
def test_fsx_lustre_backup(region, pcluster_config_reader, clusters_factory, scheduler_commands_factory):
    """
    Test FSx Lustre backup feature. As part of this test, following steps are performed
    1. Create a cluster with FSx automatic backups feature enabled.
    2. Mount the file system and create a test file in it.
    3. Wait for automatic backup to be created.
    4. Create a manual FSx Lustre backup of the file system.
    5. Delete the cluster.
    6. Verify whether automatic backup is deleted. NOTE: FSx team is planning to change this
       behavior to retain automatic backups upon filesystem deletion. The test case should
       be update when this change is in place.
    7. Restore a cluster from the manual backup taken in step 4. Verify whether test file
       created in step 2 exists in the restored file system.
    8. Delete manual backup created in step 4.

    """
    mount_dir = "/fsx_mount_dir"
    daily_automatic_backup_start_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    logging.info(f"daily_automatic_backup_start_time: {daily_automatic_backup_start_time}")
    cluster_config = pcluster_config_reader(
        mount_dir=mount_dir, daily_automatic_backup_start_time=daily_automatic_backup_start_time.strftime("%H:%M")
    )

    # Create a cluster with automatic backup parameters.
    cluster = clusters_factory(cluster_config)
    remote_command_executor = RemoteCommandExecutor(cluster)
    scheduler_commands = scheduler_commands_factory(remote_command_executor)
    fsx_fs_id = get_fsx_fs_ids(cluster, region)[0]

    # Mount file system
    assert_fsx_lustre_correctly_mounted(remote_command_executor, mount_dir, region, fsx_fs_id)

    # Create a text file in the mount directory.
    create_backup_test_file(scheduler_commands, remote_command_executor, mount_dir)

    # Wait for the creation of automatic backup and assert if it is in available state.
    automatic_backup = monitor_automatic_backup_creation(fsx_fs_id, region, daily_automatic_backup_start_time)

    # Create a manual FSx Lustre backup using boto3 client.
    manual_backup = create_manual_fs_backup(fsx_fs_id, region)

    # Delete original cluster.
    cluster.delete()

    # Verify whether automatic backup is also deleted along with the cluster.
    _test_automatic_backup_deletion(automatic_backup, region)

    # Restore backup into a new cluster
    cluster_config_restore = pcluster_config_reader(
        config_file="pcluster_restore_fsx.config.yaml", mount_dir=mount_dir, fsx_backup_id=manual_backup.get("BackupId")
    )

    cluster_restore = clusters_factory(cluster_config_restore)
    remote_command_executor_restore = RemoteCommandExecutor(cluster_restore)
    fsx_fs_id_restore = get_fsx_fs_ids(cluster_restore, region)[0]

    # Mount the restored file system
    assert_fsx_lustre_correctly_mounted(remote_command_executor_restore, mount_dir, region, fsx_fs_id_restore)

    # Validate whether text file created in the original file system is present in the restored file system.
    _test_restore_from_backup(remote_command_executor_restore, mount_dir)

    # Test deletion of manual backup
    _test_delete_manual_backup(manual_backup, region)


@pytest.mark.usefixtures("instance", "scheduler")
def test_multiple_fsx(
    os,
    region,
    fsx_factory,
    svm_factory,
    fsx_openzfs_volume_factory,
    vpc_stack,
    pcluster_config_reader,
    s3_bucket_factory,
    clusters_factory,
    scheduler_commands_factory,
    test_datadir,
    request,
    run_benchmarks,
):
    """
    Test existing Fsx file system

    Check fsx_fs_id provided in config file can be mounted correctly
    """
    # Create s3 bucket and upload test_file
    # bucket_name = s3_bucket_factory()
    # bucket = boto3.resource("s3", region_name=region).Bucket(bucket_name)
    # bucket.upload_file(str(test_datadir / "s3_test_file"), "s3_test_file")
    bucket_name = "integ-tests-1topnxtihhso8pj0"
    import_path = "s3://{0}".format(bucket_name)
    export_path = "s3://{0}/export_dir".format(bucket_name)
    num_new_fsx = 1
    if request.config.getoption("benchmarks") and os == "alinux2":
        # Only create more EFS when benchmarks are specified. Limiting OS to reduce cost of too many file systems
        num_existing_fsx = 50
    else:
        num_existing_fsx = 2
    mount_dirs = ["/shared"]  # OSU benchmark relies on /shared directory
    for i in range(num_new_fsx + num_existing_fsx - 1):
        mount_dirs.append(f"/fsx_mount_dir{i}")
    existing_fsx_lustre_fs_ids = []
    # existing_fsx_lustre_fs_ids = fsx_factory(
    #     ports=[988],
    #     ip_protocols=["tcp"],
    #     num=num_existing_fsx - 2,  # The other 2 FSx are OpenZFS and Ontap
    #     file_system_type="LUSTRE",
    #     StorageCapacity=1200,
    #     LustreConfiguration=LustreConfiguration(
    #         title="lustreConfiguration",
    #         ImportPath=import_path,
    #         ExportPath=export_path,
    #         DeploymentType="PERSISTENT_1",
    #         PerUnitStorageThroughput=200,
    #     ),
    # )
    # fsx_ontap_fs_id = fsx_factory(
    #     ports=[111, 2049, 20001, 20002, 20003],
    #     ip_protocols=["tcp", "udp"],
    #     num=1,
    #     file_system_type="ONTAP",
    #     StorageCapacity=1024,
    #     OntapConfiguration=OntapConfiguration(
    #         DeploymentType="SINGLE_AZ_1",
    #         ThroughputCapacity=128
    #     )
    # )[0]
    fsx_ontap_fs_id = "fs-05c0d3ff8f4c093d9"
    #fsx_ontap_svm_id = svm_factory([fsx_ontap_fs_id])[0]
    fsx_ontap_svm_id = "svm-0beec98b4a4f5e987"
    # fsx_open_zfs_fs_id = fsx_factory(
    #     ports=[111, 2049, 20001, 20002, 20003],
    #     ip_protocols=["tcp", "udp"],
    #     num=1,
    #     file_system_type="OPENZFS",
    #     StorageCapacity=64,
    #     OpenZFSConfiguration=OpenZFSConfiguration(
    #         DeploymentType="SINGLE_AZ_1",
    #         ThroughputCapacity=64,
    #         RootVolumeConfiguration=RootVolumeConfiguration(
    #             NfsExports=[NfsExports(ClientConfigurations=[ClientConfigurations(Clients="*", Options=["rw", "crossmnt"])])]
    #         )
    #     )
    # )[0]
    fsx_open_zfs_fs_id = "fs-03289e84d0f40081f"
    # fsx_openzfs_volume_factory([fsx_open_zfs_fs_id])


    cluster_config = pcluster_config_reader(
        bucket_name=bucket_name,
        fsx_lustre_mount_dirs=mount_dirs[0:-2],
        existing_fsx_lustre_fs_ids=existing_fsx_lustre_fs_ids,
        fsx_open_zfs_fs_id=fsx_open_zfs_fs_id,
        fsx_open_zfs_mount_dir=mount_dirs[-2],
        fsx_ontap_fs_id=fsx_ontap_fs_id,
        fsx_ontap_svm_id=fsx_ontap_svm_id,
        fsx_ontap_mount_dir=mount_dirs[-1],
    )
    cluster = clusters_factory(cluster_config)

    _test_fsx_lustre(cluster, region, scheduler_commands_factory, mount_dirs, bucket_name)

    remote_command_executor = RemoteCommandExecutor(cluster)
    scheduler_commands = scheduler_commands_factory(remote_command_executor)
    run_benchmarks(remote_command_executor, scheduler_commands)


@pytest.fixture(scope="class")
def fsx_factory(vpc_stack, cfn_stacks_factory, request, region, key_name):
    """
    Define a fixture to manage the creation and destruction of fsx.

    return fsx_id
    """
    created_stacks = []

    def _fsx_factory(ports, ip_protocols, file_system_type, num=1, **kwargs):
        # FSx stack
        fsx_template = Template()
        fsx_template.set_version()
        fsx_template.set_description("Create FSx stack")

        # Create security group. If using an existing file system
        # It must be associated to a security group that allows inbound TCP/UDP traffic to specific ports
        fsx_sg = ec2.SecurityGroup(
            "FSxSecurityGroup",
            GroupDescription="SecurityGroup for testing existing FSx",
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    IpProtocol=ip_protocol,
                    FromPort=port,
                    ToPort=port,
                    CidrIp="0.0.0.0/0",
                ) for port in ports for ip_protocol in ip_protocols
            ],
            VpcId=vpc_stack.cfn_outputs["VpcId"],
        )
        fsx_template.add_resource(fsx_sg)
        file_system_resource_name = "FileSystemResource"
        max_concurrency = 15
        for i in range(num):
            depends_on_arg = {}
            if i >= max_concurrency:
                depends_on_arg = {"DependsOn": [f"{file_system_resource_name}{i - max_concurrency}"]}
            fsx_filesystem = FileSystem(
                title=f"{file_system_resource_name}{i}",
                SecurityGroupIds=[Ref(fsx_sg)],
                SubnetIds=[vpc_stack.cfn_outputs["PublicSubnetId"]],
                FileSystemType=file_system_type,
                **kwargs,
                **depends_on_arg,
            )
            fsx_template.add_resource(fsx_filesystem)
        fsx_stack = CfnStack(
            name=utils.generate_stack_name("integ-tests-fsx", request.config.getoption("stackname_suffix")),
            region=region,
            template=fsx_template.to_json(),
        )
        cfn_stacks_factory.create_stack(fsx_stack)
        created_stacks.append(fsx_stack)
        return [fsx_stack.cfn_resources[f"{file_system_resource_name}{i}"] for i in range(num)]

    yield _fsx_factory

    if not request.config.getoption("no_delete"):
        for stack in created_stacks:
            cfn_stacks_factory.delete_stack(stack.name, region)


@pytest.fixture(scope="class")
def svm_factory(vpc_stack, cfn_stacks_factory, request, region, key_name):
    """
    Define a fixture to manage the creation and destruction of storage virtual machine for FSx for Ontap.

    return svm_id
    """
    created_stacks = []

    def _svm_factory(file_system_ids):
        # SVM stack
        fsx_svm_template = Template()
        fsx_svm_template.set_version()
        fsx_svm_template.set_description("Create Storage Virtual Machine stack")


        storage_virtual_machine_resource_name = "StorageVirtualMachineFileSystemResource"
        max_concurrency = 15
        for index, file_system_id in enumerate(file_system_ids):
            depends_on_arg = {}
            if index >= max_concurrency:
                depends_on_arg = {"DependsOn": [f"{storage_virtual_machine_resource_name}{index - max_concurrency}"]}
            fsx_svm = StorageVirtualMachine(
                title=f"{storage_virtual_machine_resource_name}{index}",
                Name="fsx",
                FileSystemId=file_system_id,
                **depends_on_arg,
            )
            fsx_svm_template.add_resource(fsx_svm)
            fsx_svm_volume = Volume(
                title=f"{storage_virtual_machine_resource_name}Volume{index}",
                Name="vol1",
                VolumeType="ONTAP",
                OntapConfiguration=VolumeOntapConfiguration(
                    JunctionPath="/vol1",
                    SizeInMegabytes="10240",
                    StorageEfficiencyEnabled="true",
                    StorageVirtualMachineId=Ref(fsx_svm)
                )
            )
            fsx_svm_template.add_resource(fsx_svm_volume)
        fsx_stack = CfnStack(
            name=utils.generate_stack_name("integ-tests-fsx-svm", request.config.getoption("stackname_suffix")),
            region=region,
            template=fsx_svm_template.to_json(),
        )
        cfn_stacks_factory.create_stack(fsx_stack)
        created_stacks.append(fsx_stack)
        return [fsx_stack.cfn_resources[f"{storage_virtual_machine_resource_name}{i}"] for i in range(len(file_system_ids))]

    yield _svm_factory

    if not request.config.getoption("no_delete"):
        for stack in created_stacks:
            cfn_stacks_factory.delete_stack(stack.name, region)


@pytest.fixture(scope="class")
def fsx_openzfs_volume_factory(vpc_stack, cfn_stacks_factory, request, region, key_name):
    """
    Define a fixture to manage the creation and destruction of volumes of FSx for OpenZFS.

    return svm_id
    """
    created_stacks = []

    def _openzfs_volume_factory(file_system_ids):
        fsx_volume_template = Template()
        fsx_volume_template.set_version()
        fsx_volume_template.set_description("Create Storage Virtual Machine stack")

        root_volume=""
        volume_resource_name = "VolumeResource"
        max_concurrency = 15
        for index, file_system_id in enumerate(file_system_ids):
            depends_on_arg = {}
            if index >= max_concurrency:
                depends_on_arg = {"DependsOn": [f"{volume_resource_name}{index - max_concurrency}"]}
            fsx_svm = Volume(
                title=f"{volume_resource_name}{index}",
                Name="vol1",
                VolumeType="OPENZFS",
                OpenZFSConfiguration=VolumeOpenZFSConfiguration(
                    ParentVolumeId="fsvol-00267aebd7f96f38f"
                ),
                **depends_on_arg,
            )
            fsx_volume_template.add_resource(fsx_svm)
        fsx_stack = CfnStack(
            name=utils.generate_stack_name("integ-tests-fsx-openzfs-volume", request.config.getoption("stackname_suffix")),
            region=region,
            template=fsx_volume_template.to_json(),
        )
        cfn_stacks_factory.create_stack(fsx_stack)
        created_stacks.append(fsx_stack)
        return [fsx_stack.cfn_resources[f"{volume_resource_name}{i}"] for i in range(len(file_system_ids))]

    yield _openzfs_volume_factory

    if not request.config.getoption("no_delete"):
        for stack in created_stacks:
            cfn_stacks_factory.delete_stack(stack.name, region)


def assert_fsx_lustre_correctly_mounted(remote_command_executor, mount_dir, region, fsx_fs_id):
    logging.info("Testing fsx lustre is correctly mounted")
    result = remote_command_executor.run_remote_command("df -h -t lustre | tail -n +2 | awk '{print $1, $2, $6}'")
    mount_name = get_mount_name(fsx_fs_id, region)
    assert_that(result.stdout).matches(
        r"[0-9\.]+@tcp:/{mount_name}\s+[15]\.[1278]T\s+{mount_dir}".format(mount_name=mount_name, mount_dir=mount_dir)
    )
    # example output: "192.168.46.168@tcp:/cg7k7bmv 1.7T /fsx_mount_dir"

    result = remote_command_executor.run_remote_command("cat /etc/fstab")
    mount_options = "defaults,_netdev,flock,user_xattr,noatime,noauto,x-systemd.automount"

    assert_that(result.stdout).matches(
        r"fs-[0-9a-z]+\.fsx\.[a-z1-9\-]+\.amazonaws\.com@tcp:/{mount_name}"
        r" {mount_dir} lustre {mount_options} 0 0".format(
            mount_name=mount_name, mount_dir=mount_dir, mount_options=mount_options
        )
    )


def get_mount_name(fsx_fs_id, region):
    logging.info("Getting MountName from DescribeFilesystem API.")
    fsx = boto3.client("fsx", region_name=region)
    return (
        fsx.describe_file_systems(FileSystemIds=[fsx_fs_id])
        .get("FileSystems")[0]
        .get("LustreConfiguration")
        .get("MountName")
    )


def get_file_system_type(fsx_fs_id, region):
    logging.info("Getting file system type from DescribeFilesystem API.")
    fsx = boto3.client("fsx", region_name=region)
    return (
        fsx.describe_file_systems(FileSystemIds=[fsx_fs_id])
        .get("FileSystems")[0]
        .get("FileSystemType")
    )


def get_fsx_fs_ids(cluster, region):
    return utils.retrieve_cfn_outputs(cluster.cfn_name, region).get("FSXIds").split(",")


def _get_storage_type(fsx):
    logging.info("Getting StorageType from DescribeFilesystem API.")
    return fsx.get("FileSystems")[0].get("StorageType")


def _test_storage_type(storage_type, fsx):
    if storage_type == "HDD":
        assert_that(_get_storage_type(fsx)).is_equal_to("HDD")
    else:
        assert_that(_get_storage_type(fsx)).is_equal_to("SSD")


def _get_deployment_type(fsx):
    deployment_type = fsx.get("FileSystems")[0].get("LustreConfiguration").get("DeploymentType")
    logging.info(f"Getting DeploymentType {deployment_type} from DescribeFilesystem API.")
    return deployment_type


def _test_deployment_type(deployment_type, fsx):
    logging.info("Test fsx deployment type")
    assert_that(_get_deployment_type(fsx)).is_equal_to(deployment_type)


def _test_import_path(remote_command_executor, mount_dir):
    logging.info("Testing fsx lustre import path")
    result = remote_command_executor.run_remote_command("cat {mount_dir}/s3_test_file".format(mount_dir=mount_dir))
    assert_that(result.stdout).is_equal_to("Downloaded by FSx Lustre")


def assert_fsx_correctly_shared(scheduler_commands, remote_command_executor, mount_dir):
    logging.info("Testing fsx lustre correctly mounted on compute nodes")
    remote_command_executor.run_remote_command("touch {mount_dir}/test_file".format(mount_dir=mount_dir))
    job_command = "cat {mount_dir}/test_file && touch {mount_dir}/compute_output".format(mount_dir=mount_dir)
    result = scheduler_commands.submit_command(job_command)
    job_id = scheduler_commands.assert_job_submitted(result.stdout)
    scheduler_commands.wait_job_completed(job_id)
    scheduler_commands.assert_job_succeeded(job_id)
    remote_command_executor.run_remote_command("cat {mount_dir}/compute_output".format(mount_dir=mount_dir))


def _test_export_path(remote_command_executor, mount_dir, bucket_name, region):
    logging.info("Testing fsx lustre export path")
    remote_command_executor.run_remote_command(
        "echo 'Exported by FSx Lustre' > {mount_dir}/file_to_export".format(mount_dir=mount_dir)
    )
    remote_command_executor.run_remote_command(
        "sudo lfs hsm_archive {mount_dir}/file_to_export && sleep 5".format(mount_dir=mount_dir)
    )
    remote_command_executor.run_remote_command(
        "sudo aws s3 cp --region {region} s3://{bucket_name}/export_dir/file_to_export ./file_to_export".format(
            region=region, bucket_name=bucket_name
        )
    )
    result = remote_command_executor.run_remote_command("cat ./file_to_export")
    assert_that(result.stdout).is_equal_to("Exported by FSx Lustre")


def _test_auto_import(auto_import_policy, remote_command_executor, mount_dir, bucket_name, region):
    s3 = boto3.client("s3", region_name=region)
    new_file_body = "New File AutoImported by FSx Lustre"
    modified_file_body = "File Modification AutoImported by FSx Lustre"
    filename = "fileToAutoImport"

    # Test new file
    s3.put_object(Bucket=bucket_name, Key=filename, Body=new_file_body)
    # AutoImport has a P99.9 of 1 min for new/changed files to be imported onto the filesystem
    remote_command_executor.run_remote_command("sleep 1m")
    if auto_import_policy in ("NEW", "NEW_CHANGED", "NEW_CHANGED_DELETED"):
        result = remote_command_executor.run_remote_command(f"cat {mount_dir}/{filename}")
        assert_that(result.stdout).is_equal_to(new_file_body)
    else:
        _assert_file_does_not_exist(remote_command_executor, filename, mount_dir)

    # Test modified file
    s3.put_object(Bucket=bucket_name, Key=filename, Body=modified_file_body)
    remote_command_executor.run_remote_command("sleep 1m")
    if auto_import_policy in ("NEW", "NEW_CHANGED", "NEW_CHANGED_DELETED"):
        result = remote_command_executor.run_remote_command(f"cat {mount_dir}/{filename}")
        assert_that(result.stdout).is_equal_to(
            modified_file_body if auto_import_policy in ["NEW_CHANGED", "NEW_CHANGED_DELETED"] else new_file_body
        )
    else:
        _assert_file_does_not_exist(remote_command_executor, filename, mount_dir)

    if auto_import_policy == "NEW_CHANGED_DELETED":
        # Test deleted file
        s3.delete_object(Bucket=bucket_name, Key=filename)
        remote_command_executor.run_remote_command("sleep 1m")
        _assert_file_does_not_exist(remote_command_executor, filename, mount_dir)


def _assert_file_does_not_exist(remote_command_executor, filename, mount_dir):
    result = remote_command_executor.run_remote_command(f"ls {mount_dir}/")
    assert_that(result.stdout).does_not_contain(filename)


@retry(
    retry_on_result=lambda result: result.get("Lifecycle") in ["PENDING", "EXECUTING", "CANCELLING"],
    wait_fixed=seconds(5),
    stop_max_delay=minutes(7),
)
def poll_on_data_export(task, fsx):
    logging.info(
        "Data Export Task {task_id}: {status}".format(task_id=task.get("TaskId"), status=task.get("Lifecycle"))
    )
    return fsx.describe_data_repository_tasks(TaskIds=[task.get("TaskId")]).get("DataRepositoryTasks")[0]


def _test_data_repository_task(remote_command_executor, mount_dir, bucket_name, fsx_fs_id, region):
    logging.info("Testing fsx lustre data repository task")
    file_contents = "Exported by FSx Lustre"
    remote_command_executor.run_remote_command(
        "echo '{file_contents}' > {mount_dir}/file_to_export".format(file_contents=file_contents, mount_dir=mount_dir)
    )

    # set file permissions
    remote_command_executor.run_remote_command(
        "sudo chmod 777 {mount_dir}/file_to_export && sudo chown 6666:6666 {mount_dir}/file_to_export".format(
            mount_dir=mount_dir
        )
    )

    fsx = boto3.client("fsx", region_name=region)
    task = fsx.create_data_repository_task(
        FileSystemId=fsx_fs_id, Type="EXPORT_TO_REPOSITORY", Paths=["file_to_export"], Report={"Enabled": False}
    ).get("DataRepositoryTask")

    task = poll_on_data_export(task, fsx)

    assert_that(task.get("Lifecycle")).is_equal_to("SUCCEEDED")

    remote_command_executor.run_remote_command(
        "sudo aws s3 cp --region {region} s3://{bucket_name}/export_dir/file_to_export ./file_to_export".format(
            region=region, bucket_name=bucket_name
        )
    )
    result = remote_command_executor.run_remote_command("cat ./file_to_export")
    assert_that(result.stdout).is_equal_to(file_contents)

    # test s3 metadata
    s3 = boto3.client("s3", region_name=region)
    metadata = (
        s3.head_object(Bucket=bucket_name, Key="export_dir/file_to_export").get("ResponseMetadata").get("HTTPHeaders")
    )
    file_owner = metadata.get("x-amz-meta-file-owner")
    file_group = metadata.get("x-amz-meta-file-group")
    file_permissions = metadata.get("x-amz-meta-file-permissions")
    assert_that(file_owner).is_equal_to("6666")
    assert_that(file_group).is_equal_to("6666")
    assert_that(file_permissions).is_equal_to("0100777")


def _test_storage_capacity(remote_command_executor, mount_dir, storage_capacity):
    logging.info("Test FSx storage capacity")
    # Get the storage size of mount_dir with GB, the storage size is slightly less than storage capacity defined,
    # here we set 0.1 as the difference ratio threshold
    result = remote_command_executor.run_remote_command(
        f"df -BG | grep {mount_dir}" + "| awk '{print$2}' | tr -d -c 0-9"
    )
    assert_that((storage_capacity - int(result.stdout)) / storage_capacity).is_less_than(0.1)


def _test_imported_file_chunch_size(imported_file_chunk_size, fsx):
    logging.info("Test FSx ImportedFileChunkSize setting")
    assert_that(get_imported_chunch_size(fsx)).is_equal_to(imported_file_chunk_size)


def _test_data_compression_type(compression_type, fsx):
    logging.info("Test FSx data compression type")
    if compression_type:
        actual_compression_type = fsx.get("FileSystems")[0].get("LustreConfiguration").get("DataCompressionType")
        assert_that(actual_compression_type).is_equal_to(compression_type)


def _test_weekly_maintenance_start_time(weekly_maintenance_start_time, fsx):
    logging.info("Test FSx weekly maintenance start time setting")
    assert_that(get_weekly_maintenance_start_time(fsx)).is_equal_to(weekly_maintenance_start_time)


def get_imported_chunch_size(fsx):
    logging.info("Getting ImportedFileChunkSize from DescribeFilesystem API.")
    return (
        fsx.get("FileSystems")[0]
        .get("LustreConfiguration")
        .get("DataRepositoryConfiguration")
        .get("ImportedFileChunkSize")
    )


def get_weekly_maintenance_start_time(fsx):
    logging.info("Getting WeeklyMaintenanceStartTime from DescribeFilesystem API.")
    return fsx.get("FileSystems")[0].get("LustreConfiguration").get("WeeklyMaintenanceStartTime")


def create_backup_test_file(scheduler_commands, remote_command_executor, mount_dir):
    logging.info("Creating a backup test file in fsx lustre mount directory")
    remote_command_executor.run_remote_command(
        "echo 'FSx Lustre Backup test file' > {mount_dir}/file_to_backup".format(mount_dir=mount_dir)
    )
    job_command = "cat {mount_dir}/file_to_backup ".format(mount_dir=mount_dir)
    result = scheduler_commands.submit_command(job_command)
    job_id = scheduler_commands.assert_job_submitted(result.stdout)
    scheduler_commands.wait_job_completed(job_id)
    scheduler_commands.assert_job_succeeded(job_id)
    result = remote_command_executor.run_remote_command("cat {mount_dir}/file_to_backup".format(mount_dir=mount_dir))
    assert_that(result.stdout).is_equal_to("FSx Lustre Backup test file")


def monitor_automatic_backup_creation(fsx_fs_id, region, backup_start_time):
    logging.info("Monitoring automatic backup for FSx Lustre file system: {fs_id}".format(fs_id=fsx_fs_id))
    fsx = boto3.client("fsx", region_name=region)
    sleep_until_automatic_backup_creation_start_time(fsx_fs_id, backup_start_time)
    logging.info(
        f"Waiting up to {MAX_MINUTES_TO_WAIT_FOR_AUTOMATIC_BACKUP_START} minutes for automatic backup creation "
        "to start"
    )
    backup = poll_on_automatic_backup_creation_start(fsx_fs_id, fsx)
    backup = poll_on_backup_creation(backup, fsx)
    assert_that(backup.get("Lifecycle")).is_equal_to("AVAILABLE")
    return backup


def sleep_until_automatic_backup_creation_start_time(fsx_fs_id, backup_start_time):
    """Wait for the automatic backup of the given file system to start."""
    logging.info(f"Sleeping until time when {fsx_fs_id}'s backup creation should start at {backup_start_time}")
    remaining_time = (backup_start_time - datetime.datetime.utcnow()).total_seconds()
    if remaining_time > 0:
        time.sleep(remaining_time)


def log_backup_state(backup):
    """Log the ID and status of the given backup."""
    logging.info(
        "Backup {backup_id}: {status}".format(backup_id=backup.get("BackupId"), status=backup.get("Lifecycle"))
    )


@retry(
    retry_on_result=lambda result: result.get("Lifecycle") == "NOT_STARTED",
    wait_fixed=seconds(5),
    stop_max_delay=minutes(MAX_MINUTES_TO_WAIT_FOR_AUTOMATIC_BACKUP_START),
)
def poll_on_automatic_backup_creation_start(fsx_fs_id, fsx):
    backups = fsx.describe_backups(Filters=[{"Name": "file-system-id", "Values": [fsx_fs_id]}]).get("Backups")
    backup = backups[0] if len(backups) > 0 else {"BackupId": "NA", "Lifecycle": "NOT_STARTED"}
    log_backup_state(backup)
    return backup


def _test_automatic_backup_deletion(automatic_backup, region):
    backup_id = automatic_backup.get("BackupId")
    logging.info("Verifying whether automatic backup '{0}' was deleted".format(backup_id))
    error_message = "Backup '{backup_id}' does not exist.".format(backup_id=backup_id)
    fsx = boto3.client("fsx", region_name=region)
    with pytest.raises(ClientError, match=error_message):
        return fsx.describe_backups(BackupIds=[backup_id])


def create_manual_fs_backup(fsx_fs_id, region):
    logging.info("Create manual backup for FSx Lustre file system: {fs_id}".format(fs_id=fsx_fs_id))
    fsx = boto3.client("fsx", region_name=region)
    backup = fsx.create_backup(FileSystemId=fsx_fs_id).get("Backup")
    backup = poll_on_backup_creation(backup, fsx)
    assert_that(backup.get("Lifecycle")).is_equal_to("AVAILABLE")
    return backup


@retry(
    retry_on_result=lambda result: result.get("Lifecycle") in BACKUP_NOT_YET_AVAILABLE_STATES,
    wait_fixed=seconds(5),
    stop_max_delay=minutes(MAX_MINUTES_TO_WAIT_FOR_BACKUP_COMPLETION),
)
def poll_on_backup_creation(backup, fsx):
    log_backup_state(backup)
    return fsx.describe_backups(BackupIds=[backup.get("BackupId")]).get("Backups")[0]


def _test_restore_from_backup(remote_command_executor, mount_dir):
    logging.info("Testing fsx lustre correctly restored from backup")
    result = remote_command_executor.run_remote_command("cat {mount_dir}/file_to_backup".format(mount_dir=mount_dir))
    assert_that(result.stdout).is_equal_to("FSx Lustre Backup test file")


def _test_delete_manual_backup(backup, region):
    backup_id = backup.get("BackupId")
    logging.info("Testing deletion of manual backup {0}".format(backup_id))
    fsx = boto3.client("fsx", region_name=region)
    response = fsx.delete_backup(BackupId=backup_id)
    assert_that(response.get("Lifecycle")).is_equal_to("DELETED")

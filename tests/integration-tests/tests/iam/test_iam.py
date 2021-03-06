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
import logging
import os
from shutil import copyfile

import boto3
import configparser
import pytest
from assertpy import assert_that
from remote_command_executor import RemoteCommandExecutor
from s3_common_utils import check_s3_read_resource, check_s3_read_write_resource

from tests.common.assertions import assert_no_errors_in_logs


@pytest.mark.usefixtures("os", "instance")
def test_iam_roles(
    region,
    scheduler,
    common_pcluster_policies,
    role_factory,
    pcluster_config_reader,
    clusters_factory,
    cluster_model,
    test_datadir,
):
    is_awsbatch = scheduler == "awsbatch"
    if is_awsbatch:
        instance_policies = common_pcluster_policies["awsbatch_instance_policy"]
        lambda_policies = common_pcluster_policies["awsbatch_lambda_policy"]
    else:
        instance_policies = common_pcluster_policies["traditional_instance_policy"]
        lambda_policies = common_pcluster_policies["traditional_lambda_policy"]
    cluster_role_name = role_factory("ec2", [instance_policies])
    lambda_role_name = role_factory("lambda", [lambda_policies])

    # Copy the config file template for reuse in update.
    config_file_name = cluster_model + ".ini"
    config_file_path = os.path.join(str(test_datadir), config_file_name)
    updated_config_file_name = cluster_model + ".update.ini"
    updated_config_file_path = os.path.join(str(test_datadir), updated_config_file_name)
    copyfile(config_file_path, updated_config_file_path)

    cluster_config = pcluster_config_reader(
        config_file=config_file_name, ec2_iam_role=cluster_role_name, iam_lambda_role=lambda_role_name
    )
    cluster = clusters_factory(cluster_config)

    main_stack_name = "parallelcluster-" + cluster.name
    cfn_client = boto3.client("cloudformation", region_name=region)
    lambda_client = boto3.client("lambda", region_name=region)

    # Check all CloudFormation stacks after creation
    # If scheduler is awsbatch, there will still be IAM roles created.
    _check_lambda_role(cfn_client, lambda_client, main_stack_name, lambda_role_name, not is_awsbatch)
    _check_cluster_role(region, cfn_client, main_stack_name, cluster_role_name)

    # Test updating the roles
    updated_cluster_role_name = role_factory("ec2", [instance_policies])
    updated_lambda_role_name = role_factory("lambda", [lambda_policies])
    assert_that(updated_cluster_role_name == cluster_role_name).is_false()
    assert_that(updated_lambda_role_name == lambda_role_name).is_false()
    cluster.config_file = str(
        pcluster_config_reader(
            config_file=updated_config_file_name,
            ec2_iam_role=updated_cluster_role_name,
            iam_lambda_role=updated_lambda_role_name,
        )
    )
    cluster.update()

    # Check all CloudFormation stacks after update
    _check_lambda_role(cfn_client, lambda_client, main_stack_name, updated_lambda_role_name, not is_awsbatch)
    _check_cluster_role(region, cfn_client, main_stack_name, updated_cluster_role_name)

def _check_cluster_role(region, cfn_client, stack_name, cluster_role_name):
    instance_profile_id = cfn_client.describe_stack_resource(
        StackName=stack_name, LogicalResourceId="RootInstanceProfile"
    )["StackResourceDetail"]["PhysicalResourceId"]
    iam_client = boto3.client("iam", region_name=region)
    instance_profile_role_name = iam_client.get_instance_profile(InstanceProfileName=instance_profile_id)["InstanceProfile"]["Roles"][0]["RoleName"]
    assert_that(instance_profile_role_name).is_equal_to(cluster_role_name)
    head_node_substack_id = cfn_client.describe_stack_resource(
        StackName=stack_name, LogicalResourceId="MasterServerSubstack"
    )["StackResourceDetail"]["PhysicalResourceId"]
    head_node_substack_parameters = cfn_client.describe_stacks(StackName=head_node_substack_id)["Stacks"][0]["Parameters"]
    for param in head_node_substack_parameters:
        if param["ParameterKey"] == "IamRoleName":
            assert_that(param["ParameterValue"]).is_equal_to(cluster_role_name)
    compute_substack_id = cfn_client.describe_stack_resource(
        StackName=stack_name, LogicalResourceId="ComputeFleetSubstack"
    )["StackResourceDetail"]["PhysicalResourceId"]
    compute_substack_parameters = cfn_client.describe_stacks(StackName=compute_substack_id)["Stacks"][0]["Parameters"]
    for param in compute_substack_parameters:
        if param["ParameterKey"] == "IamRoleName":
            assert_that(param["ParameterValue"]).is_equal_to(cluster_role_name)


def _check_lambda_role(cfn_client, lambda_client, stack_name, lambda_role_name, check_no_role_is_created):
    """Test lambda role is attached to all Lambda functions in the stack and its substack."""
    resources = cfn_client.describe_stack_resources(StackName=stack_name)["StackResources"]
    for resource in resources:
        resource_type = resource["ResourceType"]
        if check_no_role_is_created:
            # If check_no_role_is_created, check that there is no role created in the stack and its substack.
            assert_that(resource_type).is_not_equal_to("AWS::IAM::Role")
        if resource_type == "AWS::CloudFormation::Stack":
            # Recursively check substacks
            _check_lambda_role(
                cfn_client, lambda_client, resource["PhysicalResourceId"], lambda_role_name, check_no_role_is_created
            )
        if resource_type == "AWS::Lambda::Function":
            # Check the role is attached to the Lambda function
            lambda_function = lambda_client.get_function(FunctionName=resource["PhysicalResourceId"])["Configuration"]
            assert_that(lambda_role_name in lambda_function["Role"]).is_true()


@pytest.mark.regions(["ap-northeast-2"])
@pytest.mark.schedulers(["slurm", "awsbatch"])
@pytest.mark.oss(["alinux2"])
@pytest.mark.usefixtures("os", "instance")
def test_iam_policies(region, scheduler, pcluster_config_reader, clusters_factory):
    """Test IAM Policies"""
    cluster_config = pcluster_config_reader(
        iam_policies="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess, arn:aws:iam::aws:policy/AWSBatchFullAccess"
    )
    cluster = clusters_factory(cluster_config)
    remote_command_executor = RemoteCommandExecutor(cluster)

    _test_s3_access(remote_command_executor, region)

    if scheduler == "awsbatch":
        _test_batch_access(remote_command_executor, region)

    assert_no_errors_in_logs(remote_command_executor, scheduler)


def _test_s3_access(remote_command_executor, region):
    logging.info("Testing S3 Access")
    result = remote_command_executor.run_remote_command(f"AWS_DEFAULT_REGION={region} aws s3 ls").stdout
    # An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied
    assert_that(result).does_not_contain("AccessDenied")


def _test_batch_access(remote_command_executor, region):
    logging.info("Testing AWS Batch Access")
    result = remote_command_executor.run_remote_command(
        f"AWS_DEFAULT_REGION={region} aws batch describe-compute-environments"
    ).stdout
    # An error occurred (AccessDeniedException) when calling the DescribeComputeEnvironments operation: ...
    assert_that(result).does_not_contain("AccessDeniedException")


@pytest.mark.regions(["eu-central-1"])
@pytest.mark.schedulers(["slurm", "awsbatch"])
@pytest.mark.oss(["alinux2"])
@pytest.mark.usefixtures("os", "instance")
def test_s3_read_write_resource(
    region, pcluster_config_reader, clusters_factory, s3_bucket_factory, test_datadir, scheduler
):
    # Create S3 bucket for testing s3_read_resource and s3_read_write_resource
    bucket_name = s3_bucket_factory()
    bucket = boto3.resource("s3", region_name=region).Bucket(bucket_name)
    logging.info("bucket is {0}".format(bucket_name))
    bucket.upload_file(str(test_datadir / "s3_test_file"), "read_only/s3_test_file")
    bucket.upload_file(str(test_datadir / "s3_test_file"), "read_and_write/s3_test_file")

    cluster_config = pcluster_config_reader(bucket=bucket_name)
    cluster = clusters_factory(cluster_config)

    config = configparser.ConfigParser()
    config.read(cluster_config)

    # Check S3 resources
    check_s3_read_resource(region, cluster, config.get("cluster default", "s3_read_resource"))
    check_s3_read_write_resource(region, cluster, config.get("cluster default", "s3_read_write_resource"))

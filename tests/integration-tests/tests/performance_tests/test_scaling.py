import logging
import time

import pytest
from remote_command_executor import RemoteCommandExecutor

from tests.common.assertions import assert_no_msg_in_logs, wait_for_num_instances_in_cluster


@pytest.mark.parametrize(
    "max_nodes",
    [2000],
)
def test_scaling(
    vpc_stack,
    instance,
    os,
    region,
    scheduler,
    pcluster_config_reader,
    clusters_factory,
    test_datadir,
    scheduler_commands_factory,
    max_nodes,
):
    cluster_config = pcluster_config_reader(max_nodes=max_nodes)
    cluster = clusters_factory(cluster_config)

    logging.info("Cluster Created")

    remote_command_executor = RemoteCommandExecutor(cluster)
    scheduler_commands = scheduler_commands_factory(remote_command_executor)
    for i in range(10):
        logging.info(f"iterationnnnnnn: {i}")
        logging.info(f"Submitting an array of {max_nodes} jobs on {max_nodes} nodes")
        job_id = scheduler_commands.submit_command_and_assert_job_accepted(
            submit_command_args={
                "command": "srun sleep 10",
                "partition": "queue-0",
                "nodes": max_nodes,
                "slots": max_nodes,
            }
        )

        logging.info(f"Waiting for job to be running: {job_id}")
        scheduler_commands.wait_job_running(job_id)
        logging.info(f"Job {job_id} is running")

        logging.info(f"Cancelling job: {job_id}")
        scheduler_commands.cancel_job(job_id)
        logging.info(f"Job {job_id} cancelled")

        cluster.stop()
        wait_for_num_instances_in_cluster(cluster.cfn_name, cluster.region, desired=0)
        time.sleep(30)
        cluster.start()
        time.sleep(60)

    logging.info("Verifying no bootstrap errors in logs")
    assert_no_msg_in_logs(
        remote_command_executor,
        log_files=["/var/log/parallelcluster/clustermgtd"],
        log_msg=["Found the following bootstrap failure nodes"],
    )

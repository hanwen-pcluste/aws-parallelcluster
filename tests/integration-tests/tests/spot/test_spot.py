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
import pytest
from assertpy import assert_that
from remote_command_executor import RemoteCommandExecutor


@pytest.mark.usefixtures("region", "os", "instance", "scheduler")
def test_spot_default(scheduler_commands_factory, pcluster_config_reader, clusters_factory):
    """Test that a cluster with spot instances can be created with default spot_price_value."""
    min_count = 1
    cluster_config = pcluster_config_reader(min_count=min_count)
    cluster = clusters_factory(cluster_config)
    remote_command_executor = RemoteCommandExecutor(cluster)
    scheduler_commands = scheduler_commands_factory(remote_command_executor)
    assert_that(scheduler_commands.compute_nodes_count()).is_equal_to(min_count)


@pytest.mark.usefixtures("region", "os", "instance", "scheduler")
def test_spot_price_capacity_optimized(scheduler_commands_factory, pcluster_config_reader, clusters_factory):
    """Test that a cluster with spot instances can be created with price-capacity-optimized allocation strategy."""
    min_count = 1
    cluster_config = pcluster_config_reader(min_count=min_count)
    cluster = clusters_factory(cluster_config)
    remote_command_executor = RemoteCommandExecutor(cluster)
    scheduler_commands = scheduler_commands_factory(remote_command_executor)
    assert_that(scheduler_commands.compute_nodes_count()).is_equal_to(min_count)

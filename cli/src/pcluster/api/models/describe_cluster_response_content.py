# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from pcluster.api.models.base_model_ import Model
from pcluster.api.models.cloud_formation_stack_status import CloudFormationStackStatus
from pcluster.api.models.cluster_configuration_structure import ClusterConfigurationStructure
from pcluster.api.models.cluster_status import ClusterStatus
from pcluster.api.models.compute_fleet_status import ComputeFleetStatus
from pcluster.api.models.ec2_instance import EC2Instance
from pcluster.api.models.failure import Failure
from pcluster.api.models.login_nodes_pool import LoginNodesPool
from pcluster.api.models.scheduler import Scheduler
from pcluster.api.models.tag import Tag
import re
from pcluster.api import util

from pcluster.api.models.cloud_formation_stack_status import CloudFormationStackStatus  # noqa: E501
from pcluster.api.models.cluster_configuration_structure import ClusterConfigurationStructure  # noqa: E501
from pcluster.api.models.cluster_status import ClusterStatus  # noqa: E501
from pcluster.api.models.compute_fleet_status import ComputeFleetStatus  # noqa: E501
from pcluster.api.models.ec2_instance import EC2Instance  # noqa: E501
from pcluster.api.models.failure import Failure  # noqa: E501
from pcluster.api.models.login_nodes_pool import LoginNodesPool  # noqa: E501
from pcluster.api.models.scheduler import Scheduler  # noqa: E501
from pcluster.api.models.tag import Tag  # noqa: E501
import re  # noqa: E501

class DescribeClusterResponseContent(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, cluster_name=None, region=None, version=None, cloud_formation_stack_status=None, cluster_status=None, scheduler=None, cloudformation_stack_arn=None, creation_time=None, last_updated_time=None, cluster_configuration=None, compute_fleet_status=None, tags=None, head_node=None, login_nodes=None, failures=None):  # noqa: E501
        """DescribeClusterResponseContent - a model defined in OpenAPI

        :param cluster_name: The cluster_name of this DescribeClusterResponseContent.  # noqa: E501
        :type cluster_name: str
        :param region: The region of this DescribeClusterResponseContent.  # noqa: E501
        :type region: str
        :param version: The version of this DescribeClusterResponseContent.  # noqa: E501
        :type version: str
        :param cloud_formation_stack_status: The cloud_formation_stack_status of this DescribeClusterResponseContent.  # noqa: E501
        :type cloud_formation_stack_status: CloudFormationStackStatus
        :param cluster_status: The cluster_status of this DescribeClusterResponseContent.  # noqa: E501
        :type cluster_status: ClusterStatus
        :param scheduler: The scheduler of this DescribeClusterResponseContent.  # noqa: E501
        :type scheduler: Scheduler
        :param cloudformation_stack_arn: The cloudformation_stack_arn of this DescribeClusterResponseContent.  # noqa: E501
        :type cloudformation_stack_arn: str
        :param creation_time: The creation_time of this DescribeClusterResponseContent.  # noqa: E501
        :type creation_time: datetime
        :param last_updated_time: The last_updated_time of this DescribeClusterResponseContent.  # noqa: E501
        :type last_updated_time: datetime
        :param cluster_configuration: The cluster_configuration of this DescribeClusterResponseContent.  # noqa: E501
        :type cluster_configuration: ClusterConfigurationStructure
        :param compute_fleet_status: The compute_fleet_status of this DescribeClusterResponseContent.  # noqa: E501
        :type compute_fleet_status: ComputeFleetStatus
        :param tags: The tags of this DescribeClusterResponseContent.  # noqa: E501
        :type tags: List[Tag]
        :param head_node: The head_node of this DescribeClusterResponseContent.  # noqa: E501
        :type head_node: EC2Instance
        :param login_nodes: The login_nodes of this DescribeClusterResponseContent.  # noqa: E501
        :type login_nodes: LoginNodesPool
        :param failures: The failures of this DescribeClusterResponseContent.  # noqa: E501
        :type failures: List[Failure]
        """
        self.openapi_types = {
            'cluster_name': str,
            'region': str,
            'version': str,
            'cloud_formation_stack_status': CloudFormationStackStatus,
            'cluster_status': ClusterStatus,
            'scheduler': Scheduler,
            'cloudformation_stack_arn': str,
            'creation_time': datetime,
            'last_updated_time': datetime,
            'cluster_configuration': ClusterConfigurationStructure,
            'compute_fleet_status': ComputeFleetStatus,
            'tags': List[Tag],
            'head_node': EC2Instance,
            'login_nodes': LoginNodesPool,
            'failures': List[Failure]
        }

        self.attribute_map = {
            'cluster_name': 'clusterName',
            'region': 'region',
            'version': 'version',
            'cloud_formation_stack_status': 'cloudFormationStackStatus',
            'cluster_status': 'clusterStatus',
            'scheduler': 'scheduler',
            'cloudformation_stack_arn': 'cloudformationStackArn',
            'creation_time': 'creationTime',
            'last_updated_time': 'lastUpdatedTime',
            'cluster_configuration': 'clusterConfiguration',
            'compute_fleet_status': 'computeFleetStatus',
            'tags': 'tags',
            'head_node': 'headNode',
            'login_nodes': 'loginNodes',
            'failures': 'failures'
        }

        self._cluster_name = cluster_name
        self._region = region
        self._version = version
        self._cloud_formation_stack_status = cloud_formation_stack_status
        self._cluster_status = cluster_status
        self._scheduler = scheduler
        self._cloudformation_stack_arn = cloudformation_stack_arn
        self._creation_time = creation_time
        self._last_updated_time = last_updated_time
        self._cluster_configuration = cluster_configuration
        self._compute_fleet_status = compute_fleet_status
        self._tags = tags
        self._head_node = head_node
        self._login_nodes = login_nodes
        self._failures = failures

    @classmethod
    def from_dict(cls, dikt) -> 'DescribeClusterResponseContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DescribeClusterResponseContent of this DescribeClusterResponseContent.  # noqa: E501
        :rtype: DescribeClusterResponseContent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def cluster_name(self):
        """Gets the cluster_name of this DescribeClusterResponseContent.

        Name of the cluster.  # noqa: E501

        :return: The cluster_name of this DescribeClusterResponseContent.
        :rtype: str
        """
        return self._cluster_name

    @cluster_name.setter
    def cluster_name(self, cluster_name):
        """Sets the cluster_name of this DescribeClusterResponseContent.

        Name of the cluster.  # noqa: E501

        :param cluster_name: The cluster_name of this DescribeClusterResponseContent.
        :type cluster_name: str
        """
        if cluster_name is None:
            raise ValueError("Invalid value for `cluster_name`, must not be `None`")  # noqa: E501
        if cluster_name is not None and not re.search(r'^[a-zA-Z][a-zA-Z0-9-]+$', cluster_name):  # noqa: E501
            raise ValueError("Invalid value for `cluster_name`, must be a follow pattern or equal to `/^[a-zA-Z][a-zA-Z0-9-]+$/`")  # noqa: E501

        self._cluster_name = cluster_name

    @property
    def region(self):
        """Gets the region of this DescribeClusterResponseContent.

        AWS region where the cluster is created.  # noqa: E501

        :return: The region of this DescribeClusterResponseContent.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this DescribeClusterResponseContent.

        AWS region where the cluster is created.  # noqa: E501

        :param region: The region of this DescribeClusterResponseContent.
        :type region: str
        """
        if region is None:
            raise ValueError("Invalid value for `region`, must not be `None`")  # noqa: E501

        self._region = region

    @property
    def version(self):
        """Gets the version of this DescribeClusterResponseContent.

        ParallelCluster version used to create the cluster.  # noqa: E501

        :return: The version of this DescribeClusterResponseContent.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DescribeClusterResponseContent.

        ParallelCluster version used to create the cluster.  # noqa: E501

        :param version: The version of this DescribeClusterResponseContent.
        :type version: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def cloud_formation_stack_status(self):
        """Gets the cloud_formation_stack_status of this DescribeClusterResponseContent.


        :return: The cloud_formation_stack_status of this DescribeClusterResponseContent.
        :rtype: CloudFormationStackStatus
        """
        return self._cloud_formation_stack_status

    @cloud_formation_stack_status.setter
    def cloud_formation_stack_status(self, cloud_formation_stack_status):
        """Sets the cloud_formation_stack_status of this DescribeClusterResponseContent.


        :param cloud_formation_stack_status: The cloud_formation_stack_status of this DescribeClusterResponseContent.
        :type cloud_formation_stack_status: CloudFormationStackStatus
        """
        if cloud_formation_stack_status is None:
            raise ValueError("Invalid value for `cloud_formation_stack_status`, must not be `None`")  # noqa: E501

        self._cloud_formation_stack_status = cloud_formation_stack_status

    @property
    def cluster_status(self):
        """Gets the cluster_status of this DescribeClusterResponseContent.


        :return: The cluster_status of this DescribeClusterResponseContent.
        :rtype: ClusterStatus
        """
        return self._cluster_status

    @cluster_status.setter
    def cluster_status(self, cluster_status):
        """Sets the cluster_status of this DescribeClusterResponseContent.


        :param cluster_status: The cluster_status of this DescribeClusterResponseContent.
        :type cluster_status: ClusterStatus
        """
        if cluster_status is None:
            raise ValueError("Invalid value for `cluster_status`, must not be `None`")  # noqa: E501

        self._cluster_status = cluster_status

    @property
    def scheduler(self):
        """Gets the scheduler of this DescribeClusterResponseContent.


        :return: The scheduler of this DescribeClusterResponseContent.
        :rtype: Scheduler
        """
        return self._scheduler

    @scheduler.setter
    def scheduler(self, scheduler):
        """Sets the scheduler of this DescribeClusterResponseContent.


        :param scheduler: The scheduler of this DescribeClusterResponseContent.
        :type scheduler: Scheduler
        """

        self._scheduler = scheduler

    @property
    def cloudformation_stack_arn(self):
        """Gets the cloudformation_stack_arn of this DescribeClusterResponseContent.

        ARN of the main CloudFormation stack.  # noqa: E501

        :return: The cloudformation_stack_arn of this DescribeClusterResponseContent.
        :rtype: str
        """
        return self._cloudformation_stack_arn

    @cloudformation_stack_arn.setter
    def cloudformation_stack_arn(self, cloudformation_stack_arn):
        """Sets the cloudformation_stack_arn of this DescribeClusterResponseContent.

        ARN of the main CloudFormation stack.  # noqa: E501

        :param cloudformation_stack_arn: The cloudformation_stack_arn of this DescribeClusterResponseContent.
        :type cloudformation_stack_arn: str
        """
        if cloudformation_stack_arn is None:
            raise ValueError("Invalid value for `cloudformation_stack_arn`, must not be `None`")  # noqa: E501

        self._cloudformation_stack_arn = cloudformation_stack_arn

    @property
    def creation_time(self):
        """Gets the creation_time of this DescribeClusterResponseContent.

        Timestamp representing the cluster creation time.  # noqa: E501

        :return: The creation_time of this DescribeClusterResponseContent.
        :rtype: datetime
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """Sets the creation_time of this DescribeClusterResponseContent.

        Timestamp representing the cluster creation time.  # noqa: E501

        :param creation_time: The creation_time of this DescribeClusterResponseContent.
        :type creation_time: datetime
        """
        if creation_time is None:
            raise ValueError("Invalid value for `creation_time`, must not be `None`")  # noqa: E501

        self._creation_time = creation_time

    @property
    def last_updated_time(self):
        """Gets the last_updated_time of this DescribeClusterResponseContent.

        Timestamp representing the last cluster update time.  # noqa: E501

        :return: The last_updated_time of this DescribeClusterResponseContent.
        :rtype: datetime
        """
        return self._last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, last_updated_time):
        """Sets the last_updated_time of this DescribeClusterResponseContent.

        Timestamp representing the last cluster update time.  # noqa: E501

        :param last_updated_time: The last_updated_time of this DescribeClusterResponseContent.
        :type last_updated_time: datetime
        """
        if last_updated_time is None:
            raise ValueError("Invalid value for `last_updated_time`, must not be `None`")  # noqa: E501

        self._last_updated_time = last_updated_time

    @property
    def cluster_configuration(self):
        """Gets the cluster_configuration of this DescribeClusterResponseContent.


        :return: The cluster_configuration of this DescribeClusterResponseContent.
        :rtype: ClusterConfigurationStructure
        """
        return self._cluster_configuration

    @cluster_configuration.setter
    def cluster_configuration(self, cluster_configuration):
        """Sets the cluster_configuration of this DescribeClusterResponseContent.


        :param cluster_configuration: The cluster_configuration of this DescribeClusterResponseContent.
        :type cluster_configuration: ClusterConfigurationStructure
        """
        if cluster_configuration is None:
            raise ValueError("Invalid value for `cluster_configuration`, must not be `None`")  # noqa: E501

        self._cluster_configuration = cluster_configuration

    @property
    def compute_fleet_status(self):
        """Gets the compute_fleet_status of this DescribeClusterResponseContent.


        :return: The compute_fleet_status of this DescribeClusterResponseContent.
        :rtype: ComputeFleetStatus
        """
        return self._compute_fleet_status

    @compute_fleet_status.setter
    def compute_fleet_status(self, compute_fleet_status):
        """Sets the compute_fleet_status of this DescribeClusterResponseContent.


        :param compute_fleet_status: The compute_fleet_status of this DescribeClusterResponseContent.
        :type compute_fleet_status: ComputeFleetStatus
        """
        if compute_fleet_status is None:
            raise ValueError("Invalid value for `compute_fleet_status`, must not be `None`")  # noqa: E501

        self._compute_fleet_status = compute_fleet_status

    @property
    def tags(self):
        """Gets the tags of this DescribeClusterResponseContent.

        Tags associated with the cluster.  # noqa: E501

        :return: The tags of this DescribeClusterResponseContent.
        :rtype: List[Tag]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this DescribeClusterResponseContent.

        Tags associated with the cluster.  # noqa: E501

        :param tags: The tags of this DescribeClusterResponseContent.
        :type tags: List[Tag]
        """
        if tags is None:
            raise ValueError("Invalid value for `tags`, must not be `None`")  # noqa: E501

        self._tags = tags

    @property
    def head_node(self):
        """Gets the head_node of this DescribeClusterResponseContent.


        :return: The head_node of this DescribeClusterResponseContent.
        :rtype: EC2Instance
        """
        return self._head_node

    @head_node.setter
    def head_node(self, head_node):
        """Sets the head_node of this DescribeClusterResponseContent.


        :param head_node: The head_node of this DescribeClusterResponseContent.
        :type head_node: EC2Instance
        """

        self._head_node = head_node

    @property
    def login_nodes(self):
        """Gets the login_nodes of this DescribeClusterResponseContent.


        :return: The login_nodes of this DescribeClusterResponseContent.
        :rtype: LoginNodesPool
        """
        return self._login_nodes

    @login_nodes.setter
    def login_nodes(self, login_nodes):
        """Sets the login_nodes of this DescribeClusterResponseContent.


        :param login_nodes: The login_nodes of this DescribeClusterResponseContent.
        :type login_nodes: LoginNodesPool
        """

        self._login_nodes = login_nodes

    @property
    def failures(self):
        """Gets the failures of this DescribeClusterResponseContent.

        Failures array containing failures reason and code when the stack is in CREATE_FAILED status.  # noqa: E501

        :return: The failures of this DescribeClusterResponseContent.
        :rtype: List[Failure]
        """
        return self._failures

    @failures.setter
    def failures(self, failures):
        """Sets the failures of this DescribeClusterResponseContent.

        Failures array containing failures reason and code when the stack is in CREATE_FAILED status.  # noqa: E501

        :param failures: The failures of this DescribeClusterResponseContent.
        :type failures: List[Failure]
        """

        self._failures = failures

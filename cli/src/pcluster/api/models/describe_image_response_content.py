# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from pcluster.api import util
from pcluster.api.models.base_model_ import Model
from pcluster.api.models.cloud_formation_stack_status import CloudFormationStackStatus  # noqa: E501
from pcluster.api.models.ec2_ami_info import Ec2AmiInfo  # noqa: E501
from pcluster.api.models.image_build_status import ImageBuildStatus  # noqa: E501
from pcluster.api.models.image_builder_image_status import ImageBuilderImageStatus  # noqa: E501
from pcluster.api.models.image_configuration_structure import ImageConfigurationStructure  # noqa: E501
from pcluster.api.models.tag import Tag  # noqa: E501


class DescribeImageResponseContent(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, image_id=None, region=None, version=None, image_build_status=None, image_build_logs_arn=None, cloudformation_stack_status=None, cloudformation_stack_status_reason=None, cloudformation_stack_arn=None, creation_time=None, cloudformation_stack_creation_time=None, cloudformation_stack_tags=None, image_configuration=None, imagebuilder_image_status=None, imagebuilder_image_status_reason=None, ec2_ami_info=None):  # noqa: E501
        """DescribeImageResponseContent - a model defined in OpenAPI

        :param image_id: The image_id of this DescribeImageResponseContent.  # noqa: E501
        :type image_id: str
        :param region: The region of this DescribeImageResponseContent.  # noqa: E501
        :type region: str
        :param version: The version of this DescribeImageResponseContent.  # noqa: E501
        :type version: str
        :param image_build_status: The image_build_status of this DescribeImageResponseContent.  # noqa: E501
        :type image_build_status: ImageBuildStatus
        :param image_build_logs_arn: The image_build_logs_arn of this DescribeImageResponseContent.  # noqa: E501
        :type image_build_logs_arn: str
        :param cloudformation_stack_status: The cloudformation_stack_status of this DescribeImageResponseContent.  # noqa: E501
        :type cloudformation_stack_status: CloudFormationStackStatus
        :param cloudformation_stack_status_reason: The cloudformation_stack_status_reason of this DescribeImageResponseContent.  # noqa: E501
        :type cloudformation_stack_status_reason: str
        :param cloudformation_stack_arn: The cloudformation_stack_arn of this DescribeImageResponseContent.  # noqa: E501
        :type cloudformation_stack_arn: str
        :param creation_time: The creation_time of this DescribeImageResponseContent.  # noqa: E501
        :type creation_time: datetime
        :param cloudformation_stack_creation_time: The cloudformation_stack_creation_time of this DescribeImageResponseContent.  # noqa: E501
        :type cloudformation_stack_creation_time: datetime
        :param cloudformation_stack_tags: The cloudformation_stack_tags of this DescribeImageResponseContent.  # noqa: E501
        :type cloudformation_stack_tags: List[Tag]
        :param image_configuration: The image_configuration of this DescribeImageResponseContent.  # noqa: E501
        :type image_configuration: ImageConfigurationStructure
        :param imagebuilder_image_status: The imagebuilder_image_status of this DescribeImageResponseContent.  # noqa: E501
        :type imagebuilder_image_status: ImageBuilderImageStatus
        :param imagebuilder_image_status_reason: The imagebuilder_image_status_reason of this DescribeImageResponseContent.  # noqa: E501
        :type imagebuilder_image_status_reason: str
        :param ec2_ami_info: The ec2_ami_info of this DescribeImageResponseContent.  # noqa: E501
        :type ec2_ami_info: Ec2AmiInfo
        """
        self.openapi_types = {
            'image_id': str,
            'region': str,
            'version': str,
            'image_build_status': ImageBuildStatus,
            'image_build_logs_arn': str,
            'cloudformation_stack_status': CloudFormationStackStatus,
            'cloudformation_stack_status_reason': str,
            'cloudformation_stack_arn': str,
            'creation_time': datetime,
            'cloudformation_stack_creation_time': datetime,
            'cloudformation_stack_tags': List[Tag],
            'image_configuration': ImageConfigurationStructure,
            'imagebuilder_image_status': ImageBuilderImageStatus,
            'imagebuilder_image_status_reason': str,
            'ec2_ami_info': Ec2AmiInfo
        }

        self.attribute_map = {
            'image_id': 'imageId',
            'region': 'region',
            'version': 'version',
            'image_build_status': 'imageBuildStatus',
            'image_build_logs_arn': 'imageBuildLogsArn',
            'cloudformation_stack_status': 'cloudformationStackStatus',
            'cloudformation_stack_status_reason': 'cloudformationStackStatusReason',
            'cloudformation_stack_arn': 'cloudformationStackArn',
            'creation_time': 'creationTime',
            'cloudformation_stack_creation_time': 'cloudformationStackCreationTime',
            'cloudformation_stack_tags': 'cloudformationStackTags',
            'image_configuration': 'imageConfiguration',
            'imagebuilder_image_status': 'imagebuilderImageStatus',
            'imagebuilder_image_status_reason': 'imagebuilderImageStatusReason',
            'ec2_ami_info': 'ec2AmiInfo'
        }

        self._image_id = image_id
        self._region = region
        self._version = version
        self._image_build_status = image_build_status
        self._image_build_logs_arn = image_build_logs_arn
        self._cloudformation_stack_status = cloudformation_stack_status
        self._cloudformation_stack_status_reason = cloudformation_stack_status_reason
        self._cloudformation_stack_arn = cloudformation_stack_arn
        self._creation_time = creation_time
        self._cloudformation_stack_creation_time = cloudformation_stack_creation_time
        self._cloudformation_stack_tags = cloudformation_stack_tags
        self._image_configuration = image_configuration
        self._imagebuilder_image_status = imagebuilder_image_status
        self._imagebuilder_image_status_reason = imagebuilder_image_status_reason
        self._ec2_ami_info = ec2_ami_info

    @classmethod
    def from_dict(cls, dikt) -> 'DescribeImageResponseContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DescribeImageResponseContent of this DescribeImageResponseContent.  # noqa: E501
        :rtype: DescribeImageResponseContent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def image_id(self):
        """Gets the image_id of this DescribeImageResponseContent.

        Id of the Image to retrieve detailed information for.  # noqa: E501

        :return: The image_id of this DescribeImageResponseContent.
        :rtype: str
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id):
        """Sets the image_id of this DescribeImageResponseContent.

        Id of the Image to retrieve detailed information for.  # noqa: E501

        :param image_id: The image_id of this DescribeImageResponseContent.
        :type image_id: str
        """
        if image_id is None:
            raise ValueError("Invalid value for `image_id`, must not be `None`")  # noqa: E501

        self._image_id = image_id

    @property
    def region(self):
        """Gets the region of this DescribeImageResponseContent.

        AWS region where the image is created.  # noqa: E501

        :return: The region of this DescribeImageResponseContent.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this DescribeImageResponseContent.

        AWS region where the image is created.  # noqa: E501

        :param region: The region of this DescribeImageResponseContent.
        :type region: str
        """
        if region is None:
            raise ValueError("Invalid value for `region`, must not be `None`")  # noqa: E501

        self._region = region

    @property
    def version(self):
        """Gets the version of this DescribeImageResponseContent.

        ParallelCluster version used to build the image.  # noqa: E501

        :return: The version of this DescribeImageResponseContent.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DescribeImageResponseContent.

        ParallelCluster version used to build the image.  # noqa: E501

        :param version: The version of this DescribeImageResponseContent.
        :type version: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def image_build_status(self):
        """Gets the image_build_status of this DescribeImageResponseContent.


        :return: The image_build_status of this DescribeImageResponseContent.
        :rtype: ImageBuildStatus
        """
        return self._image_build_status

    @image_build_status.setter
    def image_build_status(self, image_build_status):
        """Sets the image_build_status of this DescribeImageResponseContent.


        :param image_build_status: The image_build_status of this DescribeImageResponseContent.
        :type image_build_status: ImageBuildStatus
        """
        if image_build_status is None:
            raise ValueError("Invalid value for `image_build_status`, must not be `None`")  # noqa: E501

        self._image_build_status = image_build_status

    @property
    def image_build_logs_arn(self):
        """Gets the image_build_logs_arn of this DescribeImageResponseContent.

        ARN of the logs for the image build process.  # noqa: E501

        :return: The image_build_logs_arn of this DescribeImageResponseContent.
        :rtype: str
        """
        return self._image_build_logs_arn

    @image_build_logs_arn.setter
    def image_build_logs_arn(self, image_build_logs_arn):
        """Sets the image_build_logs_arn of this DescribeImageResponseContent.

        ARN of the logs for the image build process.  # noqa: E501

        :param image_build_logs_arn: The image_build_logs_arn of this DescribeImageResponseContent.
        :type image_build_logs_arn: str
        """

        self._image_build_logs_arn = image_build_logs_arn

    @property
    def cloudformation_stack_status(self):
        """Gets the cloudformation_stack_status of this DescribeImageResponseContent.


        :return: The cloudformation_stack_status of this DescribeImageResponseContent.
        :rtype: CloudFormationStackStatus
        """
        return self._cloudformation_stack_status

    @cloudformation_stack_status.setter
    def cloudformation_stack_status(self, cloudformation_stack_status):
        """Sets the cloudformation_stack_status of this DescribeImageResponseContent.


        :param cloudformation_stack_status: The cloudformation_stack_status of this DescribeImageResponseContent.
        :type cloudformation_stack_status: CloudFormationStackStatus
        """

        self._cloudformation_stack_status = cloudformation_stack_status

    @property
    def cloudformation_stack_status_reason(self):
        """Gets the cloudformation_stack_status_reason of this DescribeImageResponseContent.

        Reason for the CloudFormation stack status.  # noqa: E501

        :return: The cloudformation_stack_status_reason of this DescribeImageResponseContent.
        :rtype: str
        """
        return self._cloudformation_stack_status_reason

    @cloudformation_stack_status_reason.setter
    def cloudformation_stack_status_reason(self, cloudformation_stack_status_reason):
        """Sets the cloudformation_stack_status_reason of this DescribeImageResponseContent.

        Reason for the CloudFormation stack status.  # noqa: E501

        :param cloudformation_stack_status_reason: The cloudformation_stack_status_reason of this DescribeImageResponseContent.
        :type cloudformation_stack_status_reason: str
        """

        self._cloudformation_stack_status_reason = cloudformation_stack_status_reason

    @property
    def cloudformation_stack_arn(self):
        """Gets the cloudformation_stack_arn of this DescribeImageResponseContent.

        ARN of the main CloudFormation stack.  # noqa: E501

        :return: The cloudformation_stack_arn of this DescribeImageResponseContent.
        :rtype: str
        """
        return self._cloudformation_stack_arn

    @cloudformation_stack_arn.setter
    def cloudformation_stack_arn(self, cloudformation_stack_arn):
        """Sets the cloudformation_stack_arn of this DescribeImageResponseContent.

        ARN of the main CloudFormation stack.  # noqa: E501

        :param cloudformation_stack_arn: The cloudformation_stack_arn of this DescribeImageResponseContent.
        :type cloudformation_stack_arn: str
        """

        self._cloudformation_stack_arn = cloudformation_stack_arn

    @property
    def creation_time(self):
        """Gets the creation_time of this DescribeImageResponseContent.

        Timestamp representing the image creation time.  # noqa: E501

        :return: The creation_time of this DescribeImageResponseContent.
        :rtype: datetime
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """Sets the creation_time of this DescribeImageResponseContent.

        Timestamp representing the image creation time.  # noqa: E501

        :param creation_time: The creation_time of this DescribeImageResponseContent.
        :type creation_time: datetime
        """

        self._creation_time = creation_time

    @property
    def cloudformation_stack_creation_time(self):
        """Gets the cloudformation_stack_creation_time of this DescribeImageResponseContent.

        Timestamp representing the CloudFormation stack creation time.  # noqa: E501

        :return: The cloudformation_stack_creation_time of this DescribeImageResponseContent.
        :rtype: datetime
        """
        return self._cloudformation_stack_creation_time

    @cloudformation_stack_creation_time.setter
    def cloudformation_stack_creation_time(self, cloudformation_stack_creation_time):
        """Sets the cloudformation_stack_creation_time of this DescribeImageResponseContent.

        Timestamp representing the CloudFormation stack creation time.  # noqa: E501

        :param cloudformation_stack_creation_time: The cloudformation_stack_creation_time of this DescribeImageResponseContent.
        :type cloudformation_stack_creation_time: datetime
        """

        self._cloudformation_stack_creation_time = cloudformation_stack_creation_time

    @property
    def cloudformation_stack_tags(self):
        """Gets the cloudformation_stack_tags of this DescribeImageResponseContent.

        Tags for the CloudFormation stack.  # noqa: E501

        :return: The cloudformation_stack_tags of this DescribeImageResponseContent.
        :rtype: List[Tag]
        """
        return self._cloudformation_stack_tags

    @cloudformation_stack_tags.setter
    def cloudformation_stack_tags(self, cloudformation_stack_tags):
        """Sets the cloudformation_stack_tags of this DescribeImageResponseContent.

        Tags for the CloudFormation stack.  # noqa: E501

        :param cloudformation_stack_tags: The cloudformation_stack_tags of this DescribeImageResponseContent.
        :type cloudformation_stack_tags: List[Tag]
        """

        self._cloudformation_stack_tags = cloudformation_stack_tags

    @property
    def image_configuration(self):
        """Gets the image_configuration of this DescribeImageResponseContent.


        :return: The image_configuration of this DescribeImageResponseContent.
        :rtype: ImageConfigurationStructure
        """
        return self._image_configuration

    @image_configuration.setter
    def image_configuration(self, image_configuration):
        """Sets the image_configuration of this DescribeImageResponseContent.


        :param image_configuration: The image_configuration of this DescribeImageResponseContent.
        :type image_configuration: ImageConfigurationStructure
        """
        if image_configuration is None:
            raise ValueError("Invalid value for `image_configuration`, must not be `None`")  # noqa: E501

        self._image_configuration = image_configuration

    @property
    def imagebuilder_image_status(self):
        """Gets the imagebuilder_image_status of this DescribeImageResponseContent.


        :return: The imagebuilder_image_status of this DescribeImageResponseContent.
        :rtype: ImageBuilderImageStatus
        """
        return self._imagebuilder_image_status

    @imagebuilder_image_status.setter
    def imagebuilder_image_status(self, imagebuilder_image_status):
        """Sets the imagebuilder_image_status of this DescribeImageResponseContent.


        :param imagebuilder_image_status: The imagebuilder_image_status of this DescribeImageResponseContent.
        :type imagebuilder_image_status: ImageBuilderImageStatus
        """

        self._imagebuilder_image_status = imagebuilder_image_status

    @property
    def imagebuilder_image_status_reason(self):
        """Gets the imagebuilder_image_status_reason of this DescribeImageResponseContent.

        Reason for the ImageBuilder Image status.  # noqa: E501

        :return: The imagebuilder_image_status_reason of this DescribeImageResponseContent.
        :rtype: str
        """
        return self._imagebuilder_image_status_reason

    @imagebuilder_image_status_reason.setter
    def imagebuilder_image_status_reason(self, imagebuilder_image_status_reason):
        """Sets the imagebuilder_image_status_reason of this DescribeImageResponseContent.

        Reason for the ImageBuilder Image status.  # noqa: E501

        :param imagebuilder_image_status_reason: The imagebuilder_image_status_reason of this DescribeImageResponseContent.
        :type imagebuilder_image_status_reason: str
        """

        self._imagebuilder_image_status_reason = imagebuilder_image_status_reason

    @property
    def ec2_ami_info(self):
        """Gets the ec2_ami_info of this DescribeImageResponseContent.


        :return: The ec2_ami_info of this DescribeImageResponseContent.
        :rtype: Ec2AmiInfo
        """
        return self._ec2_ami_info

    @ec2_ami_info.setter
    def ec2_ami_info(self, ec2_ami_info):
        """Sets the ec2_ami_info of this DescribeImageResponseContent.


        :param ec2_ami_info: The ec2_ami_info of this DescribeImageResponseContent.
        :type ec2_ami_info: Ec2AmiInfo
        """

        self._ec2_ami_info = ec2_ami_info

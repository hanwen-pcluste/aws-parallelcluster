# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from pcluster.api.models.base_model_ import Model
from pcluster.api.models.ec2_ami_state import Ec2AmiState
from pcluster.api.models.tag import Tag
from pcluster.api import util

from pcluster.api.models.ec2_ami_state import Ec2AmiState  # noqa: E501
from pcluster.api.models.tag import Tag  # noqa: E501

class Ec2AmiInfo(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, ami_id=None, tags=None, ami_name=None, architecture=None, state=None, description=None):  # noqa: E501
        """Ec2AmiInfo - a model defined in OpenAPI

        :param ami_id: The ami_id of this Ec2AmiInfo.  # noqa: E501
        :type ami_id: str
        :param tags: The tags of this Ec2AmiInfo.  # noqa: E501
        :type tags: List[Tag]
        :param ami_name: The ami_name of this Ec2AmiInfo.  # noqa: E501
        :type ami_name: str
        :param architecture: The architecture of this Ec2AmiInfo.  # noqa: E501
        :type architecture: str
        :param state: The state of this Ec2AmiInfo.  # noqa: E501
        :type state: Ec2AmiState
        :param description: The description of this Ec2AmiInfo.  # noqa: E501
        :type description: str
        """
        self.openapi_types = {
            'ami_id': str,
            'tags': List[Tag],
            'ami_name': str,
            'architecture': str,
            'state': Ec2AmiState,
            'description': str
        }

        self.attribute_map = {
            'ami_id': 'amiId',
            'tags': 'tags',
            'ami_name': 'amiName',
            'architecture': 'architecture',
            'state': 'state',
            'description': 'description'
        }

        self._ami_id = ami_id
        self._tags = tags
        self._ami_name = ami_name
        self._architecture = architecture
        self._state = state
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'Ec2AmiInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Ec2AmiInfo of this Ec2AmiInfo.  # noqa: E501
        :rtype: Ec2AmiInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def ami_id(self):
        """Gets the ami_id of this Ec2AmiInfo.

        EC2 AMI id  # noqa: E501

        :return: The ami_id of this Ec2AmiInfo.
        :rtype: str
        """
        return self._ami_id

    @ami_id.setter
    def ami_id(self, ami_id):
        """Sets the ami_id of this Ec2AmiInfo.

        EC2 AMI id  # noqa: E501

        :param ami_id: The ami_id of this Ec2AmiInfo.
        :type ami_id: str
        """
        if ami_id is None:
            raise ValueError("Invalid value for `ami_id`, must not be `None`")  # noqa: E501

        self._ami_id = ami_id

    @property
    def tags(self):
        """Gets the tags of this Ec2AmiInfo.

        EC2 AMI Tags  # noqa: E501

        :return: The tags of this Ec2AmiInfo.
        :rtype: List[Tag]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this Ec2AmiInfo.

        EC2 AMI Tags  # noqa: E501

        :param tags: The tags of this Ec2AmiInfo.
        :type tags: List[Tag]
        """

        self._tags = tags

    @property
    def ami_name(self):
        """Gets the ami_name of this Ec2AmiInfo.

        EC2 AMI name  # noqa: E501

        :return: The ami_name of this Ec2AmiInfo.
        :rtype: str
        """
        return self._ami_name

    @ami_name.setter
    def ami_name(self, ami_name):
        """Sets the ami_name of this Ec2AmiInfo.

        EC2 AMI name  # noqa: E501

        :param ami_name: The ami_name of this Ec2AmiInfo.
        :type ami_name: str
        """

        self._ami_name = ami_name

    @property
    def architecture(self):
        """Gets the architecture of this Ec2AmiInfo.

        EC2 AMI architecture  # noqa: E501

        :return: The architecture of this Ec2AmiInfo.
        :rtype: str
        """
        return self._architecture

    @architecture.setter
    def architecture(self, architecture):
        """Sets the architecture of this Ec2AmiInfo.

        EC2 AMI architecture  # noqa: E501

        :param architecture: The architecture of this Ec2AmiInfo.
        :type architecture: str
        """

        self._architecture = architecture

    @property
    def state(self):
        """Gets the state of this Ec2AmiInfo.


        :return: The state of this Ec2AmiInfo.
        :rtype: Ec2AmiState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Ec2AmiInfo.


        :param state: The state of this Ec2AmiInfo.
        :type state: Ec2AmiState
        """

        self._state = state

    @property
    def description(self):
        """Gets the description of this Ec2AmiInfo.

        EC2 AMI description  # noqa: E501

        :return: The description of this Ec2AmiInfo.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Ec2AmiInfo.

        EC2 AMI description  # noqa: E501

        :param description: The description of this Ec2AmiInfo.
        :type description: str
        """

        self._description = description

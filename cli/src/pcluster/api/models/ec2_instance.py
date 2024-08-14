# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from pcluster.api import util
from pcluster.api.models.base_model_ import Model
from pcluster.api.models.instance_state import InstanceState  # noqa: E501


class EC2Instance(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, instance_id=None, instance_type=None, launch_time=None, private_ip_address=None, public_ip_address=None, state=None):  # noqa: E501
        """EC2Instance - a model defined in OpenAPI

        :param instance_id: The instance_id of this EC2Instance.  # noqa: E501
        :type instance_id: str
        :param instance_type: The instance_type of this EC2Instance.  # noqa: E501
        :type instance_type: str
        :param launch_time: The launch_time of this EC2Instance.  # noqa: E501
        :type launch_time: datetime
        :param private_ip_address: The private_ip_address of this EC2Instance.  # noqa: E501
        :type private_ip_address: str
        :param public_ip_address: The public_ip_address of this EC2Instance.  # noqa: E501
        :type public_ip_address: str
        :param state: The state of this EC2Instance.  # noqa: E501
        :type state: InstanceState
        """
        self.openapi_types = {
            'instance_id': str,
            'instance_type': str,
            'launch_time': datetime,
            'private_ip_address': str,
            'public_ip_address': str,
            'state': InstanceState
        }

        self.attribute_map = {
            'instance_id': 'instanceId',
            'instance_type': 'instanceType',
            'launch_time': 'launchTime',
            'private_ip_address': 'privateIpAddress',
            'public_ip_address': 'publicIpAddress',
            'state': 'state'
        }

        self._instance_id = instance_id
        self._instance_type = instance_type
        self._launch_time = launch_time
        self._private_ip_address = private_ip_address
        self._public_ip_address = public_ip_address
        self._state = state

    @classmethod
    def from_dict(cls, dikt) -> 'EC2Instance':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EC2Instance of this EC2Instance.  # noqa: E501
        :rtype: EC2Instance
        """
        return util.deserialize_model(dikt, cls)

    @property
    def instance_id(self):
        """Gets the instance_id of this EC2Instance.


        :return: The instance_id of this EC2Instance.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this EC2Instance.


        :param instance_id: The instance_id of this EC2Instance.
        :type instance_id: str
        """
        if instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def instance_type(self):
        """Gets the instance_type of this EC2Instance.


        :return: The instance_type of this EC2Instance.
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        """Sets the instance_type of this EC2Instance.


        :param instance_type: The instance_type of this EC2Instance.
        :type instance_type: str
        """
        if instance_type is None:
            raise ValueError("Invalid value for `instance_type`, must not be `None`")  # noqa: E501

        self._instance_type = instance_type

    @property
    def launch_time(self):
        """Gets the launch_time of this EC2Instance.


        :return: The launch_time of this EC2Instance.
        :rtype: datetime
        """
        return self._launch_time

    @launch_time.setter
    def launch_time(self, launch_time):
        """Sets the launch_time of this EC2Instance.


        :param launch_time: The launch_time of this EC2Instance.
        :type launch_time: datetime
        """
        if launch_time is None:
            raise ValueError("Invalid value for `launch_time`, must not be `None`")  # noqa: E501

        self._launch_time = launch_time

    @property
    def private_ip_address(self):
        """Gets the private_ip_address of this EC2Instance.


        :return: The private_ip_address of this EC2Instance.
        :rtype: str
        """
        return self._private_ip_address

    @private_ip_address.setter
    def private_ip_address(self, private_ip_address):
        """Sets the private_ip_address of this EC2Instance.


        :param private_ip_address: The private_ip_address of this EC2Instance.
        :type private_ip_address: str
        """
        if private_ip_address is None:
            raise ValueError("Invalid value for `private_ip_address`, must not be `None`")  # noqa: E501

        self._private_ip_address = private_ip_address

    @property
    def public_ip_address(self):
        """Gets the public_ip_address of this EC2Instance.


        :return: The public_ip_address of this EC2Instance.
        :rtype: str
        """
        return self._public_ip_address

    @public_ip_address.setter
    def public_ip_address(self, public_ip_address):
        """Sets the public_ip_address of this EC2Instance.


        :param public_ip_address: The public_ip_address of this EC2Instance.
        :type public_ip_address: str
        """

        self._public_ip_address = public_ip_address

    @property
    def state(self):
        """Gets the state of this EC2Instance.


        :return: The state of this EC2Instance.
        :rtype: InstanceState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this EC2Instance.


        :param state: The state of this EC2Instance.
        :type state: InstanceState
        """
        if state is None:
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

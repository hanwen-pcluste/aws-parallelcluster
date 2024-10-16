# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from pcluster.api.models.base_model_ import Model
from pcluster.api import util


class Change(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, parameter=None, current_value=None, requested_value=None):  # noqa: E501
        """Change - a model defined in OpenAPI

        :param parameter: The parameter of this Change.  # noqa: E501
        :type parameter: str
        :param current_value: The current_value of this Change.  # noqa: E501
        :type current_value: str
        :param requested_value: The requested_value of this Change.  # noqa: E501
        :type requested_value: str
        """
        self.openapi_types = {
            'parameter': str,
            'current_value': str,
            'requested_value': str
        }

        self.attribute_map = {
            'parameter': 'parameter',
            'current_value': 'currentValue',
            'requested_value': 'requestedValue'
        }

        self._parameter = parameter
        self._current_value = current_value
        self._requested_value = requested_value

    @classmethod
    def from_dict(cls, dikt) -> 'Change':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Change of this Change.  # noqa: E501
        :rtype: Change
        """
        return util.deserialize_model(dikt, cls)

    @property
    def parameter(self):
        """Gets the parameter of this Change.


        :return: The parameter of this Change.
        :rtype: str
        """
        return self._parameter

    @parameter.setter
    def parameter(self, parameter):
        """Sets the parameter of this Change.


        :param parameter: The parameter of this Change.
        :type parameter: str
        """

        self._parameter = parameter

    @property
    def current_value(self):
        """Gets the current_value of this Change.


        :return: The current_value of this Change.
        :rtype: str
        """
        return self._current_value

    @current_value.setter
    def current_value(self, current_value):
        """Sets the current_value of this Change.


        :param current_value: The current_value of this Change.
        :type current_value: str
        """

        self._current_value = current_value

    @property
    def requested_value(self):
        """Gets the requested_value of this Change.


        :return: The requested_value of this Change.
        :rtype: str
        """
        return self._requested_value

    @requested_value.setter
    def requested_value(self, requested_value):
        """Sets the requested_value of this Change.


        :param requested_value: The requested_value of this Change.
        :type requested_value: str
        """

        self._requested_value = requested_value

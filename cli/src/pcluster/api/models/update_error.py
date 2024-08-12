# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from pcluster.api.models.base_model_ import Model
from pcluster.api import util


class UpdateError(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, parameter=None, current_value=None, requested_value=None, message=None):  # noqa: E501
        """UpdateError - a model defined in OpenAPI

        :param parameter: The parameter of this UpdateError.  # noqa: E501
        :type parameter: str
        :param current_value: The current_value of this UpdateError.  # noqa: E501
        :type current_value: str
        :param requested_value: The requested_value of this UpdateError.  # noqa: E501
        :type requested_value: str
        :param message: The message of this UpdateError.  # noqa: E501
        :type message: str
        """
        self.openapi_types = {
            'parameter': str,
            'current_value': str,
            'requested_value': str,
            'message': str
        }

        self.attribute_map = {
            'parameter': 'parameter',
            'current_value': 'currentValue',
            'requested_value': 'requestedValue',
            'message': 'message'
        }

        self._parameter = parameter
        self._current_value = current_value
        self._requested_value = requested_value
        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'UpdateError':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UpdateError of this UpdateError.  # noqa: E501
        :rtype: UpdateError
        """
        return util.deserialize_model(dikt, cls)

    @property
    def parameter(self):
        """Gets the parameter of this UpdateError.


        :return: The parameter of this UpdateError.
        :rtype: str
        """
        return self._parameter

    @parameter.setter
    def parameter(self, parameter):
        """Sets the parameter of this UpdateError.


        :param parameter: The parameter of this UpdateError.
        :type parameter: str
        """

        self._parameter = parameter

    @property
    def current_value(self):
        """Gets the current_value of this UpdateError.


        :return: The current_value of this UpdateError.
        :rtype: str
        """
        return self._current_value

    @current_value.setter
    def current_value(self, current_value):
        """Sets the current_value of this UpdateError.


        :param current_value: The current_value of this UpdateError.
        :type current_value: str
        """

        self._current_value = current_value

    @property
    def requested_value(self):
        """Gets the requested_value of this UpdateError.


        :return: The requested_value of this UpdateError.
        :rtype: str
        """
        return self._requested_value

    @requested_value.setter
    def requested_value(self, requested_value):
        """Sets the requested_value of this UpdateError.


        :param requested_value: The requested_value of this UpdateError.
        :type requested_value: str
        """

        self._requested_value = requested_value

    @property
    def message(self):
        """Gets the message of this UpdateError.


        :return: The message of this UpdateError.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this UpdateError.


        :param message: The message of this UpdateError.
        :type message: str
        """

        self._message = message

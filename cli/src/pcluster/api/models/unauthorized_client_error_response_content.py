# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from pcluster.api.models.base_model_ import Model
from pcluster.api import util


class UnauthorizedClientErrorResponseContent(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, message=None):  # noqa: E501
        """UnauthorizedClientErrorResponseContent - a model defined in OpenAPI

        :param message: The message of this UnauthorizedClientErrorResponseContent.  # noqa: E501
        :type message: str
        """
        self.openapi_types = {
            'message': str
        }

        self.attribute_map = {
            'message': 'message'
        }

        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'UnauthorizedClientErrorResponseContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UnauthorizedClientErrorResponseContent of this UnauthorizedClientErrorResponseContent.  # noqa: E501
        :rtype: UnauthorizedClientErrorResponseContent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self):
        """Gets the message of this UnauthorizedClientErrorResponseContent.


        :return: The message of this UnauthorizedClientErrorResponseContent.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this UnauthorizedClientErrorResponseContent.


        :param message: The message of this UnauthorizedClientErrorResponseContent.
        :type message: str
        """

        self._message = message

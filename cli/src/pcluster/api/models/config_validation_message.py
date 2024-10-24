# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from pcluster.api.models.base_model_ import Model
from pcluster.api.models.validation_level import ValidationLevel
from pcluster.api import util

from pcluster.api.models.validation_level import ValidationLevel  # noqa: E501

class ConfigValidationMessage(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, type=None, level=None, message=None):  # noqa: E501
        """ConfigValidationMessage - a model defined in OpenAPI

        :param id: The id of this ConfigValidationMessage.  # noqa: E501
        :type id: str
        :param type: The type of this ConfigValidationMessage.  # noqa: E501
        :type type: str
        :param level: The level of this ConfigValidationMessage.  # noqa: E501
        :type level: ValidationLevel
        :param message: The message of this ConfigValidationMessage.  # noqa: E501
        :type message: str
        """
        self.openapi_types = {
            'id': str,
            'type': str,
            'level': ValidationLevel,
            'message': str
        }

        self.attribute_map = {
            'id': 'id',
            'type': 'type',
            'level': 'level',
            'message': 'message'
        }

        self._id = id
        self._type = type
        self._level = level
        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'ConfigValidationMessage':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ConfigValidationMessage of this ConfigValidationMessage.  # noqa: E501
        :rtype: ConfigValidationMessage
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this ConfigValidationMessage.

        Id of the validator.  # noqa: E501

        :return: The id of this ConfigValidationMessage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConfigValidationMessage.

        Id of the validator.  # noqa: E501

        :param id: The id of this ConfigValidationMessage.
        :type id: str
        """

        self._id = id

    @property
    def type(self):
        """Gets the type of this ConfigValidationMessage.

        Type of the validator.  # noqa: E501

        :return: The type of this ConfigValidationMessage.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ConfigValidationMessage.

        Type of the validator.  # noqa: E501

        :param type: The type of this ConfigValidationMessage.
        :type type: str
        """

        self._type = type

    @property
    def level(self):
        """Gets the level of this ConfigValidationMessage.


        :return: The level of this ConfigValidationMessage.
        :rtype: ValidationLevel
        """
        return self._level

    @level.setter
    def level(self, level):
        """Sets the level of this ConfigValidationMessage.


        :param level: The level of this ConfigValidationMessage.
        :type level: ValidationLevel
        """

        self._level = level

    @property
    def message(self):
        """Gets the message of this ConfigValidationMessage.

        Validation message  # noqa: E501

        :return: The message of this ConfigValidationMessage.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ConfigValidationMessage.

        Validation message  # noqa: E501

        :param message: The message of this ConfigValidationMessage.
        :type message: str
        """

        self._message = message

# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from pcluster.api.models.base_model_ import Model
from pcluster.api.models.config_validation_message import ConfigValidationMessage
from pcluster.api.models.image_info_summary import ImageInfoSummary
from pcluster.api import util

from pcluster.api.models.config_validation_message import ConfigValidationMessage  # noqa: E501
from pcluster.api.models.image_info_summary import ImageInfoSummary  # noqa: E501

class BuildImageResponseContent(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, image=None, validation_messages=None):  # noqa: E501
        """BuildImageResponseContent - a model defined in OpenAPI

        :param image: The image of this BuildImageResponseContent.  # noqa: E501
        :type image: ImageInfoSummary
        :param validation_messages: The validation_messages of this BuildImageResponseContent.  # noqa: E501
        :type validation_messages: List[ConfigValidationMessage]
        """
        self.openapi_types = {
            'image': ImageInfoSummary,
            'validation_messages': List[ConfigValidationMessage]
        }

        self.attribute_map = {
            'image': 'image',
            'validation_messages': 'validationMessages'
        }

        self._image = image
        self._validation_messages = validation_messages

    @classmethod
    def from_dict(cls, dikt) -> 'BuildImageResponseContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The BuildImageResponseContent of this BuildImageResponseContent.  # noqa: E501
        :rtype: BuildImageResponseContent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def image(self):
        """Gets the image of this BuildImageResponseContent.


        :return: The image of this BuildImageResponseContent.
        :rtype: ImageInfoSummary
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this BuildImageResponseContent.


        :param image: The image of this BuildImageResponseContent.
        :type image: ImageInfoSummary
        """
        if image is None:
            raise ValueError("Invalid value for `image`, must not be `None`")  # noqa: E501

        self._image = image

    @property
    def validation_messages(self):
        """Gets the validation_messages of this BuildImageResponseContent.

        List of messages collected during image config validation whose level is lower than the 'validationFailureLevel' set by the user.  # noqa: E501

        :return: The validation_messages of this BuildImageResponseContent.
        :rtype: List[ConfigValidationMessage]
        """
        return self._validation_messages

    @validation_messages.setter
    def validation_messages(self, validation_messages):
        """Sets the validation_messages of this BuildImageResponseContent.

        List of messages collected during image config validation whose level is lower than the 'validationFailureLevel' set by the user.  # noqa: E501

        :param validation_messages: The validation_messages of this BuildImageResponseContent.
        :type validation_messages: List[ConfigValidationMessage]
        """

        self._validation_messages = validation_messages

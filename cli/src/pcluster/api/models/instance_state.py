# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from pcluster.api.models.base_model_ import Model
from pcluster.api import util


class InstanceState(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    PENDING = "pending"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting-down"
    TERMINATED = "terminated"
    STOPPING = "stopping"
    STOPPED = "stopped"
    def __init__(self):  # noqa: E501
        """InstanceState - a model defined in OpenAPI

        """
        self.openapi_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'InstanceState':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The InstanceState of this InstanceState.  # noqa: E501
        :rtype: InstanceState
        """
        return util.deserialize_model(dikt, cls)

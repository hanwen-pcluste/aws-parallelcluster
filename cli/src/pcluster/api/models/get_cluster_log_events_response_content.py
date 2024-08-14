# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from pcluster.api import util
from pcluster.api.models.base_model_ import Model
from pcluster.api.models.log_event import LogEvent  # noqa: E501


class GetClusterLogEventsResponseContent(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, next_token=None, prev_token=None, events=None):  # noqa: E501
        """GetClusterLogEventsResponseContent - a model defined in OpenAPI

        :param next_token: The next_token of this GetClusterLogEventsResponseContent.  # noqa: E501
        :type next_token: str
        :param prev_token: The prev_token of this GetClusterLogEventsResponseContent.  # noqa: E501
        :type prev_token: str
        :param events: The events of this GetClusterLogEventsResponseContent.  # noqa: E501
        :type events: List[LogEvent]
        """
        self.openapi_types = {
            'next_token': str,
            'prev_token': str,
            'events': List[LogEvent]
        }

        self.attribute_map = {
            'next_token': 'nextToken',
            'prev_token': 'prevToken',
            'events': 'events'
        }

        self._next_token = next_token
        self._prev_token = prev_token
        self._events = events

    @classmethod
    def from_dict(cls, dikt) -> 'GetClusterLogEventsResponseContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GetClusterLogEventsResponseContent of this GetClusterLogEventsResponseContent.  # noqa: E501
        :rtype: GetClusterLogEventsResponseContent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def next_token(self):
        """Gets the next_token of this GetClusterLogEventsResponseContent.

        Token to use for paginated requests.  # noqa: E501

        :return: The next_token of this GetClusterLogEventsResponseContent.
        :rtype: str
        """
        return self._next_token

    @next_token.setter
    def next_token(self, next_token):
        """Sets the next_token of this GetClusterLogEventsResponseContent.

        Token to use for paginated requests.  # noqa: E501

        :param next_token: The next_token of this GetClusterLogEventsResponseContent.
        :type next_token: str
        """

        self._next_token = next_token

    @property
    def prev_token(self):
        """Gets the prev_token of this GetClusterLogEventsResponseContent.

        Token to use for paginated requests.  # noqa: E501

        :return: The prev_token of this GetClusterLogEventsResponseContent.
        :rtype: str
        """
        return self._prev_token

    @prev_token.setter
    def prev_token(self, prev_token):
        """Sets the prev_token of this GetClusterLogEventsResponseContent.

        Token to use for paginated requests.  # noqa: E501

        :param prev_token: The prev_token of this GetClusterLogEventsResponseContent.
        :type prev_token: str
        """

        self._prev_token = prev_token

    @property
    def events(self):
        """Gets the events of this GetClusterLogEventsResponseContent.


        :return: The events of this GetClusterLogEventsResponseContent.
        :rtype: List[LogEvent]
        """
        return self._events

    @events.setter
    def events(self, events):
        """Sets the events of this GetClusterLogEventsResponseContent.


        :param events: The events of this GetClusterLogEventsResponseContent.
        :type events: List[LogEvent]
        """

        self._events = events

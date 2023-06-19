"""
    ParallelCluster

    ParallelCluster API  # noqa: E501

    The version of the OpenAPI document: 3.6.0
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from pcluster_client.api_client import ApiClient, Endpoint as _Endpoint
from pcluster_client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from pcluster_client.model.bad_request_exception_response_content import BadRequestExceptionResponseContent
from pcluster_client.model.describe_compute_fleet_response_content import DescribeComputeFleetResponseContent
from pcluster_client.model.internal_service_exception_response_content import InternalServiceExceptionResponseContent
from pcluster_client.model.limit_exceeded_exception_response_content import LimitExceededExceptionResponseContent
from pcluster_client.model.not_found_exception_response_content import NotFoundExceptionResponseContent
from pcluster_client.model.unauthorized_client_error_response_content import UnauthorizedClientErrorResponseContent
from pcluster_client.model.update_compute_fleet_request_content import UpdateComputeFleetRequestContent
from pcluster_client.model.update_compute_fleet_response_content import UpdateComputeFleetResponseContent


class ClusterComputeFleetApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.describe_compute_fleet_endpoint = _Endpoint(
            settings={
                'response_type': (DescribeComputeFleetResponseContent,),
                'auth': [
                    'aws.auth.sigv4'
                ],
                'endpoint_path': '/v3/clusters/{clusterName}/computefleet',
                'operation_id': 'describe_compute_fleet',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'cluster_name',
                    'region',
                ],
                'required': [
                    'cluster_name',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'cluster_name',
                ]
            },
            root_map={
                'validations': {
                    ('cluster_name',): {

                        'regex': {
                            'pattern': r'^[a-zA-Z][a-zA-Z0-9-]+$',  # noqa: E501
                        },
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'cluster_name':
                        (str,),
                    'region':
                        (str,),
                },
                'attribute_map': {
                    'cluster_name': 'clusterName',
                    'region': 'region',
                },
                'location_map': {
                    'cluster_name': 'path',
                    'region': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.update_compute_fleet_endpoint = _Endpoint(
            settings={
                'response_type': (UpdateComputeFleetResponseContent,),
                'auth': [
                    'aws.auth.sigv4'
                ],
                'endpoint_path': '/v3/clusters/{clusterName}/computefleet',
                'operation_id': 'update_compute_fleet',
                'http_method': 'PATCH',
                'servers': None,
            },
            params_map={
                'all': [
                    'cluster_name',
                    'update_compute_fleet_request_content',
                    'region',
                ],
                'required': [
                    'cluster_name',
                    'update_compute_fleet_request_content',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'cluster_name',
                ]
            },
            root_map={
                'validations': {
                    ('cluster_name',): {

                        'regex': {
                            'pattern': r'^[a-zA-Z][a-zA-Z0-9-]+$',  # noqa: E501
                        },
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'cluster_name':
                        (str,),
                    'update_compute_fleet_request_content':
                        (UpdateComputeFleetRequestContent,),
                    'region':
                        (str,),
                },
                'attribute_map': {
                    'cluster_name': 'clusterName',
                    'region': 'region',
                },
                'location_map': {
                    'cluster_name': 'path',
                    'update_compute_fleet_request_content': 'body',
                    'region': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )

    def describe_compute_fleet(
        self,
        cluster_name,
        **kwargs
    ):
        """describe_compute_fleet  # noqa: E501

        Describe the status of the compute fleet.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.describe_compute_fleet(cluster_name, async_req=True)
        >>> result = thread.get()

        Args:
            cluster_name (str): Name of the cluster

        Keyword Args:
            region (str): AWS Region that the operation corresponds to.. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            DescribeComputeFleetResponseContent
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['cluster_name'] = \
            cluster_name
        return self.describe_compute_fleet_endpoint.call_with_http_info(**kwargs)

    def update_compute_fleet(
        self,
        cluster_name,
        update_compute_fleet_request_content,
        **kwargs
    ):
        """update_compute_fleet  # noqa: E501

        Update the status of the cluster compute fleet.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.update_compute_fleet(cluster_name, update_compute_fleet_request_content, async_req=True)
        >>> result = thread.get()

        Args:
            cluster_name (str): Name of the cluster
            update_compute_fleet_request_content (UpdateComputeFleetRequestContent):

        Keyword Args:
            region (str): AWS Region that the operation corresponds to.. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            UpdateComputeFleetResponseContent
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['cluster_name'] = \
            cluster_name
        kwargs['update_compute_fleet_request_content'] = \
            update_compute_fleet_request_content
        return self.update_compute_fleet_endpoint.call_with_http_info(**kwargs)


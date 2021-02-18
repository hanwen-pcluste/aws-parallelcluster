# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "LICENSE.txt" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# This module contains all the classes representing the Resources objects.
# These objects are obtained from the configuration file through a conversion based on the Schema classes.
#

import operator
from abc import ABC
from typing import List

from pcluster.validators.common import ValidationResult, Validator
from pcluster.validators.s3_validators import UrlValidator


class _ResourceValidator(ABC):
    """Represent a generic validator for a resource attribute or object. It's a module private class."""

    def __init__(self, validator_class: Validator, priority: int = 1, **kwargs):
        """Initialize validator. Note: Validators with higher priorities will be executed first."""
        self.validator_class = validator_class
        self.priority = priority
        self.validator_args = kwargs


class Resource(ABC):
    """Represent an abstract Resource entity."""

    symbol_table = {}

    def build_symbol_table(self, parent_symbol_table):
        for key, value in vars(self).items():
            self.symbol_table[key] = value
        for key, value in vars(self).items():
            self._build_symbol_table(key,value)

    def _build_symbol_table(self, key, value):
        if isinstance(key, Resource):
            symbol_table_cppy = self.symbol_table.copy()
            del symbol_table_cppy[key]  # Prevent self reference
            value.build_symbol_table(symbol_table_cppy)
        elif isinstance(value, List):
            for element in value:
                self._build_symbol_table(key, element)

    class Param:
        """
        Represent a Configuration-managed attribute of a Resource.

        Other than the value of the attribute, it contains metadata information that allows to check if the value is
        implied or not, get the update policy and the default value.
        Instances of this class are not meant to be created directly, but only through the `init_param` utility method
        of resource class.
        """

        def __init__(self, value, default=None, update_policy=None):

            # If the value is None, it means that the value has not been specified in the configuration; hence it can
            # be implied from its default, if present.
            if value is None and default is not None:
                self.__value = default
                self.__implied = True
            else:
                self.__value = value
                self.__implied = False
            self.__default = default
            self.__update_policy = update_policy

        @property
        def value(self):
            """
            Return the value of the parameter.

            This value is always kept in sync with the corresponding resource attribute, so it is always safe to read it
            from here, if needed.
            """
            return self.__value

        @property
        def implied(self):
            """Tell if the value of this parameter is implied or not."""
            return self.__implied

        @property
        def default(self):
            """Return the default value."""
            return self.__default

        @property
        def update_policy(self):
            """Return the update policy."""
            return self.__update_policy()

    def __init__(self):
        # Parameters registry
        self.__params = {}
        self.__validators: List[_ResourceValidator] = []
        self._validation_failures: List[ValidationResult] = []

    @property
    def params(self):
        """Return the params registry for this Resource."""
        return self.__params

    def get_param(self, param_name):
        """Get the information related to the specified parameter name."""
        return self.__params.get(param_name, None)

    def is_implied(self, param_name):
        """Tell if the value of an attribute is implied or not."""
        return self.__params[param_name].implied

    def __setattr__(self, key, value):
        """
        Override the parent __set_attr__ method to manage parameters information related to Resource attributes.

        When an attribute is initialized through the `init_param` method, a Resource.Param instance is associated to
        the attribute and then kept updated accordingly every time the attribute is updated.
        """
        if key != "_Resource__params":
            if isinstance(value, Resource.Param):
                # If value is a param instance, register the Param and replace the value in the attribute
                # Register in params dict
                self.__params[key] = value
                # Set parameter value as attribute value
                value = value.value
            else:
                # If other type, check if it is backed by a param; if yes, sync the param
                param = self.__params.get(key, None)
                if param:
                    param._Param__value = value
                    param._Param__implied = False

        super().__setattr__(key, value)

    @staticmethod
    def init_param(value, default=None, update_policy=None):
        """Create a resource attribute backed by a Configuration Parameter."""
        return Resource.Param(value, default=default, update_policy=update_policy)

    def _register_validators(self):
        """
        Register the validators.

        Method to be implemented in Resources. It will be called before executing the validation.
        """
        pass

    def validate(self, raise_on_error=False):
        """Execute registered validators, ordered by priority (high prio --> executed first)."""
        # Cleanup failures
        self._validation_failures.clear()

        # Call validators for nested resources
        for attr, value in self.__dict__.items():
            if isinstance(value, Resource):
                # Validate nested Resources
                self._validation_failures.extend(value.validate())
            if isinstance(value, list) and value:
                # Validate nested lists of Resources
                for item in self.__getattribute__(attr):
                    if isinstance(item, Resource):
                        self._validation_failures.extend(item.validate())

        # Update validators to be executed according to current status of the model and order by priority
        self.__validators.clear()
        self._register_validators()
        self.__validators = sorted(self.__validators, key=operator.attrgetter("priority"), reverse=True)

        # Execute validators and add results in validation_failures array
        for validator in self.__validators:
            # Execute it by passing all the arguments
            self._validation_failures.extend(
                validator.validator_class(raise_on_error=raise_on_error).execute(**validator.validator_args)
            )

        return self._validation_failures

    def _add_validator(self, validator_class: Validator, priority: int = 1, **kwargs):
        """Store validator to be executed at validation execution."""
        self.__validators.append(_ResourceValidator(validator_class, priority=priority, **kwargs))

    def __repr__(self):
        """Return a human readable representation of the Resource object."""
        return "<{name}({attributes})>".format(
            name=self.__class__.__name__,
            attributes=",".join(f"{attr}={value}" for attr, value in self.__dict__.items()),
        )


# ------------ Common resources between ImageBuilder an Cluster models ----------- #


class BaseTag(Resource):
    """Represent the Tag configuration."""

    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        super().__init__()
        self.key = Resource.init_param(key)
        self.value = Resource.init_param(value)


class Cookbook(Resource):
    """Represent the chef cookbook configuration."""

    def __init__(self, chef_cookbook: str, extra_chef_attributes: str = None):
        super().__init__()
        self.chef_cookbook = Resource.init_param(chef_cookbook)
        self.extra_chef_attributes = Resource.init_param(extra_chef_attributes)
        # TODO: add validator

    def _register_validators(self):
        self._add_validator(UrlValidator, url=self.chef_cookbook)


class BaseDevSettings(Resource):
    """Represent the common dev settings configuration between the ImageBuilder and Cluster."""

    def __init__(
        self,
        cookbook: Cookbook = None,
        node_package: str = None,
        aws_batch_cli_package: str = None,
    ):
        super().__init__()
        self.cookbook = cookbook
        self.node_package = Resource.init_param(node_package)
        self.aws_batch_cli_package = Resource.init_param(aws_batch_cli_package)

    def _register_validators(self):
        self._add_validator(UrlValidator, url=self.node_package)
        self._add_validator(UrlValidator, url=self.aws_batch_cli_package)

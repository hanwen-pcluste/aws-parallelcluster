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
# This module contains all the classes representing the Schema of the configuration file.
# These classes are created by following marshmallow syntax.
#


def efs_existence_of_mode_throughput_validator(throughput_mode, provisioned_throughput):
    errors = []

    if throughput_mode != "provisioned" and provisioned_throughput:
        errors.append("When specifying 'provisioned_throughput', the 'throughput_mode' must be set to 'provisioned'")

    if throughput_mode == "provisioned" and not provisioned_throughput:
        errors.append(
            "When specifying 'throughput_mode' to 'provisioned', the 'provisioned_throughput' option must be specified"
        )

    return errors

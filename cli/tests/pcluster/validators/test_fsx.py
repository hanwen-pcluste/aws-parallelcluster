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
import pytest

from pcluster.schemas.cluster_schema import EbsSchema
from pcluster.validators.common import ConfigValidationError


@pytest.mark.parametrize(
    "section_dict, expected_error",
    [
        (
            {"VolumeType": "io1", "Size": 20, "Iops": 90},
            "IOPS rate must be between 100 and 64000 when provisioning io1 volumes.",
        ),
        (
            {"VolumeType": "io1", "Size": 20, "Iops": 64001},
            "IOPS rate must be between 100 and 64000 when provisioning io1 volumes.",
        ),
        ({"VolumeType": "io1", "Size": 20, "Iops": 1001}, "IOPS to volume size ratio of .* is too high"),
        (
            {"VolumeType": "io2", "Size": 20, "Iops": 90},
            "IOPS rate must be between 100 and 256000 when provisioning io2 volumes.",
        ),
        (
            {"VolumeType": "io2", "Size": 20, "Iops": 256001},
            "IOPS rate must be between 100 and 256000 when provisioning io2 volumes.",
        ),
        (
            {"VolumeType": "io2", "Size": 20, "Iops": 20001},
            "IOPS to volume size ratio of .* is too high",
        ),
        (
            {"VolumeType": "gp3", "Size": 20, "Iops": 2900},
            "IOPS rate must be between 3000 and 16000 when provisioning gp3 volumes.",
        ),
        (
            {"VolumeType": "gp3", "Size": 20, "Iops": 16001},
            "IOPS rate must be between 3000 and 16000 when provisioning gp3 volumes.",
        ),
        (
            {"VolumeType": "gp3", "Size": 20, "Iops": 10001},
            "IOPS to volume size ratio of .* is too high",
        ),
    ],
)
def test_ebs_volume_iops_validator(section_dict, expected_error):
    with pytest.raises(ConfigValidationError, match=expected_error):
        ebs_config = EbsSchema().load(section_dict)
        ebs_config.raise_on_error = True
        ebs_config.validate()

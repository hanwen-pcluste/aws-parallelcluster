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

from pcluster.schemas.cluster_schema import SharedStorageSchema
from tests.pcluster.validators.utils import assert_failure_messages


@pytest.mark.parametrize(
    "section_dict, expected_message",
    [
        ({"VolumeType": "gp3", "Throughput": 125}, None),
        (
            {"VolumeType": "gp3", "Throughput": 100},
            "Throughput must be between 125 MB/s and 1000 MB/s when provisioning gp3 volumes.",
        ),
        (
            {"VolumeType": "gp3", "Throughput": 1001},
            "Throughput must be between 125 MB/s and 1000 MB/s when provisioning gp3 volumes.",
        ),
        ({"VolumeType": "gp3", "Throughput": 125, "Iops": 3000}, None),
        (
            {"VolumeType": "gp3", "Throughput": 760, "Iops": 3000},
            "Throughput to IOPS ratio of .* is too high",
        ),
        ({"VolumeType": "gp3", "Throughput": 760, "Iops": 10000}, None),
        (
            {"VolumeType": "gp3", "Throughput": 1001, "Iops": 2900},
            [
                "IOPS rate must be between 3000 and 16000 when provisioning gp3 volumes.",
                "Throughput must be between 125 MB/s and 1000 MB/s when provisioning gp3 volumes.",
            ],
        ),
    ],
)
def test_ebs_volume_throughput_validator(section_dict, expected_message):
    actual_failures = SharedStorageSchema().load({"MountDir": "/my/mount/point", "EBS": section_dict}).validate()
    assert_failure_messages(actual_failures, expected_message)


@pytest.mark.parametrize(
    "section_dict, expected_message",
    [
        # If size is not valid, validators for iops should not be executed
        ({"VolumeType": "gp2", "Size": 0, "Iops": 120}, "The size of gp2 volumes must be at least 1 GiB"),
        ({"VolumeType": "io1", "Size": 20, "Iops": 120}, None),
        (
            {"VolumeType": "io1", "Size": 20, "Iops": 90},
            "IOPS rate must be between 100 and 64000 when provisioning io1 volumes.",
        ),
        (
            {"VolumeType": "io1", "Size": 20, "Iops": 64001},
            "IOPS rate must be between 100 and 64000 when provisioning io1 volumes.",
        ),
        ({"VolumeType": "io1", "Size": 20, "Iops": 1001}, "IOPS to volume size ratio of .* is too high"),
        ({"VolumeType": "io2", "Size": 20, "Iops": 120}, None),
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
        ({"VolumeType": "gp3", "Size": 20, "Iops": 3000}, None),
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
def test_ebs_size_iops_validators(section_dict, expected_message):
    actual_failures = SharedStorageSchema().load({"MountDir": "/my/mount/point", "EBS": section_dict}).validate()
    assert_failure_messages(actual_failures, expected_message)


@pytest.mark.parametrize(
    "section_dict, expected_message",
    [
        ({"VolumeType": "standard", "Size": 15}, None),
        ({"VolumeType": "standard", "Size": 0}, "The size of standard volumes must be at least 1 GiB"),
        ({"VolumeType": "standard", "Size": 1025}, "The size of standard volumes can not exceed 1024 GiB"),
        ({"VolumeType": "io1", "Size": 15}, None),
        ({"VolumeType": "io1", "Size": 3}, "The size of io1 volumes must be at least 4 GiB"),
        ({"VolumeType": "io1", "Size": 16385}, "The size of io1 volumes can not exceed 16384 GiB"),
        ({"VolumeType": "io2", "Size": 15}, None),
        ({"VolumeType": "io2", "Size": 3}, "The size of io2 volumes must be at least 4 GiB"),
        ({"VolumeType": "io2", "Size": 65537}, "The size of io2 volumes can not exceed 65536 GiB"),
        ({"VolumeType": "gp2", "Size": 15}, None),
        ({"VolumeType": "gp2", "Size": 0}, "The size of gp2 volumes must be at least 1 GiB"),
        ({"VolumeType": "gp2", "Size": 16385}, "The size of gp2 volumes can not exceed 16384 GiB"),
        ({"VolumeType": "gp3", "Size": 15}, None),
        ({"VolumeType": "gp3", "Size": 0}, "The size of gp3 volumes must be at least 1 GiB"),
        ({"VolumeType": "gp3", "Size": 16385}, "The size of gp3 volumes can not exceed 16384 GiB"),
        ({"VolumeType": "st1", "Size": 500}, None),
        ({"VolumeType": "st1", "Size": 20}, "The size of st1 volumes must be at least 500 GiB"),
        ({"VolumeType": "st1", "Size": 16385}, "The size of st1 volumes can not exceed 16384 GiB"),
        ({"VolumeType": "sc1", "Size": 500}, None),
        ({"VolumeType": "sc1", "Size": 20}, "The size of sc1 volumes must be at least 500 GiB"),
        ({"VolumeType": "sc1", "Size": 16385}, "The size of sc1 volumes can not exceed 16384 GiB"),
    ],
)
def test_ebs_volume_type_size_validator(section_dict, expected_message):
    actual_failures = SharedStorageSchema().load({"MountDir": "/my/mount/point", "EBS": section_dict}).validate()
    assert_failure_messages(actual_failures, expected_message)

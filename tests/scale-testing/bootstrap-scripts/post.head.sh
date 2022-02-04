#!/bin/bash
set -ex

# Cluster variables
source /etc/parallelcluster/cfnconfig
SHARED_DIR="$(echo $cfn_ebs_shared_dirs | cut -d ',' -f 1)"

# Inputs
S3_BUCKET_URI=${1-"s3://aws-parallelcluster-mgiacomo/scale-test"}

# Check inputs
if [ -z ${S3_BUCKET_URI} ]; then
  echo "[ERROR] 1st argument S3_BUCKET_URI must not be empty"
  exit 1
fi

# Load libraries
FUNCTIONS_SCRIPT_S3="${S3_BUCKET_URI}/functions.sh"
FUNCTIONS_SCRIPT="${SHARED_DIR}/assets/lib/functions.sh"
mkdir -p $(dirname "${FUNCTIONS_SCRIPT}")
aws s3 cp "${FUNCTIONS_SCRIPT_S3}" "${FUNCTIONS_SCRIPT}"
chmod 755 "${FUNCTIONS_SCRIPT}"
source "${FUNCTIONS_SCRIPT}"

# Download - Init OSU
INIT_OSU_SCRIPT_S3="${S3_BUCKET_URI}/init-osu.sh"
INIT_OSU_SCRIPT="${SHARED_DIR}/assets/workloads/osu/init-osu.sh"
download_asset "${INIT_OSU_SCRIPT_S3}" "${INIT_OSU_SCRIPT}" 755

# Download - Job OSU
JOB_OSU_SCRIPT_S3="${S3_BUCKET_URI}/job-osu.sh"
JOB_OSU_SCRIPT="${SHARED_DIR}/assets/workloads/osu/job-osu.sh"
download_asset "${JOB_OSU_SCRIPT_S3}" "${JOB_OSU_SCRIPT}" 755

# Download - Scale Test Runner
SCALE_TEST_SCRIPT_S3="${S3_BUCKET_URI}/run-scale-test.sh"
SCALE_TEST_SCRIPT="${SHARED_DIR}/assets/workloads/scale-test/run-scale-test.sh"
download_asset "${SCALE_TEST_SCRIPT_S3}" "${SCALE_TEST_SCRIPT}" 755

# Install AWS ParallelCluster
rm -rf aws-parallelcluster
pip3 uninstall -y aws-parallelcluster openapi-spec-validator
git clone https://github.com/aws/aws-parallelcluster.git
pip3 install aws-parallelcluster/cli/

# Metrics publishing
METRICS_PUBLISHER_SCRIPT_S3="${S3_BUCKET_URI}/metrics-publisher.sh"
METRICS_PUBLISHER_SCRIPT="${SHARED_DIR}/assets/monitoring/metrics-publisher.sh"
download_asset "${METRICS_PUBLISHER_SCRIPT_S3}" "${METRICS_PUBLISHER_SCRIPT}" 755
cron_script "* * * * *" "${METRICS_PUBLISHER_SCRIPT}" "${METRICS_PUBLISHER_SCRIPT}.log"

# The command below fails when executed within bootstrap script.
# So, you must run it as root before launching OSU jobs: bash /shared/assets/workloads/osu/init-osu.sh
# unset MODULEPATH
# source /etc/profile.d/modules.sh
# bash ${INIT_OSU_SCRIPT}

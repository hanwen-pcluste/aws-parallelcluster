#!/bin/bash
set -ex

# To submit this job, run:
# sbatch -n 16 /shared/assets/workloads/osu/job-osu.sh [BENCHMARK_NAME] [OUTPUT_DIR]
# sbatch -n 16 /shared/assets/workloads/osu/job-osu.sh osu_alltoall /shared/scale-tests/scale-test-$(date +"%Y-%m-%dT%H-%M-%S")
#
# Note: 16 processes = 4 compute nodes c5.xlarge having 4 vCPUs each

# Cluster variables
source /etc/parallelcluster/cfnconfig
SHARED_DIR="$(echo $cfn_ebs_shared_dirs | cut -d ',' -f 1)"

# Load libraries
FUNCTIONS_SCRIPT="${SHARED_DIR}/assets/lib/functions.sh"
source "${FUNCTIONS_SCRIPT}"

# Input
BENCHMARK_NAME=${1:-"osu_alltoall"}
OUTPUT_DIR=${2:-"${SHARED_DIR}/scale-tests/scale-test-$(timestamp_datetime)"}

# Scale Test - Directories and Files
JOB_METRICS_FILE="${OUTPUT_DIR}/job.${SLURM_JOB_ID}.sample.json"
mkdir -m 777 -p $(dirname ${JOB_METRICS_FILE})

# Scale Test - Instance Info
INSTANCE_ID=$(get_instance_id)
INSTANCE_METRICS_FILE="${SHARED_DIR}/metrics/compute-nodes/instance-${INSTANCE_ID}.json"
for metric in "instancePreInstallTimestamp" "instancePreInstallUpTime" "instancePostInstallTimestamp" "instancePostInstallUpTime" "instanceId"; do
  add_to_json "leaderComputeNode.${metric}" "$(cat ${INSTANCE_METRICS_FILE} | jq -r ".${metric}")" ${JOB_METRICS_FILE}
done
add_to_json "user" $(whoami) ${JOB_METRICS_FILE}

# Scale Test - Job Info
add_to_json "benchmark" ${BENCHMARK_NAME} ${JOB_METRICS_FILE}
add_to_json "processes" ${SLURM_NPROCS} ${JOB_METRICS_FILE}

# Scale Test - Job Start Time
JOB_START_TIME_MILLIS=$(timestamp_millis)
add_to_json "jobStartTimestamp" ${JOB_START_TIME_MILLIS} ${JOB_METRICS_FILE}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Job - OSU Benchmark
MPI_VERSION="openmpi" # or intelmpi

OSU_BENCHMARKS_VERSION="5.7.1"

module load "${MPI_VERSION}"

BENCHMARK_OPTIONS="-m 4096:65536"
BENCHMARK_RESULTS_FILE="${OUTPUT_DIR}/job.${SLURM_JOB_ID}.${BENCHMARK_NAME}.txt"

mpirun -np ${SLURM_NPROCS} "${SHARED_DIR}/${MPI_VERSION}/osu-micro-benchmarks-${OSU_BENCHMARKS_VERSION}/mpi/collective/${BENCHMARK_NAME}" ${BENCHMARK_OPTIONS} > "${BENCHMARK_RESULTS_FILE}"
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Scale Test - Job End Time
JOB_END_TIME_MILLIS=$(timestamp_millis)
add_to_json "jobEndTimestamp" ${JOB_END_TIME_MILLIS} ${JOB_METRICS_FILE}

# Scale Test - OSU Metric
# TODO Currently, we support only the parsing of the results from the benchmark "osu_alltoall"
OSU_METRIC_VALUE=$(tail -n 1 "${BENCHMARK_RESULTS_FILE}" | awk -F'[ ]+' '{print $2}')
add_to_json "osuLatencyMean" ${OSU_METRIC_VALUE} ${JOB_METRICS_FILE}

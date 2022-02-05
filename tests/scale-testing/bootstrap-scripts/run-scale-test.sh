#!/bin/bash
set -e

# Usage: /shared/assets/workloads/scale-test/run-scale-test.sh [BENCHMARK_NAME] [NUM_PROCESSES] [ITERATIONS] [JOB_USER] [OUTPUT_DIR] [OUTPUT_S3_URI]
# Usage: /shared/assets/workloads/scale-test/run-scale-test.sh osu_alltoall 16 3 ec2-user /shared/scale-tests/scale-test-$(date +"%Y-%m-%dT%H-%M-%S") s3://aws-parallelcluster-mgiacomo/scale-test/out

# Cluster variables
source /etc/parallelcluster/cfnconfig
CLUSTER_NAME="${stack_name}"
AWS_DEFAULT_REGION="${cfn_region}"
SHARED_DIR="$(echo $cfn_ebs_shared_dirs | cut -d ',' -f 1)"

# Load libraries
FUNCTIONS_SCRIPT="${SHARED_DIR}/assets/lib/functions.sh"
source "${FUNCTIONS_SCRIPT}"

# Functions
function launch_job () {
  local job_script=$1
  local benchmark_name=$2
  local num_processes=$3
  local job_user=$4
  local output_dir=$5
  local sbatch_result=$(sudo -u ${job_user} -i sbatch -n ${num_processes} "${job_script}" ${benchmark_name} ${output_dir})
  local submission_line=$(echo $sbatch_result | grep "Submitted batch job")
  if [[ -z $submission_line ]]; then
    log_error "Job submission failed";
    exit 1
  fi
  local job_id=$(echo $submission_line | cut -d ' ' -f 4)
  echo $job_id
}

# Input
BENCHMARK_NAME=${1:-"osu_alltoall"}
NUM_PROCESSES=${2:-16}
MAX_ITERATIONS=${3:-3}
JOB_USER=${4:-$(whoami)}
OUTPUT_DIR=${5:-"${SHARED_DIR}/scale-tests/${CLUSTER_NAME}-$(timestamp_datetime)"}
OUTPUT_S3=${6}

# Job Details
JOB_SCRIPT="${SHARED_DIR}/assets/workloads/osu/job-osu.sh"

# Print Info
echo "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"
echo "# SCALE TEST"
echo "# - Benchmark: ${BENCHMARK_NAME}"
echo "# - Processes: ${NUM_PROCESSES}"
echo "# - Iterations: ${MAX_ITERATIONS}"
echo "# - Job User: ${JOB_USER}"
echo "# - Job Script: ${JOB_SCRIPT}"
echo "# - Test Output: ${OUTPUT_DIR}"
echo "# - Test Output S3: ${OUTPUT_S3}"
echo "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"

# Init
for iteration in $(seq 1 ${MAX_ITERATIONS}); do
  log "Executing iteration ${iteration}/${MAX_ITERATIONS}"

  log "Terminating compute fleet"
  terminate_compute_fleet ${CLUSTER_NAME} ${AWS_DEFAULT_REGION}

  log "Waiting for compute fleet down to 0 nodes (can take up to the configured idle scale-down time, default 10 minutes)"
  wait_compute_fleet ${CLUSTER_NAME} ${AWS_DEFAULT_REGION} 0 120

  # Job Launch
  JOB_ID=$(launch_job "${JOB_SCRIPT}" "${BENCHMARK_NAME}" "${NUM_PROCESSES}" "${JOB_USER}" "${OUTPUT_DIR}")
  JOB_SUBMISSION_TIME_MILLIS=$(timestamp_millis)
  JOB_METRICS_FILE="${OUTPUT_DIR}/job.${JOB_ID}.sample.json"
  mkdir -m 777 -p $(dirname ${JOB_METRICS_FILE})
  echo "{}" > ${JOB_METRICS_FILE}
  chmod 666 ${JOB_METRICS_FILE}

  log "Job ${JOB_ID} submitted at $(millis_to_date_time ${JOB_SUBMISSION_TIME_MILLIS}); metrics will be collected in ${JOB_METRICS_FILE}"
  add_to_json "jobId" ${JOB_ID} ${JOB_METRICS_FILE}
  add_to_json "jobSubmissionTimestamp" ${JOB_SUBMISSION_TIME_MILLIS} ${JOB_METRICS_FILE}

  # Waiting Job Completion
  log "Waiting for job completion"
  wait_job_completion ${JOB_ID} 120

  # Compute Nodes Sample
  # instancePreInstallTimestamp, instancePreInstallUpTime, instancePostInstallTimestamp, instancePostInstallUpTime
  COMPUTE_NODES_SAMPLE_FILE="${OUTPUT_DIR}/compute-nodes.${JOB_ID}.sample.json"
  COMPUTE_NODES_METRICS_DIR="${SHARED_DIR}/metrics/compute-nodes"
  COMPUTE_NODES_METRICS_FILES=$(find ${COMPUTE_NODES_METRICS_DIR} -type f -name "instance-*.json")
  for metric in "instancePreInstallTimestamp" "instancePreInstallUpTime" "instancePostInstallTimestamp" "instancePostInstallUpTime"; do
    add_to_json "${metric}Sample" $(get_sample_from_json "${metric}" "${COMPUTE_NODES_METRICS_FILES}") ${COMPUTE_NODES_SAMPLE_FILE}
  done

  # Compute Nodes metrics
  # firstComputeNode timings, i.e. time metrics from the first launched compute node
  FIRST_COMPUTE_NODE_METRICS=$(get_json_with_minimum "instancePreInstallTimestamp" "${COMPUTE_NODES_METRICS_FILES}")
  for metric in "instancePreInstallTimestamp" "instancePreInstallUpTime" "instancePostInstallTimestamp" "instancePostInstallUpTime" "instanceId"; do
    add_to_json "firstComputeNode.${metric}" "$(echo ${FIRST_COMPUTE_NODE_METRICS} | jq -r ".${metric}")" ${JOB_METRICS_FILE}
  done
  # lastComputeNode timings, i.e. time metrics from the last launched compute node
  LAST_COMPUTE_NODE_METRICS=$(get_json_with_maximum "instancePreInstallTimestamp" "${COMPUTE_NODES_METRICS_FILES}")
  for metric in "instancePreInstallTimestamp" "instancePreInstallUpTime" "instancePostInstallTimestamp" "instancePostInstallUpTime" "instanceId"; do
    add_to_json "lastComputeNode.${metric}" "$(echo ${LAST_COMPUTE_NODE_METRICS} | jq -r ".${metric}")" ${JOB_METRICS_FILE}
  done

  # Derived Metrics: jobRunTime = jobEndTimestamp - jobStartTimestamp
  JOB_RUN_TIME_MILLIS=$(cat ${JOB_METRICS_FILE} | jq '(.jobEndTimestamp|tonumber) - (.jobStartTimestamp|tonumber)')
  add_to_json "jobRunTime" ${JOB_RUN_TIME_MILLIS} ${JOB_METRICS_FILE}

  # Derived Metrics: jobWaitingTime = jobStartTimestamp - jobSubmissionTimestamp
  JOB_WAITING_TIME_MILLIS=$(cat ${JOB_METRICS_FILE} | jq '(.jobStartTimestamp|tonumber) - (.jobSubmissionTimestamp|tonumber)')
  add_to_json "jobWaitingTime" ${JOB_WAITING_TIME_MILLIS} ${JOB_METRICS_FILE}

  # Derived Metrics: jobWarmupLeaderNodeTime = jobStartTimestamp - leaderComputeNode.instancePreInstallTimestamp
  JOB_WARMUP_LEADER_NODE_TIME_MILLIS=$(cat ${JOB_METRICS_FILE} | jq '(.jobStartTimestamp|tonumber) - (.leaderComputeNode.instancePreInstallTimestamp|tonumber)')
  add_to_json "jobWarmupLeaderNodeTime" ${JOB_WARMUP_LEADER_NODE_TIME_MILLIS} ${JOB_METRICS_FILE}

  # Derived Metrics: jobWarmupFirstNodeTime = jobStartTimestamp - firstComputeNode.instancePreInstallTimestamp
  JOB_WARMUP_FIRST_NODE_TIME_MILLIS=$(cat ${JOB_METRICS_FILE} | jq '(.jobStartTimestamp|tonumber) - (.firstComputeNode.instancePreInstallTimestamp|tonumber)')
  add_to_json "jobWarmupFirstNodeTime" ${JOB_WARMUP_FIRST_NODE_TIME_MILLIS} ${JOB_METRICS_FILE}

  # Derived Metrics: jobWarmupLastNodeTime = jobStartTimestamp - lastComputeNode.instancePreInstallTimestamp
  JOB_WARMUP_LAST_NODE_TIME_MILLIS=$(cat ${JOB_METRICS_FILE} | jq '(.jobStartTimestamp|tonumber) - (.lastComputeNode.instancePreInstallTimestamp|tonumber)')
  add_to_json "jobWarmupLastNodeTime" ${JOB_WARMUP_LAST_NODE_TIME_MILLIS} ${JOB_METRICS_FILE}

  # Cleanup
  rm -rf ${COMPUTE_NODES_METRICS_FILES}

  # Finalize
  log "Iteration ${iteration}/${MAX_ITERATIONS} completed: job metrics in ${JOB_METRICS_FILE}"
  log "Waiting 60 seconds before the next iteration"
  sleep 60
  log "Terminating compute fleet"
  terminate_compute_fleet ${CLUSTER_NAME} ${AWS_DEFAULT_REGION}
done

# Samples
log "Generating samples"
SAMPLES_FILE="${OUTPUT_DIR}/samples.json"
JOBS_SAMPLE_FILES=$(find ${OUTPUT_DIR} -type f -name "job.*.sample.json")
for metric in "jobRunTime" "jobWaitingTime" "jobWarmupLeaderNodeTime" "jobWarmupFirstNodeTime" "jobWarmupLastNodeTime"; do
  add_to_json "${metric}Sample" $(get_sample_from_json "${metric}" "${JOBS_SAMPLE_FILES}") ${SAMPLES_FILE}
done
COMPUTE_NODES_SAMPLE_FILES=$(find ${OUTPUT_DIR} -type f -name "compute-nodes.*.sample.json")
for metric in "instancePreInstallTimestamp" "instancePreInstallUpTime" "instancePostInstallTimestamp" "instancePostInstallUpTime"; do
  add_to_json "${metric}Sample" $(get_sample_from_json "${metric}Sample" "${COMPUTE_NODES_SAMPLE_FILES}") ${SAMPLES_FILE}
done

# Statistics
log "Generating statistics"
STATISTICS_FILE="${OUTPUT_DIR}/statistics.json"
for metric in "jobRunTime" "jobWaitingTime" "jobWarmupLeaderNodeTime" "jobWarmupFirstNodeTime" "jobWarmupLastNodeTime"; do
  add_to_json "${metric}.min" $(get_min "$(cat ${SAMPLES_FILE} | jq -r ".${metric}Sample")") ${STATISTICS_FILE}
  add_to_json "${metric}.max" $(get_max "$(cat ${SAMPLES_FILE} | jq -r ".${metric}Sample")") ${STATISTICS_FILE}
  add_to_json "${metric}.avg" $(get_avg "$(cat ${SAMPLES_FILE} | jq -r ".${metric}Sample")") ${STATISTICS_FILE}
  add_to_json "${metric}.std" $(get_std "$(cat ${SAMPLES_FILE} | jq -r ".${metric}Sample")") ${STATISTICS_FILE}
done

# Upload samples and statistics on S3
if [[ -z ${OUTPUT_S3} ]]; then
  log "Skipping upload on S3 as no OUTPUT_S3 has been specified"
else
  aws s3 sync ${OUTPUT_DIR} "${OUTPUT_S3}/"
fi

# End
log "Scale test completed: samples in ${SAMPLES_FILE}, statistics in ${STATISTICS_FILE}"

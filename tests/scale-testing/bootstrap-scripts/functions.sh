#!/bin/bash

function log () {
  echo "$(date +"%Y-%m-%dT%H-%M-%S") [INFO] $1"
}

function log_error () {
  echo "$(date +"%Y-%m-%dT%H-%M-%S") [ERROR] $1"
}

function fail () {
  echo "$(date +"%Y-%m-%dT%H-%M-%S") [ERROR] $1"
  exit 1
}

function download_asset () {
  local S3_URI="$1"
  local LOCAL_FILE="$2"
  local PERMISSIONS="$3"
  mkdir -p $(dirname "${LOCAL_FILE}")
  aws s3 cp "${S3_URI}" "${LOCAL_FILE}"
  chmod ${PERMISSIONS} "${LOCAL_FILE}"
}

function cron_script () {
  local CRON_EXPRESSION="$1"
  local SCRIPT="$2"
  local LOG="$3"
  echo "${CRON_EXPRESSION} ${SCRIPT} > ${LOG} 2>&1" >> "/var/spool/cron/$(whoami)"
}

function timestamp_millis () {
  date +"%s%3N"
}

function timestamp_datetime () {
  date +"%Y-%m-%dT%H-%M-%S"
}

function millis_to_date_time () {
  date -d @${1::-3} +"%Y-%m-%dT%H-%M-%S"
}

function date_time_to_millis () {
  date -d ${1} +"%Y-%m-%dT%H-%M-%S"
}

function get_instance_id () {
  local imds_endpoint="http://169.254.169.254/latest"
  local imds_token=$(curl -X PUT "${imds_endpoint}/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" 2>/dev/null)
  curl -H "aws-ec2-metadata-token: ${imds_token}" "${imds_endpoint}/meta-data/instance-id" 2>/dev/null
}

function wait_job_completion () {
  local job_id=$1
  local sleep_seconds=$2
  local expected_jobs_in_queue=0
  while true; do
    local jobs_in_queue=$(/opt/slurm/bin/squeue -h -j${job_id} | wc -l)
    log "Current jobs running: ${jobs_in_queue}. Expected jobs running: ${expected_jobs_in_queue}"
    [ ${jobs_in_queue} == ${expected_jobs_in_queue} ] && break
    log "Sleeping ${sleep_seconds} seconds"
    sleep ${sleep_seconds}
  done
}

function get_compute_fleet_running_nodes () {
  local cluster_name=$1
  local region=$2
  /usr/local/bin/pcluster describe-cluster-instances --region ${region} --cluster-name "${cluster_name}" --query 'instances[].nodeType'  | grep -o ComputeNode  | wc -l
}

function terminate_compute_fleet () {
    local cluster_name=$1
    local region=$2
    /usr/local/bin/pcluster delete-cluster-instances --region ${region} --cluster-name "${cluster_name}" --force true
}

function wait_compute_fleet () {
  local cluster_name=$1
  local region=$2
  local expected_compute_nodes=$3
  local sleep_seconds=$4
  while true; do
    local compute_nodes=$(get_compute_fleet_running_nodes ${cluster_name} ${region})
    log "Current compute nodes ${compute_nodes}. Expected compute nodes ${expected_compute_nodes}."
    [ ${compute_nodes} == ${expected_compute_nodes} ] && break
    log "Sleeping ${sleep_seconds} seconds"
    sleep ${sleep_seconds}
  done
}

function add_to_json () {
  local key=$1
  local value=$2
  local json_file=$3

  [[ ! -f ${json_file} ]] && echo "{}" > ${json_file}
  echo $(jq ".${key} = \"${value}\"" ${json_file}) > ${json_file}
}

function merge_json () {
  local json_file_1=$1
  local json_file_2=$2
  local json_file_3=$3
  echo $(jq --argfile f1 "${json_file_1}" --argfile f2 "${json_file_2}" -n '$f1 * $f2') > "${json_file_3}"
}

function get_sample_from_json () {
  local key="$1"
  local files="$2"
  jq -n "[inputs.${key}]" ${files} | jq -r -c 'join(",")'
}

function get_json_with_minimum () {
  local key="$1"
  local files="$2"
  jq -n "[inputs] | sort_by(.${key}) | .[0]" ${files}
}

function get_json_with_maximum () {
  local key="$1"
  local files="$2"
  jq -n "[inputs] | sort_by(.${key}) | .[-1]" ${files}
}

function get_min () {
  python3 -c "print(min([${1}]))"
}

function get_max () {
  python3 -c "print(max([${1}]))"
}

function get_avg () {
  python3 -c "from statistics import mean;print(mean([${1}]))"
}

function get_std () {
  python3 -c "from statistics import stdev;print(stdev([${1}]))"
}

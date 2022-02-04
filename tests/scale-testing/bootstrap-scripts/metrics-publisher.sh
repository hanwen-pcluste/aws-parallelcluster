#!/bin/bash
set -e

# Cluster variables
source /etc/parallelcluster/cfnconfig
CLUSTER_NAME="${stack_name:?}"
AWS_DEFAULT_REGION="${cfn_region:?}"

CW_NAMESPACE="ParallelCluster/ScaleTesting/AdIntegration"
PCLUSTER="/usr/local/bin/pcluster"
SQUEUE="/opt/slurm/bin/squeue"

echo "$(date) [INFO] Publishing metrics for cluster ${CLUSTER_NAME} in region ${AWS_DEFAULT_REGION} to CloudWatch namespace ${CW_NAMESPACE}"

NUM_COMPUTE_NODES=$(${PCLUSTER} describe-cluster-instances --region ${AWS_DEFAULT_REGION} --cluster-name "$CLUSTER_NAME" --query 'instances[].nodeType'  | grep -o ComputeNode  | wc -l)
aws cloudwatch put-metric-data \
    --region "${AWS_DEFAULT_REGION}" \
    --namespace "${CW_NAMESPACE}" \
    --metric-name "ComputeNodeCount" \
    --dimensions "ClusterName=${CLUSTER_NAME}" \
    --value "${NUM_COMPUTE_NODES}"

NUM_JOBS_QUEUED=$(${SQUEUE} -h | wc -l)
aws cloudwatch put-metric-data \
    --region "${AWS_DEFAULT_REGION}" \
    --namespace "${CW_NAMESPACE}" \
    --metric-name "JobsQueuedCount" \
    --dimensions "ClusterName=${CLUSTER_NAME}" \
    --value "${NUM_JOBS_QUEUED}"

NUM_JOBS_PENDING=$(${SQUEUE} -h -t configuring,pending | wc -l)
aws cloudwatch put-metric-data \
    --region "${AWS_DEFAULT_REGION}" \
    --namespace "${CW_NAMESPACE}" \
    --metric-name "JobsPendingCount" \
    --dimensions "ClusterName=${CLUSTER_NAME}" \
    --value "${NUM_JOBS_PENDING}"

NUM_JOBS_RUNNING=$(${SQUEUE} -h -t running | wc -l)
aws cloudwatch put-metric-data \
    --region "${AWS_DEFAULT_REGION}" \
    --namespace "${CW_NAMESPACE}" \
    --metric-name "JobsRunningCount" \
    --dimensions "ClusterName=${CLUSTER_NAME}" \
    --value "${NUM_JOBS_RUNNING}"

NUM_JOBS_FAILED=$(${SQUEUE} -h -t failed | wc -l)
aws cloudwatch put-metric-data \
    --region "${AWS_DEFAULT_REGION}" \
    --namespace "${CW_NAMESPACE}" \
    --metric-name "JobsFailedCount" \
    --dimensions "ClusterName=${CLUSTER_NAME}" \
    --value "${NUM_JOBS_FAILED}"

echo "$(date) [INFO] Published metrics for cluster ${CLUSTER_NAME} in region ${AWS_DEFAULT_REGION} to CloudWatch namespace ${CW_NAMESPACE}"

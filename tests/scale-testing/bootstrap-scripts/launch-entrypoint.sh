NAME={{ name }}
NUM_NODES={{ num_nodes }}
DIRECTORY_TYPE={{ directory_type }}
NUM_VCPUS=4 # constant, depending on compute node instance type, e.g. c5.xlarge has 4 vcpusNUM_PROCESSES=$(( ${NUM_NODES} * ${NUM_VCPUS} ))
NUM_ITERATIONS=3
JOB_USER={{ job_user }} # "PclusterUser1" # can be ec2-user or a directory user
BENCHMARK="osu_alltoall" # currently supported only osu_alltoall
OUTPUT_DIR="/ebs/scale-tests/${NAME}/${NUM_NODES}nodes/${DIRECTORY_TYPE}"
OUTPUT_S3="s3://aws-parallelcluster-dev-hanwenli-scalingtest/results/${NAME}/${NUM_NODES}nodes/${DIRECTORY_TYPE}"
NUM_PROCESSES=$(( $NUM_NODES * $NUM_VCPUS ))

bash -x /ebs/assets/workloads/scale-test/run-scale-test.sh ${BENCHMARK} ${NUM_PROCESSES} ${NUM_ITERATIONS} ${JOB_USER} ${OUTPUT_DIR} ${OUTPUT_S3}

# Retrieve output
cat ${OUTPUT_DIR}/statistics.json
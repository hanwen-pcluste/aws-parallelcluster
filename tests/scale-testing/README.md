# Scale Testing

## Content
1. bootstrap-scripts: this folder contains bootstrap scripts for head/compute nodes and auxiliary scripts used for the scale test
1. cluster-config: this folder contains a set of cluster configurations
1. plotting: this folder contains the scripts used to generate plots from data

## Usage

### Step 1 - Launch a scale test
From within the head node:
```
NAME="baseline"
BENCHMARK="osu_alltoall"
NUM_NODES=4
NUM_VCPUS=4 # constant, depending on compute node instance type, e.g. c5.xlarge has 4 vcpus
NUM_PROCESSES=$(( ${NUM_NODES} * ${NUM_VCPUS} ))
NUM_ITERATIONS=3
OUTPUT_DIR=/shared/scale-tests/${NAME}/${NUM_NODES}nodes
OUTPUT_S3="s3://aws-parallelcluster-mgiacomo/experiments/scale-test/${NAME}/${NUM_NODES}nodes"

bash /shared/assets/workloads/scale-test/run-scale-test.sh ${BENCHMARK} ${NUM_PROCESSES} ${NUM_ITERATIONS} ${OUTPUT_DIR} ${OUTPUT_S3}

# Retrieve local output
cat ${OUTPUT_DIR}/samples.json
cat ${OUTPUT_DIR}/statistics.json
```

### Step 2 - Download scale test results from S3
```
DATA_ON_S3="s3://${S3_BUCKET}/experiments/scale-test/"
LOCAL_PATH="/Users/mgiacomo/workplace/aws-parallelcluster-notes/experiments/scale-test"

aws s3 sync ${DATA_ON_S3} ${LOCAL_PATH}
```

### Step 3 - Generate plots from data
```
DATA_DIR="/Users/mgiacomo/workplace/aws-parallelcluster-notes/experiments/scale-test"
PLOTS_DIR="${DATA_DIR}/plots"
python3 create-scale-test-plots.py --datadir ${DATA_DIR} --outdir ${PLOTS_DIR}
```

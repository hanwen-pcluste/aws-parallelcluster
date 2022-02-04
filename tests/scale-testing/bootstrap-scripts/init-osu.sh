#!/bin/bash
set -e

source /etc/parallelcluster/cfnconfig

SHARED_DIR="$(echo $cfn_ebs_shared_dirs | cut -d ',' -f 1)"

MPI_VERSION="openmpi" # or intelmpi

OSU_BENCHMARKS_VERSION="5.7.1"
OSU_BENCHMARKS_PACKAGE_NAME="osu-micro-benchmarks-${OSU_BENCHMARKS_VERSION}"

module load "${MPI_VERSION}"
mkdir -p "${SHARED_DIR}/${MPI_VERSION}"

wget --no-check-certificate http://mvapich.cse.ohio-state.edu/download/mvapich/${OSU_BENCHMARKS_PACKAGE_NAME}.tgz
cp "./${OSU_BENCHMARKS_PACKAGE_NAME}.tgz" "${SHARED_DIR}/${MPI_VERSION}"
cd "${SHARED_DIR}/${MPI_VERSION}"
tar zxvf "./${OSU_BENCHMARKS_PACKAGE_NAME}.tgz"

# Update config.guess and config.sub files to support ARM architecture.
#cd
#cp "./config.guess" "/shared/${MPI_VERSION}/${OSU_BENCHMARKS_PACKAGE_NAME}/"
#cp "./config.sub" "/shared/${MPI_VERSION}/${OSU_BENCHMARKS_PACKAGE_NAME}/"

# Compile OSU benchmarks
cd "${SHARED_DIR}/${MPI_VERSION}/${OSU_BENCHMARKS_PACKAGE_NAME}"
./configure CC=$(which mpicc) CXX=$(which mpicxx)
make

#!/bin/bash

set -ex

./launch_functions.sh deploy

# 1.autheticate
pushd ./1.authenticate/
./run_bench.sh 20 $1_20_authenticate
../stats.py $1_20_authenticate > $1_20_authenticate_results
cp $1_20_authenticate_results $2
popd

# 2.getPrice
pushd ./2.getPrice/
./run_bench.sh 20 $1_20_getPrice
../stats.py $1_20_getPrice > $1_20_getPrice_results
cp $1_20_getPrice_results $2
popd

# 3.authorize-cc
pushd ./3.authorize-cc/
./run_bench.sh 20 $1_20_authorize-cc
../stats.py $1_20_authorize-cc > $1_20_authorize-cc_results
cp $1_20_authorize-cc_results $2
popd

# 4.publish
pushd ./4.publish/
./run_bench.sh 20 $1_20_publish
../stats.py $1_20_publish > $1_20_publish_results
cp $1_20_publish_results $2
popd

./launch_functions.sh remove

#!/bin/bash

set -ex

./launch_functions.sh deploy

# $2 is the results dir
# $1 is the runtime: gvisor, kalium
# 1.assign
pushd ./1.assign/
./run_bench.sh 20 $1_20_assign
../stats.py $1_20_assign > $1_20_assign_results
cp $1_20_assign_results $2
popd

# 1.microbench
pushd ./1.microbench/
./run_bench.sh 20 $1_20_microbench
../stats.py $1_20_microbench > $1_20_microbench_results
cp $1_20_microbench_results $2
popd

# 2.message
pushd ./2.message/
./run_bench.sh 20 $1_20_message
../stats.py $1_20_message > $1_20_message_results
cp $1_20_message_results $2
popd

# 2.record
pushd ./2.record/
./run_bench.sh 20 $1_20_record
../stats.py $1_20_record > $1_20_record_results
cp $1_20_record_results $2
popd

# 3.receive
pushd ./3.receive/
./run_bench.sh 20 $1_20_receive
../stats.py $1_20_receive > $1_20_receive_results
cp $1_20_receive_results $2
popd

# 4.success
pushd ./4.success/
./run_bench.sh 20 $1_20_success
../stats.py $1_20_success > $1_20_success_results
cp $1_20_success_results $2
popd

# 6.report
pushd ./6.report/
./run_bench.sh 20 $1_20_report
../stats.py $1_20_report > $1_20_report_results
cp $1_20_report_results $2
popd

# master-photos
pushd ./master/
./run_bench_photos.sh 20 $1_20_masterPhotos
../stats.py $1_20_masterPhotos > $1_20_masterPhotos_results
cp $1_20_masterPhotos_results $2
popd

# master-receive
pushd ./master/
./run_bench_request.sh 20 $1_20_masterReceive
../stats.py $1_20_masterReceive > $1_20_masterReceive_results
cp $1_20_masterReceive_results $2
popd

./launch_functions.sh remove


#!/bin/bash

#set -ex

#./launch_functions.sh deploy

# 1.assign
pushd ./1.assign/
rm -f trapeze_20_assign_results
popd

# 1.microbench
pushd ./1.microbench/
rm -f trapeze_20_microbench_results
popd

# 2.message
pushd ./2.message/
#./run_bench.sh 20 trapeze_20_message
rm -f trapeze_20_message_results
popd

# 2.record
pushd ./2.record/
rm -f trapeze_20_record_results
popd

# 3.receive
pushd ./3.receive/
rm -f trapeze_20_receive_results
popd

# 4.success
pushd ./4.success/
rm -f trapeze_20_success_results
popd

# 6.report
pushd ./6.report/
rm -f trapeze_20_report_results
popd

# master-photos
pushd ./master/
rm -f trapeze_20_masterPhotos_results
popd

# master-receive
pushd ./master/
#./run_bench_receive.sh 20 trapeze_20_masterReceive
rm -f trapeze_20_masterReceive_results
popd

#./launch_functions.sh remove


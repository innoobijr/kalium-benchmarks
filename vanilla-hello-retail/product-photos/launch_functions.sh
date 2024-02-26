#!/bin/bash

set -ex

pushd ./1.assign/
faas-cli $1 -f product-photos-1-assign.yml --gateway $HOSTNAME:31112
popd

pushd ./1.microbench/
faas-cli $1 -f product-photos-1-microbench_seclambda.yml --gateway $HOSTNAME:31112
popd

pushd ./2.message/
faas-cli $1 -f product-photos-2-message.yml --gateway $HOSTNAME:31112
popd

pushd ./2.record/
faas-cli $1 -f product-photos-2-record.yml --gateway $HOSTNAME:31112
popd

pushd ./3.receive/
faas-cli $1 -f product-photos-3-receive.yml --gateway $HOSTNAME:31112
popd

pushd ./4.success/
faas-cli $1 -f product-photos-4-success.yml --gateway $HOSTNAME:31112
popd

pushd ./6.report/
faas-cli $1 -f product-photos-6-report.yml --gateway $HOSTNAME:31112
popd

pushd ./master/
faas-cli $1 -f master.yml --gateway $HOSTNAME:31112
popd

sleep 70

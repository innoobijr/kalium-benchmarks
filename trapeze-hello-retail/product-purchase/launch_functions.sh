#!/bin/bash

set -ex

pushd ./1.authenticate/
faas-cli $1 -f 1authenticate.yml --gateway $HOSTNAME:31112
popd

pushd ./2.getPrice/
faas-cli $1 -f product-purchase-2-get-price.yml --gateway $HOSTNAME:31112
popd

pushd ./3.authorize-cc/
faas-cli $1 -f product-purchase-authorize-cc.yml --gateway $HOSTNAME:31112
popd

pushd ./4.publish/
faas-cli $1 -f product-purchase-4-publish.yml --gateway $HOSTNAME:31112
popd

sleep 70

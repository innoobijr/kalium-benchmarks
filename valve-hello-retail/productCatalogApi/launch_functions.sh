#!/bin/bash

set -ex

pushd ./api/
faas-cli $1 -f product-catalog-api.yml --gateway $HOSTNAME:31112
popd

pushd ./builder/
faas-cli $1 -f product-catalog-builder.yml --gateway $HOSTNAME:31112
popd

sleep 70

#!/bin/bash

mkdir -p results_$1

dir=$(pwd)
pushd ./productCatalogApi
./run_bench.sh $1 $dir/results_$1
popd

pushd ./product-photos
./run_bench.sh $1 $dir/results_$1
popd

pushd ./product-purchase
./run_bench.sh $1 $dir/results_$1
popd



#!/bin/bash

set -ex

./launch_functions.sh deploy
# $2 is the results dir
# $1 is the name of the runtime: gvisor, kalium
pushd ./api
./run_bench.sh 20 $1
../stats.py $1_20_api_products > $1_20_api_products_results
../stats.py $1_20_api_categories > $1_20_api_categories_results
cp $1_20_api_categories_results $2
cp $1_20_api_products_results $2
popd

pushd ./builder
./run_bench.sh 20 $1
../stats.py $1_20_builder_product > $1_20_builder_product_results
../stats.py $1_20_builder_photo > $1_20_builder_photo_results
cp $1_20_builder_photo_results $2
cp $1_20_builder_product_results $2
popd

./launch_functions.sh remove

#!/bin/bash
NUM_ITER=$1

function usage() {
	echo "./run_bench.sh <num_iter> <outfile>"
}

if [ -z "$1" ] || [ -z "$2" ]; then
	usage
	exit
fi

./run_bench-product.sh $1 $2_$1_builder_product
./run_bench-photo.sh $1 $2_$1_builder_photo

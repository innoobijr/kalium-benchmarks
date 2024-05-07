#!/bin/bash
NUM_ITER=$1

function usage() {
	echo "./run_bench.sh <num_iter> <outfile>"
}

if [ -z "$1" ] || [ -z "$2" ]; then
	usage
	exit
fi

counter=0
while [ $counter -lt $NUM_ITER ]
do
	curl -d @sample-input.json -w "@curl-format_total.txt" -H "Content-Type: application/json" -X POST "http://127.0.0.1:8080/function/trapeze-product-photos-2-record" -m 6 -o /dev/null >> $2
	counter=$((counter + 1))
done

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
	curl -d @sample-input_localurl.json -w "@curl-format_total.txt" -H "Content-Type: application/json" -X POST "http://$HOSTNAME:31112/function/valve-product-photos-3-receive" -o /dev/null >> $2
	counter=$((counter + 1))
done

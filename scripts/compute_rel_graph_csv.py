#!/usr/bin/python3

# Computes the necessary csv files needed for plotting the relative latency graph
# Inputs: Result dirs of running the benchmarks
# Output: seclats.csv, trapezelats.csv, valvelats.csv
# seclats.csv, trapezelats.csv, valvelats.csv can be plugged into the graphing latex project to generate the final graphs

import sys
import os

benchmarks = ['microbenchmark', 'product-photos-receive', 'product-master-photos', 'product-master-request', 'product-photos-assign', 'product-photos-message',
              'product-photos-record', 'product-photos-success', 'product-photos-report', 'product-purchase-authenticate', 'product-purchase-getprice',
              'product-purchase-authorize-cc', 'product-purchase-publish', 'product-catalog-api-categories', 'product-catalog-api-products', 'product-catalog-builder-image',
              'product-catalog-builder-product']

has_star = ['microbenchmark', 'product-photos-receive', 'product-master-photos']
file_to_bench = {
        #product-photos
        'assign':'product-photos-assign',
        'microbench': 'microbenchmark',
        'message': 'product-photos-message',
        'record': 'product-photos-record',
        'receive': 'product-photos-receive',
        'success': 'product-photos-success',
        'report': 'product-photos-report',
        'masterPhotos': 'product-master-photos',
        'masterReceive': 'product-master-request',
        #product-purchase
        'authenticate': 'product-purchase-authenticate',
        'getPrice': 'product-purchase-getprice',
        'authorize-cc': 'product-purchase-authorize-cc',
        'publish': 'product-purchase-publish',
        #productCatalogApi
        'api_categories': 'product-catalog-api-categories',
        'api_products': 'product-catalog-api-products',
        'builder_photo': 'product-catalog-builder-image',
        'builder_product': 'product-catalog-builder-product'
}


def usage():
    print ("python3 compute_rel_graph_csv.py <vanilla_results_kalium_dir> <vanilla_results_gvisor_dir> <valve_results_gvisor_dir> <trapeze_results_gvisor_dir>")
    exit(1)

def create_csv(fname, benchmark_dict):
    f = open(fname, "w")
    print (benchmark_dict)
    f.write("name, mean\n")

    for benchmark in benchmarks:
        if benchmark in benchmark_dict:
            if benchmark in has_star:
                f.write(benchmark + "*"+ "," + str(benchmark_dict[benchmark][0]) + "\n")
            else:
                f.write(benchmark + "," + str(benchmark_dict[benchmark][0]) + "\n")
    f.close()

def main():
    if len(sys.argv) != 5:
        usage()

    vanilla_results_kalium_dir = os.fsencode(sys.argv[1])
    vanilla_results_gvisor_dir = os.fsencode(sys.argv[2])
    valve_results_gvisor_dir = os.fsencode(sys.argv[3])
    trapeze_results_gvisor_dir = os.fsencode(sys.argv[4])

    vanilla_results_gvisor = {}
    vanilla_results_kalium = {}
    valve_results_gvisor = {}
    trapeze_results_gvisor = {}

    #TODO: Add assertions about runtime name
    for file in os.listdir(vanilla_results_kalium_dir):
        filename = os.fsencode(file).decode('utf-8')
        #print (filename)
        s = filename.split('_')
        bench_name = '_'.join(s[2:len(s)-1])
        runtime_name = s[0]
        assert(runtime_name == "kalium")

        #print (filename, bench_name)
        f = open(os.path.join(vanilla_results_kalium_dir, file), 'r')
        for line in f.readlines():
            avg = float(line.strip().split(',')[0].strip().split(':')[1].strip())
            stdev = float(line.strip().split(',')[1].strip().split(':')[1].strip())
            vanilla_results_kalium[file_to_bench[bench_name]] = (avg, stdev)
            break

    for file in os.listdir(valve_results_gvisor_dir):
        filename = os.fsencode(file).decode('utf-8')
        #print (filename)
        s = filename.split('_')
        bench_name = '_'.join(s[2:len(s)-1])
        runtime_name = s[0]
        assert(runtime_name == "gvisor")

        #print (filename, bench_name)
        f = open(os.path.join(valve_results_gvisor_dir, file), 'r')
        for line in f.readlines():
            avg = float(line.strip().split(',')[0].strip().split(':')[1].strip())
            stdev = float(line.strip().split(',')[1].strip().split(':')[1].strip())
            valve_results_gvisor[file_to_bench[bench_name]] = (avg, stdev)
            break

    for file in os.listdir(trapeze_results_gvisor_dir):
        filename = os.fsencode(file).decode('utf-8')
        #print (filename)
        s = filename.split('_')
        bench_name = '_'.join(s[2:len(s)-1])
        runtime_name = s[0]
        assert(runtime_name == "gvisor")

        #print (filename, bench_name)
        f = open(os.path.join(trapeze_results_gvisor_dir, file), 'r')
        for line in f.readlines():
            avg = float(line.strip().split(',')[0].strip().split(':')[1].strip())
            stdev = float(line.strip().split(',')[1].strip().split(':')[1].strip())
            trapeze_results_gvisor[file_to_bench[bench_name]] = (avg, stdev)
            break

    # Normalize and compute averages
    for file in os.listdir(vanilla_results_gvisor_dir):
        filename = os.fsencode(file).decode('utf-8')
        #print (filename)
        s = filename.split('_')
        bench_name = '_'.join(s[2:len(s)-1])
        runtime_name = s[0]
        assert(runtime_name == "gvisor")

        #print (filename, bench_name)
        f = open(os.path.join(vanilla_results_gvisor_dir, file), 'r')
        for line in f.readlines():
            gvisor_avg = float(line.strip().split(',')[0].strip().split(':')[1].strip())
            gvisor_stdev = float(line.strip().split(',')[1].strip().split(':')[1].strip())
            vanilla_results_gvisor[file_to_bench[bench_name]] = (avg, stdev)

            (kalium_avg, kalium_stdev) = vanilla_results_kalium[file_to_bench[bench_name]]
            (trapeze_avg, trapeze_stdev) = trapeze_results_gvisor[file_to_bench[bench_name]]
            (valve_avg, valve_stdev) = valve_results_gvisor[file_to_bench[bench_name]]

            kalium_rel = kalium_avg / gvisor_avg
            trapeze_rel = trapeze_avg / gvisor_avg
            valve_rel = valve_avg / gvisor_avg
            
            vanilla_results_kalium[file_to_bench[bench_name]] = (kalium_rel, kalium_stdev)
            trapeze_results_gvisor[file_to_bench[bench_name]] = (trapeze_rel, trapeze_stdev)
            valve_results_gvisor[file_to_bench[bench_name]] = (valve_rel, valve_stdev)

            break 
    
    create_csv("seclats.csv", vanilla_results_kalium)
    create_csv("trapezelats.csv", trapeze_results_gvisor)
    create_csv("valvelats.csv", valve_results_gvisor)
            

main()

        

import os
import statistics

# Define the root directories
root_dirs = ["vanilla-hello-retail", "valve-hello-retail"]

# Define the subdirectories of interest
subdirs = ["1.assign", "2.record", "3.receive", "4.success", "6.report"]

# Define the file names
file_names = ["bench_20_assign", "bench_20_record", "bench_20_receive", "bench_20_success", "bench_20_report"]

# Output file
output_file = "averages.txt"

with open(output_file, "w") as f:
    f.write("Averages of bench files:\n\n")
    for root_dir in root_dirs:
        f.write(f"Directory: {root_dir}\n")
        for subdir in subdirs:
            for file_name in file_names:
                bench_file = os.path.join(root_dir, "product-photos", subdir, file_name)
                if os.path.exists(bench_file):
                    with open(bench_file) as bf:
                        values = [float(line.strip()) for line in bf.readlines()]
                        avg = statistics.mean(values)
                        f.write(f"File: {bench_file} - Average: {avg:.6f}\n")
                else:
                    f.write(f"File: {bench_file} - Not found\n")
        f.write("\n")

# Benchmarks for Kalium

**Warning** This guide should be followed after installing OpenFaas on a Kubernetes cluster.

The guide contains the steps to generate the performance data and graphs in the evaluation section of the paper. More specifically, the repository contains the data and setup needed to reproduce Figures 7 and 8 along with the fine grained measurements for the per-system call overhead.

Clone this repository on the Kubernetes controller node.

### Table of Contents
1. [Setting up MySql Database](#mysql)
2. [Setting up Image Server](#imgsrvr)
3. [Running Benchmarks](#bench)
4. [Running Microbenchmark for Per-Syscall Overheads](#micro)
5. [Generating Performance Graph (Figure 8)](#graph)
6. [Generating Policy Accuracy Graph (Figure 7)](#policy)
7. [Generating Per Syscall Overheads](#syscall)


### 1. Setting up MySql Database <a name="mysql"></a>
**[Time taken: approx 30 mins]**

Some of the benchmark functions require a prebuilt database. The database is run inside a Kubernetes pod in the openfaas-fn namespace.
```
cd mysql
kubectl apply -f ./mysql-pv.yml
kubectl apply -f ./mySqlDeployment.yml
```

Check if the mysql pod is ready by running `kubectl get pods -n openfaas-fn -o wide`

Once the pod is ready, populate it by connecting to it, creating a new user and uploading the prebuilt database.
```
$ sudo apt install -y mariadb-client-core-10.1
$ mysql -u root -ppassword -h <mysql pod IP> -P 3306
> CREATE USER 'abc'@'%' IDENTIFIED BY 'xyz';
> GRANT ALL PRIVILEGES ON * . * TO 'abc'@'%';
> create database helloRetail;
> exit
$ mysql -u root -ppassword -h <mysql pod IP> -P 3306 -D helloRetail < ../vanilla-hello-retail/helloRetailVanillaFinal.sql
$ mysql -u root -ppassword -h <mysql pod IP> -P 3306
> use helloRetail;
> alter table storedPhotosTable add label INTEGER NOT NULL;
> exit
```

### 2. Setting up Image Server <a name="imgsrvr"></a>
**[Time taken: approx 10 mins]**

**If this step was already done then it can be skipped.**

The image server is needed for the microbenchmark as well as the receive function in the product-photos benchmark. It is a python server script that serves an image at the url https://<hostname>:4443/image.jpg

In order for kalium to intercept the request, the server needs a valid certificate chain.

Copy the `python_server` folder into the controller node. Follow the guide at [the certbot website](https://certbot.eff.org/instructions?ws=other&os=ubuntubionic) to get a certificate for the controller domain. When prompted for the domain, provide the publicly facing hostname of the controller node.

Create a directory called `certs` in `srv_dir`. Copy `fullchain.pem` and `privkey.pem` to `certs`.

Open a new terminal to the controller and start the server by running `python server.py`. Test it out by visiting the URL [https://\<hostname\>:4443/image.jpg]() on your browser

### 3. Running Benchmarks <a name="bench"></a>
**[Time Taken: 3-4 hours]**

The benchmarks consist of 3 application flows: productCatalogApi, product-photos, product-purchase. The 3 flows need to be run with stock gVisor as well as with Kalium.

#### 3.1 Running with Stock gVisor
If there are changes to the repo from the previous runs, run `git checkout .` to reset the changes.

Checkout the gvisor branch of the benchmarks by running `git checkout artifact_gvisor`
Copy `build/bin/runsc_stock` to `/usr/local/bin/runsc` on all the Kubernetes nodes. Open a new terminal to the controller and start the image server by running `python server.py`.

Run `scripts/replace_image_url.py <kalium-benchmarks-root-dir> https://<hostname>:4443/image.jpg` to replace all the benchmark inputs with the image URL.
Run all the benchmarks as follows:
```
$ pushd vanilla-hello-retail && ./run_all_benches.sh gvisor && popd
$ pushd valve-hello-retail && ./run_all_benches.sh gvisor && popd
$ pushd trapeze-hello-retail && ./run_all_benches.sh gvisor && popd
```

The above commands will generate results directories `results_gvisor` under the respective directories (vanilla-hello-retail, valve-hello-retail, trapeze-hello-retail).

#### 3.2 Running with Kalium
If there are changes to the repo from the previous runs, run `git checkout .` to reset the changes.

Checkout the gvisor branch of the benchmarks by running `git checkout artifact_kalium`.
Copy `build/bin/runsc_kalium` to `/usr/local/bin/runsc` on all the Kubernetes nodes. 

Open a new terminal to the controller and start the image server by running `python server.py`. Start the controller by running `./ctr policy_test.json` on the controller node.

Run `scripts/replace_image_url.py <kalium-benchmarks-root-dir> https://<hostname>:4443/image.jpg` to replace all the benchmark inputs with the image URL. Make sure that ports 4443 and 5000 are publicly reachable at the controller.

Run all the benchmarks as follows:
```
$ pushd vanilla-hello-retail && ./run_all_benches.sh kalium && popd
```

The above commands will generate result directory `results_kalium` under the respective directory (vanilla-hello-retail).

### 4. Running Microbenchmark for Per-Syscall Overheads <a name="micro"></a>
If there are changes to the repo from the previous runs, run `git checkout .` to reset the changes.

Checkout the gvisor branch of the benchmarks by running `git checkout artifact_kalium`.
Copy `build/bin/runsc_microbench` to `/usr/local/bin/runsc` on all the Kubernetes nodes. Clear `/mydata/runsc_logs` on all the Kubernetes nodes.

Open a new terminal to the controller and start the image server by running `python server.py`. Start the controller by running `./ctr policy_test.json` on the controller node.

Run `scripts/replace_image_url.py <kalium-benchmarks-root-dir> https://<hostname>:4443/image.jpg` to replace all the benchmark inputs with the image URL. Make sure that ports 4443 and 5000 are publicly reachable at the controller.


Run the microbenchmark as follows:
```
$ cd vanilla-hello-retail/product-photos/1.microbench
$ faas-cli deploy -f product-photos-1-microbench.yml --gateway $HOSTNAME:31112
$ sleep 70
$ ./run_bench.sh 20 bench_20_microbench
```

Check the node on which the pod is running by running `kubectl get pods -n openfaas-fn -o wide`.

Open to a shell to the node running the microbenchmark pod and navigate to `/mydata/runsc_logs/`. There should be exactly one file ending with `.boot`, if there are multiple files from previous runs, note the one which is modified the latest.

Copy the `.boot` file locally for later analysis.

### 5. Generating Performance Graph (Figure 8) <a name="graph"></a>
Run `python3 compute_rel_graph_csv.py <vanilla_results_kalium_dir> <vanilla_results_gvisor_dir> <valve_results_gvisor_dir> <trapeze_results_gvisor_dir>` where:
- `<vanilla_results_kalium_dir>` is `vanilla-hello-retail/results_kalium`
- `<vanilla_results_gvisor_dir>` is `vanilla-hello-retail/results_gvisor`
- `<valve_results_gvisor_dir>` is `valve-hello-retail/results_gvisor`
- `<trapeze_results_gvisor_dir>` is `trapeze-hello-retail/results_gvisor`

This will generate 3 files: seclats.csv, valvelats.csv and trapezelats.csv. These file can be replaced in 56, 60 and 64 in `graphs/figure/fig_latRestRel.tex`. After this run `make` in the graphs directory.

### 6. Generating Policy Accuracy Graph (Figure 7) <a name="policy"></a>

Run `make` in the `graphs` directory. The data used to generate the data is already present.

### 7. Generating Per Syscall Overheads <a name="syscall"></a>
Run `scripts/display_per_syscall_overheads.py <boot_file>` where:
- `<boot_file>` is the boot file saved from the microbenchmark run

This script will print out the statistics of the various overheads.

#!/usr/bin/sh

remove_function() {
	faas-cli remove trapeze-product-catalog-builder
}

build_function() {
	faas-cli build -f product-catalog-builder.yml
}

push_to_registry() {
	docker push innocentjr1995/trapeze-product-catalog-builder:latest
}

deploy_function() {
	faas-cli deploy -f product-catalog-builder.yml
}

print_function_pod_name() {
	kubectl get pods -n openfaas-fn | grep "trapeze-product-catalog-builder" | cut -d ' ' -f1 |  xargs -I {} echo -e "    **************************************************************\n\tTrapeze Product Catalog Build Pod: \n\t\t{}\n    **************************************************************"
}

export_pod_name() {
	export PODNAME=$(kubectl get pods -n openfaas-fn | grep "trapeze-product-catalog-builder" | cut -d ' ' -f1 |  xargs -I {} echo {})

	echo $PODNAME;	
}

exec_in_pod() {
	NAME=$(export_pod_name)
	kubectl exec -it $NAME -n openfaas-fn -- sh

}

	
main(){
	remove_function
	build_function
	push_to_registry
	deploy_function
	print_function_pod_name
}

decide(){
	if [ $1 = "build" ]; then
		main
	elif [ $1 = "exec" ]; then
		exec_in_pod 
	else
		echo "Wrong argument"
	fi
}

while getopts s: flag
do
	case "${flag}" in
		s) state=${OPTARG};;
	esac
done

decide $state



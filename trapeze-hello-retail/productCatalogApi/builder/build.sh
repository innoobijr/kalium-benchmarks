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

print_funciton_pod_name() {
	kubectl get pods -n openfaas-fn | grep "trapeze-product-catalog-builder" | cut -d ' ' -f1 |  xargs -I {} echo -e "    **************************************************************\n\tTrapeze Product Catalog Build Pod: \n\t\t{}\n    **************************************************************"
}


main(){
	remove_function
	build_function
	push_to_registry
	deploy_function
	print_funciton_pod_name
}

main

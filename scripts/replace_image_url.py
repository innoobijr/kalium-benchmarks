#!/usr/bin/python3

import sys
import json

filenames = ['valve-hello-retail/product-photos/1.microbench/sample-input_localurl.json',
             'trapeze-hello-retail/product-photos/1.microbench/sample-input.json',
             'trapeze-hello-retail/product-photos/4.success/sample-input.json',
             'valve-hello-retail/product-photos/master/sample-input-photos.json',
             'valve-hello-retail/product-photos/4.success/sample-input.json',
             'trapeze-hello-retail/product-photos/master/sample-input-photos.json',
             'trapeze-hello-retail/product-photos/3.receive/sample-input.json',
             'valve-hello-retail/product-photos/3.receive/sample-input_localurl.json',
             'vanilla-hello-retail/product-photos/4.success/sample-input.json',
             'vanilla-hello-retail/product-photos/master/sample-input-photos.json',
             'vanilla-hello-retail/product-photos/1.microbench/sample-input_localurl.json',
             'vanilla-hello-retail/product-photos/3.receive/sample-input_localurl.json']

def usage():
    print ("python3 replace_image_url.py <repository_root> <replacement URL>")
    exit(1)

def main():
    if len(sys.argv) != 3:
        usage()


    repo_root = sys.argv[1]
    replacement_url = sys.argv[2]

    for file in filenames:
        f_path = repo_root + '/' + file
        f = open(f_path, 'r+')
        j = json.loads(f.read())

        j["MediaUrl0"] = replacement_url
        
        res = json.dumps(j)
        f.close()
        f_w = open(f_path, 'w')
        f_w.write(res)

main()
        

#!/usr/bin/env python2
# taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate certificates with the following command:
#    export EMAIL=admin@example.com
#    export DOMAIN=example.com
#    curl -sL https://gist.githubusercontent.com/RichardBronosky/644cdfea681518403f5409fa16823c1f/raw/get_letsencrypt_cert.sh | bash
# create symbloic links to the certificates
#    ln -s /etc/letsencrypt/live/$DOMAIN/fullchain.pem ./
#    ln -s /etc/letsencrypt/live/$DOMAIN/privkey.pem ./
# run as follows:
#    python simple-https-server.py
# then in your browser, visit:
#    https://localhost or https://$DOMAIN

import BaseHTTPServer, SimpleHTTPServer
import ssl

httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
#httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./fullchain.pem', keyfile='./privkey.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2, ciphers="ECDHE-RSA-AES256-GCM-SHA384")
#httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./certs/fullchain.pem', keyfile='./certs/privkey.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2, ciphers="ECDHE-RSA-AES256-GCM-SHA384")
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./certs/fullchain.pem', keyfile='./certs/privkey.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2, ciphers="ECDHE-RSA-AES256-GCM-SHA384, ECDHE-ECDSA-AES256-GCM-SHA384")
httpd.serve_forever()


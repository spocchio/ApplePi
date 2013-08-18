#!/bin/bash

resPy=$(python -c 'import web' 2>&1 )
if [ ! -z "$resPy" ]; then
	echo ""
	echo "ApplePi: The python package web is necessary and is not found, doyou want to install it now? [y]/n"
	read a
	if [ "$a" == 'y' ] || [ "$a" == 'Y' ] || [ "$a" == '' ]; then
		echo ""
		echo "Installing web package.."
		rm -rf web
		wget http://webpy.org/static/web.py-0.37.tar.gz
		tar -xvzf web.py-0.37.tar.gz
		mv web.py-0.37/web web
		rm -rf web.py-0.37.tar.gz web.py-0.37
	fi
fi

echo ""
echo "ApplePi: If you want to use secure connections (HTTPS) you need to make a certificates, the certificates has to be the files server.key and server.crt."
echo "ApplePi: Do you want to (re)generate these files now? [y]/n"
read a
if [ "$a" == 'y' ] || [ "$a" == 'Y' ] || [ "$a" == '' ]; then
	echo ""
	echo "ApplePi: Generating the key:"
	openssl genrsa -des3 -out server.key 2048
	echo ""
	echo "ApplePi: Generating CSR File, probably you have to reinsert the passphrase"
	openssl req -new -key server.key -out server.csr
	echo ""
	echo "ApplePigenerating the private key,  probably you have to reinsert the passphrase"
	openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

fi

echo ""
echo "ApplePi: Remember: you need to install the package pyOpenSSL to use the ssl connection"

echo ""
echo "It is reccommended for you to edit the file config.json to modify the authentication user/password key."



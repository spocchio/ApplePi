ApplePi
=======

With  ApplePi you can easly create python web apps to remotely manage your Pi! 
Currently, these are the app installed:

* a basic System Monitor (temperature, cpu usage ecc..)
* web Shell
* Media Center (let you play OMXPlayer videos)
* File Manager (let you upload and download from the web

All apps have:

* Basic authentication
* possible HTTPS connection
 
# Installation:

you should installthe `web` python package, put ssl certificate files as `server.crt` and `server.key`, and modify the user/password pair in the `config.json` file.
Or just run

	bash setup.bash

# Usage:

In the Raspberry execute:

	python ApplePi.py

In your favorite browser go to

	https://ip_of_yor_pi/


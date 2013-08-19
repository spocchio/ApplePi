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
 
PS: This is a prototype, do not wait to contact me if you need help or, better, if you want to help me :D

## Installation:

you should installthe `web` python package, or just run

	bash setup.bash

This will also set up the local/public pair key for the SSL connection. For HTTPS you need the pyOpenSSL package.

Please modify the user/password authentication pair in the file `config.json`. 

## Usage:

In the Raspberry execute:

	python ApplePi.py

In your favorite browser go to

	http://ip_of_yor_pi/

The default user is `pi` with password `gamma`

## Screenshots:

The web shell:
![web shell](https://lh3.googleusercontent.com/-XHJGxW0ggiY/UhInDCZUu7I/AAAAAAAAAmA/Z0WAe-gr1co/s800/apple_bash.png)
The remote OMXPlayer:
![OMXPlayer remote ](https://lh6.googleusercontent.com/-OOqnpsHqdbk/UhInDESbsCI/AAAAAAAAAmE/89ME6P29IKc/s800/apple_omx.png)


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

## Writing your own app:

### Introduction

ApplePi is an HTTP RPC Server with an HTML/JS frontend, this mean that you can access every app directly throught an IP address, e.g.:

	http://raspberry_pi:8080/SystemMonitor//getDiskSpace

will execute the method `getDiskSpace(self)` inside the class `SystemMonitor`.

You can also pass parameters to the method of the apps, for example:

	http://raspberry_pi:8080/AppManager//echo?message=Hello

will execute the method `echo(self, message = None)` inside the class `AppManager` and with the parameter `message` taken by the HTTP Request.


### Hello World App

The applications run by ApplePi are in the `apps` folder, each app stays in a different folder and a class with the same name should be defined in  `__init__.py` file.
Each app class inherits from the class `WebApp` (stored in `ApplePi/WebApp.py`) which handle the `GET` and `POST`, the authentication and the file uploading.
should have the `HTML(self)`  method that is loaded by default when you open it with the browser.

For example, to create an Hello World application, create the file `ApplePi/apps/HelloWorld/__init__.py`
and write into it:

	import WebApp
	
	class HelloWorld(WebApp):
		def HTML(self):
			return "Hello my world!"
	
You have to restart ApplePi to test a new app, but then you can modify it without resetting ApplePi,
you canseeyour app on 

	http://raspberry_pi/

or directly access on 

	http://raspberry_pi/HelloWorld//HTML

### Returning HTML Data

It is the `WebApp.WebApp` class that take the return of the called method and send it to your browser, since it is mainly an RPC Server, you can return any object, like:

	import WebApp
	import os
	
	class HelloWorld(WebApp.WebApp):
		def HTML(self, key=None):
			if(key == None or key not in os.environ): return os.environ
			else: return os.environ[key]

First you will notice that the `HelloWorld` app is appeared in the list of application in the ApplePi front-end!
you can try

	http://raspberry_pi:8080/HelloWorld//HTML

and

	http://raspberry_pi:8080/HelloWorld//HTML?key=DESKTOP_SESSION


So, ApplePi by default returns a JSON object.. and if you return a string with an HTML content..well it will be encolsed by two apex!
to tell the class WebApp that you want to return only HTML stuff, just set the parameter `isHTML` to `True`, for example:

	import WebApp
	import datetime
	
	class HelloWorld(WebApp.WebApp):
		isHTML = True
		def HTML(self):
			return "Now is <b>%s</b>" % str(datetime.datetime.now())

You can access  this tiny app also browsing the HTML/JS client on http://raspberry_pi:8080/

### Using Javascript

Let think you want to automatically update some fields you are showing, or to send an input to the server through the web interface,
ApplePi has some javascript function, stored on `static/rpcberry.js` that let you do some AJAX in the front-end.

#### the call Javascript method
Parameters: `call(object,self,method,parameters,f)`

* object is the name of the app you want to execute
* self is the instace id (because you can open multiple applications like the Shell, see the chapter ***Multiple Instances***), you can take it as an empty string at the moment 
* method, is the method to call inside the object `object`.
* parameters, the parameters of the function, have to stay in a dictionary, like `{'key':'value'}`
* f, a callback called with the result of the function `method`

for example: 

	import WebApp
	import datetime
	
	class HelloWorld(WebApp.WebApp):
		isHTML = True
		def now(self):
			return datetime.datetime.now()
		def HTML(self):
			return """ <a href='#' onclick="call('HelloWorld','','now',{},function(x){alert(x)})"> click here to know the current time	""" 

#### the read Javascript method
the `read` function is bot trivial as the `call` function, because it don't ask for the object name and for the instance id as parameters.

Parameters: `read(method,parameters,f)`

* method, is the method to call inside the object `object`.
* parameters, the parameters of the function, have to stay in a dictionary, like `{'key':'value'}`
* f, a callback called with the result of the function `method`

for example: 

	import WebApp
	import datetime
	
	class HelloWorld(WebApp.WebApp):
		isHTML = True
		def now(self):
			return datetime.datetime.now()
		def HTML(self):
			return """ <a href='#' onclick="read(now',{},function(x){alert(x)})"> click here to know the current time	""" 


#### The readHTML JS method
sometimes you want to just put the output of a method in a field, so use the readHTML method.
this is a less trivial method and you don't need to specify the application name and the instance id (it is implied you want to call a method of the current loaded app)

	function readHTML(method,parameters,ele,f)

* method, is the function name of the currently opened app
* parameters have to stay in a dictionary, like `{'key':'value'}`, if the function doesn't have parameters (if not `self`) then you can put `{}`
* element in which put the result of the call
* an optional callback function to handle the final result

example:
	import WebApp
	import datetime

	class HelloWorld(WebApp.WebApp):
		isHTML = True
		def now(self,hello_string):
			return hello_string+' '+str(datetime.datetime.now())
		def HTML(self):
			return """<b id ='b_field'></b> <a href='#' onclick="readHTML('now',{'hello_string':'Now is'},$('#b_field'))"> click here to update the current time	</a>""" 

#### the reloadEvery JS method :
This is the definition of the function:

	function reloadEvery(method,parmeters,idElem,t,f)

it is like `readHTML` but takes also the `t` parameter that reload the element every `t` milliseconds

	import WebApp
	import datetime
	
	class HelloWorld(WebApp.WebApp):
		isHTML = True
		def now(self,hello_string):
			return hello_string+' '+str(datetime.datetime.now())
		def HTML(self):
			return """<b id ='b_field'></b> 
			<script>
				reloadEvery('now',{'hello_string':'Now is'},$('#b_field'),1000)
			</script>""" 

### Caching data

You would like to receive an input from the user and to save it in memory, 
since ApplePi is made with web.py that re-instantiate the class everytime, the class `WebApp` gives you a variable called self.data
which is a dict and is persistent!

have a look here:

	import WebApp
		

	class HelloWorld(WebApp.WebApp):
		isHTML = True
		def store(self,message = None):
			self.data['storage'] = message
		def load(self):
			if 'storage' in self.data: return self.data['storage']
			
		def HTML(self):
			return """ data stored:<b id ='b_field'></b> <br/>
			send data: <input id ="input_field" > <input type=submit id ="submit_field">
			<script>
				reloadEvery('load',{},$('#b_field'),1000)
				$('#submit_field').click(function(){
					read('store',{'message':$('#input_field').val()})
					return false;
				})
			</script>""" 

#### Browsing local files:

Sometimes you need to browse the files inside the Pi, to do it there is a trick that launch the jQuery-tree.
Here an example to download files from the Pi:

	import WebApp
		

	class HelloWorld(WebApp.WebApp):
		isHTML = True
		def store(self,message = None):
			self.data['storage'] = message
		def load(self):
			if 'storage' in self.data: return self.data['storage']
			
		def HTML(self):
			return """First of all <b>click</b> this input to select a folder or a file to work with:
					<input id="browse" type=text placeholder="Click to browse" name=mfile onclick='fileBrowserFromHidden(this); return false'>"""

The function `fileBrowserFromHidden(this)` will generate a browser that will store the selected file name on the input type above.

#### A simple example: download a file from the Pi


	import WebApp
	import web
		

	class HelloWorld(WebApp.WebApp):
		isHTML = True
		mediadir = os.path.expanduser('~')        
		def download(self, filename = None,action = None):
			
			if filename != None:	
				with  open(self.mediadir+filename) as f:
					web.header('Content-Disposition', 'attachment; filename="' + os.path.basename(filename) + '"')
					while True:
						data = f.read(1024)
						if not data:
							return
						yield data
		def HTML(self):
			return """
				<form method="POST"  enctype="multipart/form-data" action="/HelloWorld//download" target="my_iframe">
					Click this input to select a folder or a file to work with:
					<input type=text placeholder="Click to browse" name=filename onclick='fileBrowserFromHidden(this); return false'>
					<input type=submit name=action value="Download the selected file"/>
				</form>
			<iframe name="my_iframe" src="about:blank"></iframe>
			"""


Notable stuff:

* Since the download of data is not made through AJAX I used an `<iframe>` where I redirect the `<form>` request. of the `HelloWorld.download(self,name)` method:
* I imported `web` to modify the  header
* to download large files you can't just return it content, you have to use a Generator, ApplePi supports it and the method `download` is a generator function that returns chunks of data
* I manually set the basedir `mediadir` to `~`, becouse at the moment there is no place where a global configuration is store.

### Uploading files

To upload a file you can't use ajax and you need a little workaround using the POST method you are forced to use a `<form>`.
when a file is sent to a method from the `<form>`, the parameter of the function corresponding to the `<input type="upload/>`
***don't contain the file data*** but a dict with the filename of the temporary uploaded file and the name of the uploaded file.

Since we need to use a POST request, we need to direct it somewhere and this is why I use an iframe here. 


This is an example:


	import WebApp 
	import os
		

	class HelloWorld(WebApp.WebApp):
		isHTML = True
		mediadir = os.path.expanduser('~')        
		def upload(self, filename = None,action = None):
			if filename != None:	
					dest = self.mediadir
					print filename
					dest = self.mediadir +'/'+ filename['filename']
					print dest
					os.rename(filename['path'],dest)
					return 'File saved on '+dest
		def HTML(self):
			return """	<form method="POST"  enctype="multipart/form-data" action="/HelloWorld//upload" target="my_iframe">
						<input type=submit name=action value="Upload here the following file:"/>
						<input type=file  name=filename />
						</form>
						<iframe name="my_iframe" src="about:blank"></iframe>	"""
### Multiple instances

Some thinGs you have to know:
 * As you can see you can open several instance of the web shell. You can try to reopen ApplePi in another browser and yet, there are the same instance of the web shells.
This is the many idea of ApplePi: access from every where your Pi, and, if I start a `bash` command in my cellphone I want to be able to end it on my desktop ;D
 * if you access the url `http://raspberry_pi:8080/HelloWorld//` a number is returned which is the instance ID of the app.
 * To let your app be multi-instantiable, add a flag `keepInstance=True`
 * You may access a particoular instance `INSTANCE_ID` of a class by the url `http://raspberry_pi:8080/HelloWorld/INSTANCE_ID/`.
 
 Here an example:
 
	import WebApp 
		

	class HelloWorld(WebApp.WebApp):
		isHTML = True
		keepInstance=True
		def HTML(self):
			if not 'hits' in self.data: self.data['hits'] = 0
			self.data['hits']+=1
			return """	you hit me %s times """ % self.data['hits']
	
 * If you go to `http://raspberry_pi:8080/HelloWorld//` , then a number is returned and it is the instance ID (e.g. `123456678`), 
 * to open a particoular instance (e.g. `12345678`)go to: `http://raspberry_pi:8080/HelloWorld/12345678/HTML` 
 
 
### AppManager

to have a list of the loaded applications and their instances go to:

	http://raspberry_pi:8080/AppManager//appList
 
## Screenshots:

The web shell:
![web shell](https://lh3.googleusercontent.com/-XHJGxW0ggiY/UhInDCZUu7I/AAAAAAAAAmA/Z0WAe-gr1co/s800/apple_bash.png)
The remote OMXPlayer:
![OMXPlayer remote ](https://lh6.googleusercontent.com/-OOqnpsHqdbk/UhInDESbsCI/AAAAAAAAAmE/89ME6P29IKc/s800/apple_omx.png)



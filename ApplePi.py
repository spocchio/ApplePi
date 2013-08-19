#!/usr/bin/python
import web
import apps.AppManager
import WebApp
import sys
import threading
import os
import json
import time


from web.wsgiserver import CherryPyWSGIServer

# load configuration
config = json.loads(file('config.json').read())
if(config['ssl']['enabled']):
	CherryPyWSGIServer.ssl_certificate = config['ssl']['certificate']
	CherryPyWSGIServer.ssl_private_key = config['ssl']['private']
if(config['auth']['enabled']):
	WebApp.allowed = ((config["auth"]["user"],config["auth"]["pass"]),)

#config redirection to the static folder
urls = ['/', 'redirect']

#load the applications from the 'apps' folder
apps = json.loads(apps.AppManager.AppManager().appList())
for app in apps:
	appUrl = '/'+app+'/(.*)/(.*)'
	appClass = 'apps.'+app+'.'+app
	if appClass not in urls:
		k = eval('__import__("apps.'+app+'").'+app+'.'+app+'.keepInstance')
		if(not k): WebApp.selfies[app]=None
		else: WebApp.selfies[app]={}
		urls.append(appUrl)
		urls.append(appClass)

#show the apps and the mapping.		
print 'urls:', urls

if __name__ == "__main__":
	# web.py has troubles to stop on the CTRL-C event,
	# so I have to start it as a thread and to manually catch the 
	# CTRL-C
	def startServer():
		global urls
		class redirect:
		    def GET(self):
		        raise web.seeother('/static/index.html')
		app = web.application(urls,locals())
		app.run()
	t = threading.Thread(target=startServer, args=[])
	t.start()
	while True:
		try:
			pass
			time.sleep(1)
		except KeyboardInterrupt:
			print 'CTRL+C'
			os.kill(os.getpid(),9)			
	        	
        
		


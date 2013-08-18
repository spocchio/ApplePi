import web
import apps.AppManager
import WebApp
import json
from web.wsgiserver import CherryPyWSGIServer

# load configuration
config = json.loads(file('config.json').read())
CherryPyWSGIServer.ssl_certificate = config['ssl']['certificate']
CherryPyWSGIServer.ssl_private_key = config['ssl']['private']
WebApp.allowed = ((config["auth"]["user"],auth["auth"]["pass"]),)

#config redirection to the static folder
urls = ['/', 'redirect']
class redirect:
    def GET(self):
        raise web.seeother('/static/index.html')

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
    app = web.application(urls,locals())
    app.run()


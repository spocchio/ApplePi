import web
import apps.AppManager
import WebApp

urls = ['/', 'redirect']


class redirect:
    def GET(self):
        raise web.seeother('/static/index.html')

apps = apps.AppManager.AppManager().appList()
for app in apps:
	appUrl = '/'+app+'/(.*)/(.*)'
	appClass = 'apps.'+app+'.'+app
	if appClass not in urls:
		k = eval('__import__("apps.'+app+'").'+app+'.'+app+'.keepInstance')
		if(not k): WebApp.selfies[app]=None
		else: WebApp.selfies[app]={}
		urls.append(appUrl)
		urls.append(appClass)
		
print urls

if __name__ == "__main__":
    app = web.application(urls)
    app.run()


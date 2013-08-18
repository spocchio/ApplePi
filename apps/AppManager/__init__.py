import web 

import WebApp
import os
import json
		
class AppManager(WebApp.WebApp):
	#mediadir = 'media/'
	mediadir = os.path.expanduser('~')
	def __init__(self):
		pass
	def fileList(self,folder = ""):
		#mediadir='media/'
		mediadir= self.mediadir
		l = os.listdir(mediadir+folder)
		files=[]
		for f in l:
			if(os.path.isfile(mediadir+folder+f)):
				files.append({'name':f,'type':os.path.splitext(f)[1][1:]})
			else:
				files.append({'name':f,'type':'folder'})
		return json.dumps(files);
				

		
	def dirList(self,folder = ""):
		#mediadir='media/'
		mediadir = self.mediadir
		return filter(os.path.isdir,  os.listdir(mediadir+folder)) 
		
	def appList(self):
		appsdir='./apps'
		ls = os.listdir(appsdir) 
		apps = {}
		for f in ls:
			if(os.path.isdir(appsdir+'/'+f)):
				app = f
				if (self.instanciable(app)): apps[app]=self.instanceList(app)
				else: apps[app]=None
		#print json.dumps(apps)
		return json.dumps(apps)
	def close(self,app=None,id=None):
		#del WebApp.selfies[app][id]
		raise  web.seeother('/'+app+'/'+id+'/close?app='+app+'&id='+id)
	def instanceList(self,app):
		if app in WebApp.selfies and WebApp.selfies[app]!=None : return WebApp.selfies[app].keys()
		else: return []
	def instanciable(self,app):
		return   app in WebApp.selfies and WebApp.selfies[app]!=None
	def HTML(self):
		return '<div> <p>Welcome to RPC Berry - Remotely controll your device ;) </p> <p> By Antonio Ragagnin [spocchio@gmail.com] </p></div>'

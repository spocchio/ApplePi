import datetime
import tempfile
import random
import web
import json
import urllib2
import os
import inspect
import re
import base64

selfies = {}
selfies2 = {}

allowed  = (('user','pass'),)

class WebApp:
	keepInstance=False
	isHTML = False
	_id = None
	def _getUrl(self):
		return web.ctx.home + web.ctx.fullpath
	def _render(self,x):
		if x == None: return 'null'
		if(self.isHTML): return x
		try:
			data = json.dumps(x)
			return data
		except:
			return x
	def _getPars(self,url):
		if(url != ""):
			params = url.split("?",1)[1]
			params = params.split("&")
			res = dict()
			for param in params:
				(k,v) = param.split("=",1)
				k=urllib2.unquote(k.decode("utf8"))
				v=urllib2.unquote(v.decode("utf8"))
				v = v.replace('+',' ')
				#print k,v
				res[k]=v
			return res
		else: return dict()
	def GET(self,_id,f,forzaParametri = None):
		auth = web.ctx.env.get('HTTP_AUTHORIZATION')
		error  = False
		authreq = False
		if auth is None: authreq = True
		else:
			auth = re.sub('^Basic ','',auth)
			username,password = base64.decodestring(auth).split(':')
			print (username,password) , allowed, (username,password)  in allowed
			if (username,password) not in allowed:
				authreq = True 
		if authreq:
			web.header('WWW-Authenticate','Basic realm="Authorized access only"')
			web.ctx.status = '401 Unauthorized'
			error =  True
		cname = self.__class__.__name__
		if(self.keepInstance):
			if cname not in selfies: selfies[cname]={}
			if(_id==''):
				_id=str(id(self))
				selfies[cname][_id]={}
			if _id not in selfies[cname]:
				yield 'null'
				error = True
			self.data = selfies[cname][_id]
			self._id = _id
		else:
			if cname not in selfies2: selfies2[cname]={}
			self._id = None
			self.data = selfies2[cname]
		query=web.ctx.query
		pars = self._getPars(query)
		if (isinstance(forzaParametri,dict)):
			for k in forzaParametri:
				v=forzaParametri[k]
				pars[k]=v
				
		#print web.ctx.path
		#print web.ctx.homepath
		#print pars.keys();
		print 'Parameters: ',pars.keys(),', App: ',cname,', Id:',_id
		if f != "" and f != None:
			
			fz = getattr(self, f)
		else:
			fz = self.index
		if not error:
			if inspect.isgeneratorfunction(fz):
				for res in fz(**pars):
					yield res
			else:
				yield fz(**pars)
	def POST(self,id,f):
		pars2 = web.input()
		filedir = 'tmp' # change this to the directory you want to store the file in.
		for par in pars2:
			 
			 
			try:
				pars=web.input(**{par:{}})
				#web.debug(par)
				#print 'par:',web.debug(pars[par])
				if(pars[par].filename!=None):
					print 'lord...there isa file here!!'
					#web.debug(pars[par].filename)
					filename=str(random.random())+pars[par].filename.replace('\\','_')
					
					#filename="a"
					#web.debug(filename)
					fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
					fout.write(pars[par].file.read()) # writes the uploaded file to the newly created file.
					fout.close() # closes the file, upload complete.
					#web.debug (filename)
					pars2[par]={'path':filedir+'/'+filename,'filename':pars[par].filename}
					 
			except:
				pass	
#		web.debug('ecc')
		for gamma in self.GET(id,f,forzaParametri = pars2):
			yield gamma
	def index(self):
		return id(self)
	def close(self,app,id):
		return 'null'

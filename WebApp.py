import datetime
import tempfile
import random
import web
import json
import urllib2
import os

selfies = {}
selfies2 = {}

class WebApp:
	keepInstance=False
	isHTML = False
	_id = None
	def _getUrl(self):
		return web.ctx.home + web.ctx.fullpath
	def _render(self,x):
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
				print k,v
				res[k]=v
			return res
		else: return dict()
	def GET(self,_id,f):
		cname = self.__class__.__name__
		if(self.keepInstance):
			
			if cname not in selfies: selfies[cname]={}
			if(_id==''):
				_id=str(id(self))
				selfies[cname][_id]={}
			self.data = selfies[cname][_id]
			self._id = _id
		else:
			if cname not in selfies2: selfies2[cname]={}
			self._id = None
			self.data = selfies2[cname]
		query=web.ctx.query
		pars = self._getPars(query)
		print web.ctx.path
		print web.ctx.homepath
		print pars;
		if f != "" and f != None:
			return self._render(getattr(self, f)(**pars))
		else:
			return self._render(self.index(**pars))
	def POST(self,id,f):
		pars2 = web.input()
		#print 'pars:',pars
		#print 'end pars'
		filedir = 'tmp' # change this to the directory you want to store the file in.

		for par in pars2:
			 
			 
			try:
				pars=web.input(**{par:{}})
				#web.debug(par)
				print 'par:',web.debug(pars[par])
				if(pars[par].filename!=None):
					print 'lord...there isa file here!!'
					web.debug(pars[par].filename)
					filename=str(random.random())+pars[par].filename.replace('\\','_')
					
					#filename="a"
					web.debug(filename)
					fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
					fout.write(pars[par].file.read()) # writes the uploaded file to the newly created file.
					fout.close() # closes the file, upload complete.
					web.debug (filename)
					pars2[par]={'path':filedir+'/'+filename,'filename':pars[par].filename}
					 
			except:
				web.debug('ecc')
		if f != "":
			 
			return self._render(getattr(self, f)(**pars2))
		else:
			return self._render(self.index(**pars2))
	def index(self):
		return id(self)

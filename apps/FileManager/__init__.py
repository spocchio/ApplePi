import web 

import WebApp
import os
import subprocess

import sys
import select

class FileManager(WebApp.WebApp):
	isHTML=True
	mediadir = os.path.expanduser('~')        
	def handle(self,mfile=None,nome=None, action=None,nfile=None):
		mediadir = self.mediadir	
		if action=='Download this' and mfile != None:
			with  open(self.mediadir+mfile) as f:
				web.header('Content-Disposition', 'attachment; filename="' + os.path.basename(mfile) + '"')
				while True:
					data = f.read(1024)
					if not data:
						return
					yield data
		else:
			web.header('Content-type','text/html')
			web.header('Transfer-Encoding','chunked')  
			if action=='Rename to' and mfile != None and nome!=None:
				
				dest = os.path.dirname(mfile) +nome
				os.rename(mediadir+mfile,mediadir+dest)
				yield '  folder/file '+mfile+' renamed to ! '+dest
			elif action=='Remove this' and mfile != None:
				os.remove(mediadir+mfile)
				yield '  folder/file '+mfile+' removed! '
			elif action=='Upload here' and mfile != None and nfile!=None:
				print 'nfile:'
				print nfile
				dest = mediadir+os.path.dirname(mfile) +'/' +nfile['filename']
				os.rename(nfile['path'],dest)
				print (nfile['path'],dest)
				yield str(nfile)+' uploaded on '+str(mfile)+'!'
			else:
				yield 'some error occurred: '+str((mfile,nome,action,nfile))
			yield '<script>window.parent.top.reloadApp()</script>'
		

	def HTML(self,c=None):
		return """
			<style>
				pre {background-color: #222; color: #cfc; 
				width:100%;
				overflow: scroll;} 
				#omxstatus{
					height:20%;
				}
				#omxout{
					height:20%;
				}
			</style>
		<article>
			<h3> Data Selection </h3>
			
				<h3>File Browser</h3>
				
			<form method="POST"  enctype="multipart/form-data" action="/FileManager//handle" target="my_iframe">
				<input type=text placeholder="Click to browse" name=mfile onclick='fileBrowserFromHidden(this); return false'>Browse files</button>
				<input type=submit name=action value="Download this"/><br/>
				<input type=submit name=action value="Remove this"/><br/>
				<input type=text name="nome"><input type=submit name=action value="Rename to"/><br/>
				<input type=file  name=nfile />	<input type=submit name=action value="Upload here"/>
			</form>
		</article>
		<iframe name="my_iframe" src="about:blank"></iframe>
			<script>
				
			</script>
			
	"""
	



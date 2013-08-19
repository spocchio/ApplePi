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
		if action=='Download the selected file' and mfile != None:
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
			if action=='Rename the selected file to:' and mfile != None and nome!=None:
				
				dest = os.path.dirname(mfile) +nome
				os.rename(mediadir+mfile,mediadir+dest)
				yield '  folder/file '+mfile+' renamed to ! '+dest
			elif action=='Remove the selected file' and mfile != None:
				os.remove(mediadir+mfile)
				yield '  folder/file '+mfile+' removed! '
			elif action=='Upload here the following file:' and mfile != None and nfile!=None:
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
				iframe{
					border:0;
					width:100%;
					
				}
			</style>
		<article>
			<h3> Manage the folders and files. </h3>
			
			
				
			<form method="POST"  enctype="multipart/form-data" action="/FileManager//handle" target="my_iframe">
				<p>
				First of all <b>click</b> this input to select a folder or a file to work with:
				<input type=text placeholder="Click to browse" name=mfile onclick='fileBrowserFromHidden(this); return false'>
					
				</p>
				<p>
					
					<input type=submit name=action value="Download the selected file"/>
				</p>
				<p>
					<input type=submit name=action value="Remove the selected file"/>
				</p>
				<p>
					<input type=submit name=action value="Rename the selected file to:"/>
					<input type=text name="nome">

				</p>
				<p>
					<input type=submit name=action value="Upload here the following file:"/>
					<input type=file  name=nfile />
				</p>
			</form>
		</article>
		<article>
		<p>The <b> upload system </b> is not free from bugs, here will appears the result of the posts:</p>
		<iframe name="my_iframe" src="about:blank"></iframe>
		</article>
			<script>
				
			</script>
			
	"""
	



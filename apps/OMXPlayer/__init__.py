import web 

import WebApp
import os
import subprocess

import sys
import select

class OMXPlayer(WebApp.WebApp):
	isHTML=True
	def close(self):
		if 'pipe' in self.data:
			self.data['err']=''
			try: self.data['pipe'].close()
			except: self.data['err'] = '\n Error closing pipe\n'
	def send(self,c):
		if 'pipe' in self.data:
			self.data['err']=''
			try: self.data['pipe'].stdin.write(c)
			except: self.data['err'] = '\n Error writing to pipe\n'
				
	def start(self,movie=None,autoSottotitoli=False):
		self.data['out']=''
		self.data['err']=''
		if(autoSottotitoli==True):
			sottotitoli = os.path.splitext(movie)[0]+'.srt'
			try: self.data['pipe'] = subprocess.Popen(["omxplayer",movie,"--subtitles",sottotitoli],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			except: self.data['err'] = '\n Error opening pipe\n'
		else:
			try: self.data['pipe'] = subprocess.Popen(["omxplayer",movie],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			except: self.data['err'] = '\n Error opening pipe\n'
	def err(self):
		if 'err' in self.data:
			return self.data['err']
		else: return ''
	def read(self):
		if 'pipe' in self.data:
			p = self.data['pipe']
			self.data['err']=''
			try:
				if(c!=None): self.send(cs=c)
				print 'select',select.select([p.stdout],[],[],0)[0]!=[]
				while select.select([p.stdout],[],[],0)[0]!=[] or select.select([p.stderr],[],[],0)[0]!=[]:
					if(select.select([p.stdout],[],[],0)[0]!=[]): self.data['out']+=p.stdout.read(1)
					if(select.select([p.stderr],[],[],0)[0]!=[]): self.data['out']+=p.stderr.read(1)
			except: self.data['err'] = '\n Error reading pipe \n '
			return self.data['out']
		else:
			return ''
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
		<h3>OMXPlayer status</h3>
		<pre id="omxout">Loading..</pre>
		<pre id="omxstatus">Loading..</pre>
			<button id="" value="j">[&lt;</button>
			<button id="" value="U">&lt;</button>
			<button id="" value="R">&lt;</button>
			<button id="" value=" ">||/&gt;</button>
			<button id="" value="L">&gt;</button>
			<button id="" value="D">&gt;</button>
			<button id="" value="k">&gt;]</button>
			<button id="" value="1">+speed</button>
			<button id="" value="2">-speed</button>
			<br/>
			<button id="" value="-">-volume/button>
			<button id="" value="+">+volume</button>
			<button id="" value="j">&lt; audio stream</button>
			<button id="" value="k">&gt; audio stream</button>
			<br/>
			<button id="" value="n">&lt; subs stream</button>
			<button id="" value="m">&gt; subs stream</button>
			<button id="" value="d">+0.25s sync subs</button>
			<button id="" value="f">-0.25s sync subs</button>
			<button id="" value="s">no subs</button>
			<br/>
			<button id="" value="z">?</button>
			<button id="" value="q">quit</button>
		</article>
		<article>
			<h3> Data Selection </h3>
			<form method="POST" action="start" >
				<div id="fileBro"></div>
				<input type=text placeholder="Click to browse" name=mfile onclick='fileBrowserFromHidden(this); return false'>Browse files</button>
				<input type="checkbox">Auto select omonimus srt file (if your omxplayer supports it)</radio>
				<input type="checkbox"> audio HDMI</radio>
			</form>
		</article>
			<script>
				
				reloadEvery(currentApp,currentId,'read',{},'#omxout',1000)
				reloadEvery(currentApp,currentId,'err',{},'#omxstatus',1000)
			</script>
			
	"""
	
	


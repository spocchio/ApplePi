import web 

import WebApp
import os
import subprocess

import sys
import select

class OMXPlayer(WebApp.WebApp):
	isHTML=True
	mediadir = os.path.expanduser('~')
	def close(self):
		if 'pipe' in self.data:
			self.data['err']=''
			try: self.data['pipe'].close()
			except: self.data['err'] = '\n Error closing pipe\n'
	def send(self,c):
		if 'pipe' in self.data:
			self.data['err']=''
			try: 
				self.data['pipe'].stdin.write(c)
				print ''
				print 'writtin'
				print ''
			except: self.data['err'] = '\n Error writing to pipe\n'
				
	def start(self,movie=None,autoSottotitoli=False,hdmi=False):
		mediadir = self.mediadir
		self.data['out']=''
		self.data['err']=''
		basic = ["omxplayer",mediadir+movie]
		if(autoSottotitoli==True):
			sottotitoli = os.path.splitext(movie)[0]+'.srt'
			basic += ["--subtitles",sottotitoli]
		if(hdmi):
			basic += ["-o","hdmi"]
		print 'ezzecutin',basic
		subprocess.call(["killall"," omxplayer"])
		self.data['pipe'] = subprocess.Popen(basic,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		self.data['pipe'].stdin.write('.')
		self.data['out'] = 'omxplayer started'
		self.data['err'] = '\n Error opening pipe\n'

	def err(self):
		if 'err' in self.data:
			return self.data['err']
		else: return ''
	def read(self):
		if 'pipe' in self.data:
			p = self.data['pipe']
			self.data['err']=''
			e=''
			#print 'select',select.select([p.stdout],[],[],0)[0]!=[]
			#if True:
			try:
				while select.select([p.stdout],[],[],0)[0]!=[] or select.select([p.stderr],[],[],0)[0]!=[]:
					#print 'select1',select.select([p.stdout],[],[],0)[0]!=[]
					#print 'select2',select.select([p.stderr],[],[],0)[0]!=[]
					lenZeri = True
					if(select.select([p.stdout],[],[],0)[0]!=[]):
						c = p.stdout.read(1)
						print 'ridin ',c,len(c)
						if(len(c)>0):
							lenZeri = False
							#print '1',c,len(c),'%x' % ord(c),len(c)
							self.data['out']+=c
					if(select.select([p.stderr],[],[],0)[0]!=[]): 
						c= p.stderr.read(1)
						if(len(c)>0):
							lenZeri = False	
							#print '2',c,len(c),'%x' % ord(c),len(c)
							self.data['out']+=c
					if(lenZeri):
						break
			except e:
				self.data['err'] = '\n Error reading pipe '+str(e)+'\n '
			print 'selected o yeah ['+self.data['out']+']'
			#self.data['err'] = '\n Error reading pipe \n '
			return self.data['out']
		else:
			return 'pipe not present'
	def HTML(self,c=None):
		return """
			<style>
				pre {background-color: #222; color: #cfc; 
				width:100%;
				} 
				iframe{ border:0;}
				
			</style>
		<article>
		<h3>From here you can manage the running OMXPlayer.</h3>
		<p>Here is shown the OMXPlayer output
		<pre id="omxout">Loading..</pre>
		<pre id="omxstatus">Loading..</pre></p>
			<p> Here you can send an input to OMXPlayer</p>
			<button  value="j">[&lt;</button>
			<button  value="U">&lt;</button>
			<button  value="R">&lt;</button>
			<button  value=" ">||/&gt;</button>
			<button  value="L">&gt;</button>
			<button  value="D">&gt;</button>
			<button  value="k">&gt;]</button>
			<button  value="1">+speed</button>
			<button  value="2">-speed</button>
			<br/>
			<button  value="-">-volume/button>
			<button  value="+">+volume</button>
			<button  value="j">&lt; audio stream</button>
			<button  value="k">&gt; audio stream</button>
			<br/>
			<button  value="n">&lt; subs stream</button>
			<button  value="m">&gt; subs stream</button>
			<button  value="d">+0.25s sync subs</button>
			<button  value="f">-0.25s sync subs</button>
			<button  value="s">no subs</button>
			<br/>
			<button  value="z">?</button>
			<button  value="q">quit</button>
			
		</article>
		<article>
			<h3> Here you can choose a file to play with OMXPlayer </h3>
			<form method="POST"   enctype="multipart/form-data" action="/OMXPlayer//start" target="my_iframe"  >
				<div id="fileBro"></div>
				<p>
				First of all <b>click</b> here to choose a media file:
				<input type=text placeholder="Click to browse" name=movie onclick='fileBrowserFromHidden(this); return false'>
				</p><p>
				<input type="checkbox" name="autoSottotitoli">Automatically select the corresponding .srt file (if your omxplayer supports it)</radio>
				</p>
				<p>
				<input type="checkbox" name="hdmi">send audio to HDMI output</radio>
				</p>
				<p>
				<input type="submit" value="Play!">
				</p>
			</form>
			  <iframe name="my_iframe" src="about:blank"></iframe>

		</article>
			<script>
				$('button').click(function(){
					console.log($(this))
					console.log($(this).val())
					readHTML('send',{'c': $(this).val()},null)					
				})
				
				reloadEvery(currentApp,currentId,'read',{},'#omxout',1000)
				reloadEvery(currentApp,currentId,'err',{},'#omxstatus',1000)
			</script>
			
	"""
	
	


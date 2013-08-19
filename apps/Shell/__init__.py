import web

import re
import cgi

import WebApp
import os
import datetime
import subprocess

import sys
import select
import random

class Shell(WebApp.WebApp):
	isHTML=True
	keepInstance=True
	def close(self,app,id):
		if 'pipe' in self.data:
			try: 
				self.data['pipe'].kill()
			except: 
				self.data['out'] += '\n Error closing pipe\n'
		del WebApp.selfies[app][id]
		return '""'
	def send(self,cs):
		if 'pipe' in self.data:
			for c in cs:
				if(ord(c)==8):
					c=chr(127)#+'[D'
					self.data['out']=self.data['out'][:len(self.data['out'])-1]
				else:
					self.data['out']+=c
				try: self.data['pipe'].stdin.write(c)
				except: self.data['out'] += '\n Error writing to pipe\n'
				
	def get(self,c=None):
		self.getDiff(c=c)
		#print 'read:',self.data['out']
		while self.data['out'].rfind(chr(07)) != -1:
			pos = self.data['out'].rfind(chr(07))
			#print 'pos',pos
			pos2 = self.data['out'][:pos].rfind(chr(10))
			#print 'pos2',pos2
			if(pos2==-1): pos2=0
			#print 'pos2',pos2
			self.data['out'] = self.data['out'][:pos2+1]+self.data['out'][pos+1:]
			#print 'new read',self.data['out']

		return self.data['out']
	def getDiff(self,c=None):
		
		if 'pipe' not in self.data:
			self.data['out']=''
			self.data['diff']=''
			#self.data['outFile']='tmp/typeScript.'+str(random.random())
			#try: self.data['pipe'] = subprocess.Popen(["script","-f","-q","-c","bash -i"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			#try: self.data['pipe'] = subprocess.Popen(["script","-f","-q","-c","bash -i"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			try: self.data['pipe'] = subprocess.Popen(["script","-f","-q","-c","bash -i"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			except: self.data['out'] += '\n Error opening pipe\n'

			#self.data['pipe'] = subprocess.Popen(["script","-f","-c","bash -i -l -v",self.data['outFile']],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			#self.data['pipe'] = subprocess.Popen(["script","-c","bash -i"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		p = self.data['pipe']
		try:
			if(c!=None): self.send(cs=c)
			self.data['diff'] = ''
			#print 'select',select.select([p.stdout],[],[],0)[0]!=[]
			while select.select([p.stdout],[],[],0)[0]!=[] or select.select([p.stderr],[],[],0)[0]!=[]:
				readed = False
				if(select.select([p.stdout],[],[],0)[0]!=[]): 
					data = p.stdout.read(1)
					if(len(data)>0):
						self.data['diff']+=data
						readed = True
				if(select.select([p.stderr],[],[],0)[0]!=[]):
					data = p.stdout.read(1)
					if(len(data)>0):
						self.data['diff']+=p.stderr.read(1)
						readed = True
				if (not readed):
					break
		except: self.data['out'] += '\n Error reading pipe \n '
		self.data['out']+=self.data['diff']
		"""
		try:self.data['out'] = open(self.data['outFile']).read()
		except: pass
		"""
		
		return self.data['diff']
	def getHTML(self,c=None):
		dato = self.get(c)
		#print 'dato',dato
		return deansi(dato)
	def getDiffHTML(self,c=None):
		dato = self.getDiff(c=c)
		#print 'dato',dato
		return deansi(dato)
	def HTML(self,c=None):
		return """
			<style>
			#scatola { background-color: #222; color: #cfc; 
			width:100%;
			height:90%;
			overflow: scroll;
			} 
//			input { height:8%}
			"""+styleSheet()+"""
			</style>
			<article>
			<h3>This is a web shell, type the commands in the black box</h3>
			<pre id="scatola" contenteditable="true">"""+deansi(self.get())+"""</pre>
			If you have troubles inserting text (e.g. pasting), try this input: <input type=text id="raw" placeholder="paste here"   />
			<input type="submit" id="sendRaw" value="send"/>
			
			</article>
			<script>
				$('#sendRaw').click(function(e){
					readHTML('send', {'cs':$('#raw').val() },null)					
				})
				$('#scatola')[0].sposta = function(){
										lc = $('#scatola :last-child')
										//onsole.log('lc.get0')
										//console.log(lc.get(0))
										//console.log('parentame')
										//console.log(document.activeElement)
						
										if(document.activeElement == lc.parent().get(0)){
											placeCaretAtEnd(lc.get(0));
										}
										//console.log(lc.parent().get(0))
									    $('#scatola').scrollTop($('#scatola')[0].scrollHeight);

						}
				reloadEvery(currentApp,currentId,'getHTML',{},'#scatola',1000,$('#scatola')[0].sposta)
				$('#scatola').keydown(function(e) {
					//console.log(e)
					code = e.keyCode
					if(code==8) {
						readHTML('send',{'cs': String.fromCharCode(8)},null)
					}
				})
				$('#scatola').keypress(function(e){
					//console.log(e)
					code = e.keyCode
					if(code==13) {
					 code=10
					}
					c = String.fromCharCode(code)
					readHTML('send',{'cs': c},null)
						
				})
				function placeCaretAtEnd(el) {
					el.focus();
					if (typeof window.getSelection != "undefined"
							&& typeof document.createRange != "undefined") {
						var range = document.createRange();
						range.selectNodeContents(el);
						range.collapse(false);
						var sel = window.getSelection();
						sel.removeAllRanges();
						sel.addRange(range);
					} else if (typeof document.body.createTextRange != "undefined") {
						var textRange = document.body.createTextRange();
						textRange.moveToElementText(el);
						textRange.collapse(false);
						textRange.select();
					}
				}
			</script>
			
	"""
	
	

# script stolen from https://raw.github.com/vokimon/python-service/master/deansi.py by  David Garcia Garzon

# TODO: Support empty m, being like 0m
# TODO: Support 38 and 38 (next attrib is a 256 palette color (xterm?))
# TODO: Support 51-55 decorations (framed, encircled, overlined, no frame/encircled, no overline)


colorCodes = {
	0 : 'black',
	1 : 'red',
	2 : 'green',
	3 : 'yellow',
	4 : 'blue',
	5 : 'magenta',
	6 : 'cyan',
	7 :	'white',
}
attribCodes = {
	1 : 'bright',
	2 : 'faint',
	3 : 'italic',
	4 : 'underscore',
	5 : 'blink',
# TODO: Chek that 6 is ignored on enable and disable or enable it
#	6 : 'blink_rapid',
	7 : 'reverse',
	8 : 'hide',
	9 : 'strike',
}

variations = [ # normal, pale, bright
	('black', 'black', 'gray'), 
	('red', 'darkred', 'red'), 
	('green', 'darkgreen', 'green'), 
	('yellow', 'orange', 'yellow'), 
	('blue', 'darkblue', 'blue'), 
	('magenta', 'purple', 'magenta'), 
	('cyan', 'darkcyan', 'cyan'), 
	('white', 'lightgray', 'white'), 
]

def styleSheet(brightColors=True) :
	"""\
	Returns a minimal css stylesheet so that deansi output 
	could be displayed properly in a browser.
	You can append more rules to modify this default
	stylesheet.

	brightColors: set it to False to use the same color
		when bright attribute is set and when not.
	"""

	simpleColors = [
		".ansi_%s { color: %s; }" % (normal, normal)
		for normal, pale, bright in variations]
	paleColors = [
		".ansi_%s { color: %s; }" % (normal, pale)
		for normal, pale, bright in variations]
	lightColors = [
		".ansi_bright.ansi_%s { color: %s; }" % (normal, bright)
		for normal, pale, bright in variations]
	bgcolors = [
		".ansi_bg%s { background-color: %s; }" % (normal, normal)
		for normal, pale, bright in variations]

	attributes = [
		".ansi_bright { font-weight: bold; }",
		".ansi_faint { opacity: .5; }",
		".ansi_italic { font-style: italic; }",
		".ansi_underscore { text-decoration: underline; }",
		".ansi_blink { text-decoration: blink; }",
		".ansi_reverse { border: 1pt solid; }",
		".ansi_hide { opacity: 0; }",
		".ansi_strike { text-decoration: line-through; }",
	]

	return '\n'.join(
		[ ".ansi_terminal { white-space: pre; font-family: monospace; }", ]
		+ (paleColors+lightColors if brightColors else simpleColors)
		+ bgcolors
		+ attributes
		)

def ansiAttributes(block) :
	"""Given a sequence "[XX;XX;XXmMy Text", where XX are ansi 
	attribute codes, returns a tuple with the list of extracted
	ansi codes and the remaining text 'My Text'"""

	attributeRe = re.compile( r'^[[](\d+(?:;\d+)*)?m')
	match = attributeRe.match(block)
	if not match : return [], block
	if match.group(1) is None : return [0], block[2:]
	return [int(code) for code in match.group(1).split(";")], block[match.end(1)+1:]


def ansiState(code, attribs, fg, bg) :
	"""Keeps track of the ansi attribute state given a new code"""

	if code == 0 : return set(), None, None   # reset all
	if code == 39 : return attribs, None, bg   # default fg
	if code == 49 : return attribs, fg, None   # default bg
	# foreground color
	if code in xrange(30,38) :
		return attribs, colorCodes[code-30], bg
	# background color
	if code in xrange(40,48) :
		return attribs, fg, colorCodes[code-40]
	# attribute setting
	if code in attribCodes :
		attribs.add(attribCodes[code])
	# attribute resetting
	if code in xrange(21,30) and code-20 in attribCodes :
		toRemove = attribCodes[code-20] 
		if toRemove in attribs :
			attribs.remove(toRemove)
	return attribs, fg, bg


def stateToClasses(attribs, fg, bg) :
	"""Returns css class names given a given ansi attribute state"""

	return " ".join(
		["ansi_"+attrib for attrib in sorted(attribs)]
		+ (["ansi_"+fg] if fg else [])
		+ (["ansi_bg"+bg] if bg else [])
		)

def deansi(text) :
	text = cgi.escape(text)
	blocks = text.split("\033")
	state = set(), None, None
	ansiBlocks = blocks[:1]
	for block in blocks[1:] :
		attributeCodes, plain = ansiAttributes(block)
		for code in attributeCodes : state = ansiState(code, *state)
		classes = stateToClasses(*state)
		ansiBlocks.append(
			(("<span class='%s'>"%classes) + plain + "</span>")
			if classes else "<span>"+plain+"</span>"
			)
	text = "".join(ansiBlocks)
	return text

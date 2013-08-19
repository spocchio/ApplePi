import web 

import WebApp
import os
import datetime


class SystemMonitor(WebApp.WebApp):
	isHTML=True
#http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=22180
	def getCPUtemperature(self):
		res = os.popen('vcgencmd measure_temp').readline()
		return(res.replace("temp=","").replace("'C\n",""))
# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
	def getRAMinfo(self):
		p = os.popen('free')
		i = 0
		while 1:
			i = i + 1
			line = p.readline()
			if i==2:
				return(line.split()[1:4])

# Return % of CPU used by user as a character string                                
        def getCPUuse(self):
                return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
        )))
        def getExternalDevices(self):
                return(str(os.popen("df -h /media/* | grep -v /dev/root | tail -n +2").read().strip(\
        )))
	def getDevices(self):
		return(str(os.popen("mount").readline().strip(\
	)))
# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
	def getDiskSpace(self):
		p = os.popen("df -h /")
		i = 0
		while 1:
			i = i +1
			line = p.readline()
			if i==2:
				return(line.split()[1:5])
	def infoHTML(self):
		# CPU informatiom
		CPU_temp = self.getCPUtemperature()
		CPU_usage = self.getCPUuse()

		# RAM information
		# Output is in kb, here I convert it in Mb for readability
		RAM_stats = self.getRAMinfo()
		RAM_total = round(int(RAM_stats[0]) / 1000,1)
		RAM_used = round(int(RAM_stats[1]) / 1000,1)
		RAM_free = round(int(RAM_stats[2]) / 1000,1)

		# Disk information
		DISK_stats = self.getDiskSpace()
		DISK_total = DISK_stats[0]
		DISK_free = DISK_stats[1]
		DISK_perc = DISK_stats[3]


		
		res=	"<h2> Here are listed some realtime informations about your Pi</h2>"
		res+=   "<article><h3>CPU</h3><p><b>Usage</b>:"+str(CPU_usage)+"</p>"
		res+=	"<p><b>Temperature</b>:"+str(CPU_temp)+"</p></article>"
		res+=	"<article><h3>Memory</h3><p><b>Total</b>:"+str(RAM_total)+"</p>"
		res+=	"<p><b>Used</b>:"+str(RAM_used)+"</p>"
		res+=	"<p><b>Free</b>:"+str(RAM_free)+"</p></article>"
		res+=	"<article><h3>Disk</h3><p><b>Total</b>:"+str(DISK_total)+"</p>"
		res+=	"<p><b>Free</b>:"+str(DISK_free)+" ("
		res+=	str(DISK_perc)+")</p></article>"
		res+=   "<article><h3>System</h3><p><b>Time:</b>"+str(datetime.datetime.now())+"</p>"

		res+=   "<b>Mounted devices:</b><pre>"+str(self.getExternalDevices())+"</pre></article>"
		return res
	def HTML(self):
		#return "<div onload='readFrom(this,\"PiInfo\",\"infoHTML\",{})'></div>"
		return "<div id='content'>"+self.infoHTML()+"""</div>
		
			<script>
				reloadEvery(currentApp,currentId,'infoHTML',{},'#content',1000)
			</script>
			
		"""


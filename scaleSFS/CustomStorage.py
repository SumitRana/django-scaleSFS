from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from .Connector import CustomStorage

# configuration
# server tuple = ("ip","port","base path","user",current or not boolean,"identity_key path","password")
StaticServers = (('http://10.5.50.1:80','/var/www/','ubuntu',False,None,"password"),
				 ('http://10.5.50.1:80','/var/www/','ubuntu',False,"/path/to/pem/sam.pem",None))
# Author - Sumit | Sam

class CustomStorage(FileSystemStorage):

	rc = None
	currentFileServer = None

	def __init__(self):
		for server in StaticServers:
			if server[3]== True:
				self.currentFileServer = server

	def _save(self,name,content):
		if self.exists(name):
			self.delete(name)

		# name = "@"+current_ip+":"+current_ip_port+"@"+"/"+str(name)
		name = str(self.currentFileServer[0])+str(name)

		parts = str(name).split("/")
		filename = parts[len(parts)-1]
		folders = parts.remove(filename)

		# Making file buffer
		with open(settings.BASE_DIR+"/"+filename,"wb+") as f:
			for chunk in content.chunks():
				print("writing chunk")
				f.write(chunk)

		# uploading file to current remote server
		self.rc = RemoteConnection(ip_address=self.currentFileServer[0],username=self.currentFileServer[2],
									identity_key=self.currentFileServer[4],password=self.currentFileServer[5])
		rt = self.rc.put_file(settings.BASE_DIR+"/"+filename,"/home/ubuntu/",name)
		# deleting file buffer
		if rt is True:
			os.remove(settings.BASE_DIR+"/"+filename)

		return name

	def exists(self,name):
		return False

	def delete(self,name):
		pass

	def listdir(self,path):
		pass

	def size(self,name):
		pass

	def url(self,name):
		# return str("/media/"+name)
		# return str(protocol+"://"+str(current_ip)+":"+str(current_ip_port)+"/"+name)
		return name

	def get_availaible_name(self,name):
		return name
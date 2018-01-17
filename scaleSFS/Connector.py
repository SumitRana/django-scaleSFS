# Author - Sumit | Sam

import paramiko

class RemoteConnection:
	client = None
	ftp_client = None

	def __init__(self,ip_address=None,username=None,password=None,identity_key=None):
		if ip_address is not None and username is not None:
			self.client = paramiko.client.SSHClient()
			self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())#trusting system - for first time
			if (password is None) and (identity_key is not None):
				#connect with private key
				ikey = paramiko.RSAKey.from_private_key_file(identity_key)
				self.client.connect(hostname=ip_address,username=username,password=password,pkey=ikey)
			else:
				#connect with password
				self.client.connect(hostname=ip_address,username=username,password=password)
		else:
			raise Exception('ip_address and username cannot be None')

	def open_file_channel(self):
		self.ftp_client = self.client.open_sftp()
		return True

	def get_file(self,filename):
		if self.ftp_client is not None:
			self.open_file_channel()
		return True

	def put_file(self,localpath,rootpath,remotepath):
		if self.ftp_client is None:
			self.open_file_channel()
		# content/2017/add.png
		parts = str(remotepath).split("/")
		temppath = rootpath
		for folder in parts[0:len(parts)-1]:
			self.client.exec_command("cd "+temppath+";mkdir "+str(folder))
			i,o,e = self.client.exec_command("cd "+temppath+"/"+folder+";pwd")
			p = str(o.read())
			temppath = p.split("\n")[0]

		try:
			self.ftp_client.put(localpath,rootpath+remotepath)
			return True
		except Exception as e:
			return str(e)

	def __del__(self):
		try:
			if ftp_client is not None:
				ftp_client.close()

			if client is not None:
				client.close()
		except Exception:
			pass
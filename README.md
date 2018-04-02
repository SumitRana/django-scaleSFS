## django-scaleSFS

django-scaleSFS is a django based library which lets to scale your file system ( media files ) ,
across multiple servers .

The app distributes files to the servers listed by you in the settings file , thus taking care of the location 
of the file and providing a easy access link with the django-orm .


#### Quick start
-----------

1. Changes in settings.py :

	```python

		StaticServers = (('http','10.5.50.1','80','/var/www/','ubuntu',False,None,"password"), ..)
		DEFAULT_FILE_STORAGE = "scaleSFS.CustomStorage.CustomStorage"

	```




#### Project Architecture

<img src="arch.jpg"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
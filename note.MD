## django-admin startproject projectname 
## python manage.py runserver 
## Start a new app 
## python manage.py startapp appname

## Django Load to the VirtualEnv Dir cannot read the template 
https://stackoverflow.com/questions/50294869/django-looks-for-templates-in-my-envs-folder-django-admin

Django was looking for templates in my venv dir (my virtual environment dir) too, in my case, I solved it after I added my app in the settings file of the main project dir.

Basically in your app dir, there's an apps.py file which has a class named *YOURAPPNAME*Config. In my case, the app is accounts so the class is AccountsConfig. Then go into your main project dir, which is located in same directory as your manage.py file, open settings.py, scroll down to INSTALLED_APPS and add your class there. For me it would be accounts.apps.AccountsConfig
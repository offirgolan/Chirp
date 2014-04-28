Chirp
=====

Live Demo:
----------

http://chirp-offirgolan.rhcloud.com/

Feel free to make a dummy account and chirp away :)

About
-----

This is a twitter clone written for Django 1.6 with python 2.7. It is ready to be deployed on the openshift servers. 

* Django 1.6 w/ Python 2.7
* SQLite 3 DB
* Ready for Deployment to RedHat's openshift servers


Features
--------

* Login
* Signup
* Auto-updated views 
* Dashboard view
	* View your own chirps, chirps you have been tagged in, and chirps of users you are following
* Profile view
	* View public user chirps 
	* Follow / Unfollow
* Hashtag view
	* Displays all chirps for the given hashtag 
* Settings
	* Change email, first, and last name
	* Change / Upload profile picture
* Compose
	* 140 max characters
	* Autocomplete for users and hashtags (start by typing @ or # and one more characters)
* Search
	* Site wide autocomplete search for users and hashtags
* Admin panel for managing users, tags, chirps, etc. 


Setup Local Environment
-----------------------

1) Create the python virtual enviroment 

```
 $ virtualenv venv --no-site-packages
 $ source venv/bin/activate
 $ python setup.py install
```

2) Setup admin username and password
In Chirp/wsgi/openshift

```
 $ python manage.py changepassword admin
 $ Changing password for user 'admin'
 $ Password: 
 $ Password (again):
```

3) Setup the DB
In Chirp/wsgi/openshift

```
 $ python manage.py syncdb
```

4) Run the server
In Chirp/wsgi/openshift

```
 $ python manage.py runserver
```

5) In your browser, go to http://localhost:8000/ for the web application or http://localhost:8000/admin for the admin panel
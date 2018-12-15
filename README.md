# mezzsite
mezzanine site

# installation

## ubuntu
```
apt install python3
apt install python3-pip
apt install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install mezzanine
```
# create a project
```
$ mezzanine-project wfblog
$ cd wfblog
```

# Create a database
```
$ python manage.py createdb
```
# Run the web server
```
$ python manage.py runserver 0.0.0.0:80
```
# FAQ

* Q. UserWarning: You haven't defined the ALLOWED_HOSTS settings, which Django requires. Will fall back to the domains configured as sites.

A.
if you are just doing development, simply add the following address into wfblog/settings.py

ALLOWED_HOSTS = [\'*\']

it will fix your problem.(https://docs.djangoproject.com/en/dev/ref/settings/#core-settings)

For production, you will need to define it with the host/domain names that your project is allowed to serve. This is a security feature.

https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts

Or set DEBUG=True

# Reference

* http://mezzanine.jupo.org/docs/

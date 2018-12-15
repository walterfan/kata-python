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

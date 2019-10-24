# Backend - Face-recognition Based Attendance Taking System 

## Setup

First, make sure you have `python3` installed.

Using `virtualenv` is recommended. To create and activate a `virtualenv`:

```sh
virtualenv env
source env/bin/activate
```

To install all required packages, run
```sh
pip install -r requirements.txt
```

To start the development server, run

```sh
python manage.py. runserver
```


## Test
run tests
```
$ python manage.py test
```

run coverage
```
$ coverage run manage.py test
$ coverage report
```

generate html report
```
$ coverage run manage.py test && coverage html
```
open htmlcov/index.html

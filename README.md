# Simple Flask CRUD Web Application
This is a very simple Flask Application where user can log in and create posts.

## Application Breakdown
This is the breakdown of a fairly simple Flask Application using a [SQLite](https://www.sqlite.org/index.html) database
```
Flask-on
│   README.md
│   FlaskDeployment.md
│   .gitignore
│
└───flask_app
│   │   __init__.py
│   │   forms.py
│   │   models.py
│   │   routes.py
│   │   requriments.txt
│   │   site.db
│   │
│   └───static
│   │   │   ...
│   │
│   └───templates
│   │   │   ...

```

## Flask Frameworks
These are the [Flask](http://flask.pocoo.org/docs/1.0/) libraries used in this Project. You'll find these in the requirements.txt file.
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
- [Flask-Security](https://pythonhosted.org/Flask-Security/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)

## Deploying Locally
Lets walk through setting up your development environment and deploying this application on your local machine

1. Install Python, pip, and virtualenv
  - [Python](https://www.python.org/)
  - [pip](https://pip.pypa.io/en/stable/installing/)
  - [Virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

2. Clone this repo and CD into the projects directory
```
git clone https://github.com/RaiderHacks/RaiderHacks-Website-2.0 flask_app_project
cd flask_app_project
```
3. Create and activate a virtualenv
```
virtualenv venv
source venv/bin/activate

windows
venv\Scripts\activate
```
4. Install packages
```
pip install -r flask_app/requirements.txt
```
5. Create Flask environment variables
```
export FLASK_APP=flask_app/__init__.py
export FLASK_ENV=development

Windows:

  $env:FLASK_APP = "__init__.py"
  go to flas_app document
  python -m flask run
```
6. Run it
```
flask run
```

## How to actually run on windows
1. Navigate to project directory
2. Make sure that you open project in powershell 
3. Update git
```bash
git pull
``` 
4. Create virtualenv if one does not exist
```bash
virtualenv [name of virtual env]
``` 
5. Activate the virtualenv
```bash
.\env\Scripts\activate
```
6. install requirmets using 
```bash
pip install -r requirements.txt
```
7. set environment vars
```bash
  $env:FLASK_APP = "__init__.py"
``` 

8. Move into app directory 
```bash
    flask run
```
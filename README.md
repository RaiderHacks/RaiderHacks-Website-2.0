# Simple Flask CRUD Web Application
This is a very simple Flask Application where user can log in and create posts.
To submit push requets, your public key

## Application Breakdown
This is the breakdown of a fairly simple Flask Application using a [SQLite](https://www.sqlite.org/index.html) database
```
raider_hacks
│   ├── __init__.py
│   ├── auth
│   │   ├── routes.py
│   │   └── templates
│   │       └── auth
│   │           ├── login.html
│   │           └── register.html
│   ├── blog
│   │   ├── routes.py
│   │   └── templates
│   │       └── blog
│   │           └── blog.html
│   ├── forms.py
│   ├── main.py
│   ├── models.py
│   ├── posts
│   │   ├── routes.py
│   │   └── templates
│   │       └── posts
│   │           ├── create_post.html
│   │           └── post.html
│   ├── requirements.txt
│   ├── site.db
│   ├── static
│   │   ├── images
│   │   ├── scripts
│   │   │   └── messages.js
│   │   └── styles
│   │       ├── footer.css
│   │       ├── global.css
│   │       ├── login.css
│   │       ├── members.css
│   │       ├── navbar.css
│   │       └── register.css
│   └── templates
│       ├── addachievements.html
│       ├── includes
│       │   ├── _footer.html
│       │   ├── _messages.html
│       │   └── _navbar.html
│       ├── index.html
│       ├── layout.html
│       ├── login.html
│       └── members.html
```


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
```
4. Install packages
```
pip install -r requirements.txt
```
5. Create Flask environment variables
```
export FLASK_APP=raider_hacks/__init__.py
export FLASK_ENV=development
Windows:
  $env:FLASK_APP = "__init__.py"
  python -m flask run
```
6. Run it
```
flask run
```

## useful sqlite3 scripts
update user permissions 
```
 update user set permissions = '3' where id = '1';
```
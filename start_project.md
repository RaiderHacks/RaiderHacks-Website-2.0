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


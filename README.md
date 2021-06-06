# Born_to_Blog_Project
<h2>A Blog Site made using Flask</h2>

* The site uses Sqlite DB and HTML,CSS frontend.

* It also requires a python virtual environment.

<h3>Steps to launch the site(locally):</h3>

<b>1) Create a python virtual environment in the enclosing folder.</b>

   (Make sure you hvae the virtualenv package)

   In the terminal,
```python
virtualenv -p python3 envname
```

<b>2) Activate the virtual environment you just created.</b>

```python
source envname/bin/activate
```

<b>3) Install the required packages</b>

```python
pip3 install -r requirements.txt
```

If required, choose the appropriate python interpreter from source/bin/

<b>4) Generate a Key (required as part of Flask app configuration)</b>

In python console,
```python
import secrets
secrets.token_hex(16)
```

Make note of the key generated above.



<b>5) Set Environment Variables that contain the configuration information</b>

| Key                       | Value                                                | 
| --------------------------|:----------------------------------------------------:| 
| FLASKBLOG_SECRET_KEY      | The key you just generated                           | 
| FLASKBLOG_DEV_DB_URI      | sqlite:///site.db                                    | 
| MAIL_USERNAME             | A gmail id from which to send mails to contributors  | 
| MAIL_PASSWORD             | Password of the mail id provided above               | 

Note: U can use a fresh databse for the site, by deleting the site.db file in the folder, and using the following commands,to create a new database with no initial data.

```python
from flaskblog import db
db.create_all()
```

<b>6) Launch the site using the following command</b>

```python
python3 run.py
```

The site will be launched at http://localhost:5000/



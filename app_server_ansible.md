# Doing ansible role for app server

## Files

Modify the code to provide enviroment variables and add it to the role files.

```
from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

conn = psycopg2.connect(
    dbname=os.getenv("postgresql_db"),
    user=os.getenv("postgresql_user"),
    password=os.getenv("postgresql_password"),
    host=os.getenv("postgresql_ip")
)

@app.route("/")
def home():
    return "App server running"

@app.route("/data")
def data():
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    result = cur.fetchone()
    return jsonify({"time": str(result[0])})

app.run(host="0.0.0.0", port=5000)
```



## Tasks

I'm goin through what every task does.

### Install required packages

Does apt update and installs/checks that python3 and python3-pip are present.

### Create application directory

Creates directory for our app and sets permissions. We are using /opt/app so it's not tied to specific user

### Create vitual environment

We couldn't install some pip packages without virtual environment so we're also doing it here. We create a isolated Python environment at /opt/app/venv

### Install python dependencies

Installs Flask and psycopg2 which is a PostgreSQL driver, inside virtual environment, not in system Python.

### Copy app file

Copies our code to the directory we created earlier and gives permissions.

### Create systemd service file

Takes the template we created and generates a systemd service file. If changes were made to the template file it notifys a handler to reload systemd and restart the app.

### Enable and start the service we created in the last task

Ensures app is started and enabled.

## Handlers

## Template

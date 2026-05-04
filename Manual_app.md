# Creating app that utilises the DB server

Install dependencies.

```
sudo apt update
sudo apt install python3 python3-pip -y
```

Install python libraries that we use, you will need to setup a virtual environment to be able to do the install.

Go to your project directory and do the following commands.

```
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install flask psycopg2-binary
```

Create a python function that creates a webserver using Flask that listens to HTTP requests, connects to a PostgreSQL database and returns data from the DB as JSON.

```
micro flaski.py
```

We used the following program (ChatGPT)

```
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="mydb",
    user="app_user",
    password="password",
    host="DB_SERVER_IP"
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

Now in our original manual postgresql setup .conf files we add

change postgresql.conf

```
listen_addresses = '*'
```

change pg_hba.conf

```
host    projekti    mini    APP_SERVER_IP/32    md5
```

change postgres section in /etc/nftables.conf

```
ip addr APP_SERVER_IP tcp dport 5432 accept
```

Test by running the flaski.py program.

Then in your browser enter

```
http://127.0.0.1:5000/data
```

You should then get the current time given by our database!


from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "App server running"

@app.route("/data")
def data():
    conn = psycopg2.connect(
        dbname=os.getenv("postgresql_db"),
        user=os.getenv("postgresql_user"),
        password=os.getenv("postgresql_password"),
        host=os.getenv("postgresql_ip")
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    result = cur.fetchone()

    cur.close()
    conn.close()
    
    return jsonify({"time": str(result[0])})

app.run(host="0.0.0.0", port=5000)

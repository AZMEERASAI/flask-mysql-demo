from flask import Flask, jsonify
import os
import pymysql

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "demo_user")
DB_PASS = os.environ.get("DB_PASS", "demo_pass")
DB_NAME = os.environ.get("DB_NAME", "demo_db")

@app.route("/")
def hello():
    return "Hello from Flask!"

@app.route("/db")
def test_db():
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME, connect_timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT VERSION();")
        ver = cur.fetchone()
        conn.close()
        return jsonify({"mysql_version": ver[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

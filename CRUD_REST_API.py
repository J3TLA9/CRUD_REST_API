from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin"
app.config["MYSQL_DB"] = "car_hire"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def main_page():
    html = '''
    <p>Welcome to Car Hire Database</p>
    <a href="/customer">
    <button>Customer</button>
    </a>
    '''
    return html

@app.route("/customer", methods=["GET"])
def get_customer():
    data = data_fetch('''
    select * from customer
    ''')
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)
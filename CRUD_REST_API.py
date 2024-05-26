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
    <a href="/customer/create">
    <button>Create Customer</button>
    <p></p>
    </a>
    <a href="/customer">
    <button>Read Customer</button>
    </a>
    '''
    return html


@app.route("/customer/create")
def customer_page():
    form_html = '''
    <h2>Add Customer</h2>
    <form action="/customer" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        
        <label for="gender">Gender:</label>
        <input type="text" id="gender" name="gender" required><br><br>
        
        <label for="email_address">Email Address:</label>
        <input type="email" id="email_address" name="email_address" required><br><br>
        
        <label for="phone_number">Phone Number:</label>
        <input type="tel" id="phone_number" name="phone_number" required><br><br>
        
        <label for="country">Country:</label>
        <input type="text" id="country" name="country" required><br><br>
        
        <label for="province">Province:</label>
        <input type="text" id="province" name="province" required><br><br>
        
        <label for="municipality">Municipality:</label>
        <input type="text" id="municipality" name="municipality" required><br><br>
        
        <label for="address">Address:</label>
        <input type="text" id="address" name="address" required><br><br>
        
        <input type="submit" value="Submit">
        
    </form>
    <a href="/">
    <button>Go Back</button>
    </a>
    '''
    return form_html

@app.route("/customer", methods=["GET"])
def get_customer():
    data = data_fetch('''
    select * from customer
    ''')
    return make_response(jsonify(data), 200)

@app.route("/customer", methods=["POST"])
def add_customer():
    name = request.form.get("name")
    gender = request.form.get("gender")
    email_address = request.form.get("email_address")
    phone_number = request.form.get("phone_number")
    country = request.form.get("country")
    province = request.form.get("province")
    municipality = request.form.get("municipality")
    address = request.form.get("address")
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT MAX(customer_id) FROM customer")
    max_id_result = cur.fetchone()

    print("max_id_result:", max_id_result)


    if max_id_result and max_id_result['MAX(customer_id)'] is not None:
        new_customer_id = max_id_result['MAX(customer_id)'] + 1
    else:
        new_customer_id = 1
    
    cur.execute(
        """INSERT INTO customer (customer_id, customer_name, gender, email_address, phone_number, country, province, municipality, address) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (new_customer_id, name, gender, email_address, phone_number, country, province, municipality, address),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    
    return make_response(
        jsonify(
            {"message": "customer added successfully", "rows_affected": rows_affected}
        ),
        201,
    )



if __name__ == "__main__":
    app.run(debug=True)
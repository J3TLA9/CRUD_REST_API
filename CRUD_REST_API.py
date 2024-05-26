from flask import Flask, make_response, jsonify, request, redirect, url_for
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
    </a>
    <p></p>
    <a href="/customer/read">
    <button>Read Customer</button>
    </a>
    <p></p>
    </a>
    <a href="/customer/update">
    <button>Edit Customer</button>
    </a>
    '''
    return html


@app.route("/customer/create")
def customer_create_page():
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
@app.route("/customer/read")
def customer_read_page():
    html = '''
    <a href="/customer">
    <button>Customer List</button>
    </a>
    <p></p>
    <form action="/customer/search/ID" method="get">
        <label for="search">Find by ID:</label>
        <input type="number" id="searchID" name="search" min="1">
        <button type="submit">Search</button>
    </form>
    <form action="/customer/search/name" method="get" onsubmit="return validateSearch()">
        <label for="searchName">Find:</label>
        <input type="text" id="searchName" name="search">
        <button type="submit">Search</button>
    </form>
    <p></p>
    <a href="/">
    <button>Go Back</button>
    </a>
    <script>
        function validateSearch() {
            var searchNameInput = document.getElementById("searchName").value;
            if (containsNonDigit(searchNameInput)) {
                return true;
            } else {
                alert("Input contains only digit characters. Forbidding...");
                return false;
            }
        }

        function containsNonDigit(inputString) {
            for (var i = 0; i < inputString.length; i++) {
                if (isNaN(inputString[i]) && inputString[i] !== ' ') {
                    return true;
                }
            }
            return false;
        }
    </script>
    '''
    return html


@app.route("/customer/search/ID", methods=["GET"])
def customer_search_ID():
    search_query = request.args.get("search")
    return redirect(url_for("get_customer_by_id", id=search_query))

@app.route("/customer/search/name", methods=["GET"])
def customer_search_name():
    search_query = request.args.get("search")
    return redirect(url_for("get_customer_by_name", name=search_query))
    
@app.route("/customer/edit")
def customer_edit_page():
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

@app.route("/customer/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    data = data_fetch("""SELECT * FROM customer where customer_id = {}""".format(id))
    return make_response(jsonify(data), 200)

from flask import request

@app.route("/customer/<string:name>", methods=["GET"])
def get_customer_by_name(name):
    query = """
    SELECT *
    FROM customer
    WHERE 
        customer_name LIKE CONCAT('%', '{}', '%')
        OR gender LIKE CONCAT('%', '{}', '%')
        OR email_address LIKE CONCAT('%', '{}', '%')
        OR phone_number LIKE CONCAT('%', '{}', '%')
        OR country LIKE CONCAT('%', '{}', '%')
        OR province LIKE CONCAT('%', '{}', '%')
        OR municipality LIKE CONCAT('%', '{}', '%')
        OR address LIKE CONCAT('%', '{}', '%');
    """.format(name, name, name, name, name, name, name, name)
    
    data = data_fetch(query)
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

@app.route("/customer/<int:id>", methods=["PUT"])
def update_customer(id):
    name = request.form.get("name")
    gender = request.form.get("gender")
    email_address = request.form.get("email_address")
    phone_number = request.form.get("phone_number")
    country = request.form.get("country")
    province = request.form.get("province")
    municipality = request.form.get("municipality")
    address = request.form.get("address")
    cur = mysql.connection.cursor()
    cur.execute(
        """
        UPDATE customer 
        SET name = %s, gender = %s, email_address = %s, phone_number = %s, country = %s, province = %s, municipality = %s, address = %s
        WHERE customer_id = %s
        """,
        (name, gender, email_address, phone_number, country, province, municipality, address, id)
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    
    if rows_affected == 0:
        return jsonify({"message": "Customer not found"}), 404
    
    return make_response(
        jsonify(
            {"message": "Customer updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
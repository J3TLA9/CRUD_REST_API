import html
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
    
@app.route("/customer/update", methods=["GET", "POST"])
def customer_update_page():
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        query = f"SELECT * FROM customer WHERE customer_id = {customer_id}"
        data = data_fetch(query)
        if data:
            customer_data = data[0]
            form_html = f'''
            <form id="updateForm" onsubmit="submitForm(event)">
                <input type="hidden" name="customer_id" value="{customer_id}">
                <input type="hidden" name="_method" value="PUT"> <!-- Method override for PUT request -->
                <label for="customer_id">Customer ID: {customer_data['customer_id']}</label>
                <p></p>
                <label for="customer_name">Customer Name:</label>
                <input type="text" id="customer_name" name="customer_name" value="{customer_data['customer_name']}"><br>
                <label for="gender">Gender:</label>
                <input type="text" id="gender" name="gender" value="{customer_data['gender']}"><br>
                <label for="email_address">Email Address:</label>
                <input type="text" id="email_address" name="email_address" value="{customer_data['email_address']}"><br>
                <label for="phone_number">Phone Number:</label>
                <input type="text" id="phone_number" name="phone_number" value="{customer_data['phone_number']}"><br>
                <label for="country">Country:</label>
                <input type="text" id="country" name="country" value="{customer_data['country']}"><br>
                <label for="province">Province:</label>
                <input type="text" id="province" name="province" value="{customer_data['province']}"><br>
                <label for="municipality">Municipality:</label>
                <input type="text" id="municipality" name="municipality" value="{customer_data['municipality']}"><br>
                <label for="address">Address:</label>
                <input type="text" id="address" name="address" value="{customer_data['address']}"><br>
                <button type="submit">Update</button>
            </form>
            <a href="/customer/update">
                <button>Go Back</button>
            </a>
            '''
        else:
            form_html = '<p>No Customer Exists With That ID</p>'
    else:
        form_html = '''
        <form action="/customer/update" method="post">
            <label for="customer_id">Customer ID:</label>
            <input type="text" id="customer_id" name="customer_id">
            <button type="submit">Submit</button>
        </form>
        <a href="/">
        <button>Go Back</button>
        </a>
        '''
    return form_html + '''
    <script>
        function submitForm(event) {
            event.preventDefault();
            var formData = {};
            var formElements = document.getElementById("updateForm").elements;
            for (var i = 0; i < formElements.length; i++) {
                var element = formElements[i];
                if (element.name) {
                    formData[element.name] = element.value;
                }
            }
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/customer/" + formData.customer_id, true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        alert("Customer updated successfully");
                        window.location.reload(); // Refresh the page or perform any other action
                    } else {
                        alert("Failed to update customer");
                    }
                }
            };
            xhr.send(JSON.stringify(formData));
        }
    </script>
    '''


@app.route("/customer", methods=["GET"])
def get_customer():
    data = data_fetch("""
    select * from customer
    """)
    return html + make_response(jsonify(data), 200)

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
    
    html = """
    <p></p>
    <a href="/">
    <button>Go Back</button>
    </a>"""
    
    if not gender.isalpha():
        return "Invalid gender. Gender should only contain alphabetic characters." + html

    if not all(char.isdigit() or char == "+" for char in phone_number):
        return "Invalid phone number. Phone number should only contain digits and '+'." + html

    for field in [country, province, municipality]:
        if any(char.isdigit() for char in field):
            return f"Invalid {field}. {field} should not contain numbers." + html

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

@app.route("/customer/<int:id>", methods=["POST"])
def update_customer(id):
    data = request.json
    if data:
        customer_name = data.get("customer_name")
        gender = data.get("gender")
        email_address = data.get("email_address")
        phone_number = data.get("phone_number")
        country = data.get("country")
        province = data.get("province")
        municipality = data.get("municipality")
        address = data.get("address")

        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE customer 
            SET customer_name = %s, gender = %s, email_address = %s, phone_number = %s, country = %s, province = %s, municipality = %s, address = %s
            WHERE customer_id = %s
            """,
            (customer_name, gender, email_address, phone_number, country, province, municipality, address, id)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Customer updated successfully"}), 200
    else:
        return jsonify({"error": "No data provided"}), 400


if __name__ == "__main__":
    app.run(debug=True)
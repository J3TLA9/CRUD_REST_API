# CRUD_REST_API
 This is a final project for IT6

 
CRUD REST API
Overview
This CRUD REST API is built using Flask, a lightweight Python web framework. It provides endpoints for performing CRUD (Create, Read, Update, Delete) operations on a customer database. The API supports various functionalities such as adding, retrieving, updating, and deleting customer records.

Features
Create Customer: Add a new customer record to the database.
Read Customer: Retrieve customer records from the database.
Update Customer: Update existing customer records in the database.
Delete Customer: Remove customer records from the database.


Prerequiste:
Python
https://www.python.org/downloads/


Installation Process:
Step 1: Install Repository
git clone https://github.com/yourusername/crud-rest-api.git

Step 2: Open Command line on the same folder or navigate to the folder and enter:
cd crud-rest-api

Step 3: Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

Step 4: Install requirements
pip install -r requirements.txt

Step 5: Run Python
python CRUD_REST_API.py


API Endpoints
GET /customer: Retrieve customer records.
POST /customer: Add a new customer record.
PUT /customer/<customer_id>: Update an existing customer record.
DELETE /customer/<customer_id>: Delete a customer record.

Security
Authentication: Implement authentication using JWT (JSON Web Tokens) for securing endpoints.
Authorization: Ensure that only authenticated users with the appropriate permissions can access sensitive endpoints.
HTTPS: Enable HTTPS to encrypt data transmitted between clients and the server.
Input Validation: Validate and sanitize all input data to prevent common security vulnerabilities.

Testing
The API comes with a test suite to ensure its functionality and reliability. You can run the tests using the following command:
python TEST.py

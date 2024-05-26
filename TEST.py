import unittest
import warnings
from CRUD_REST_API import app

class appTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        warnings.simplefilter("ignore", category=DeprecationWarning)
        
    def test_main_page(self):
        self.maxDiff = None 
        expected_html = '''
    <p>Welcome to Car Hire Database</p>
    <a href="/customer/create">
    <button>Create Customer</button>
    </a>
    <p></p>
    <a href="/customer/read">
    <button>Read Customer</button>
    </a>
    <p></p>
    <a href="/customer/update">
    <button>Edit Customer</button>
    </a>
    <p></p>
    <a href="/customer/delete">
    <button>Delete Customer</button>
    </a>
    '''
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), expected_html)
        
    def test_getcustomers(self):
        response = self.app.get("/customer")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("test" in response.data.decode())
        
    def test_add_customer(self):
        data = {
            'name': 'John Doe',
            'gender': 'Male',
            'email_address': 'john@example.com',
            'phone_number': '+123456789',
            'country': 'USA',
            'province': 'California',
            'municipality': 'Los Angeles',
            'address': '123 Main St'
        }
        response = self.app.post('/customer', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("customer added successfully" in response.data.decode())

    def test_update_customer(self):
        data = {
            'customer_name': 'John Doe Updated',
            'gender': 'Male',
            'email_address': 'john_updated@example.com',
            'phone_number': '+123456789',
            'country': 'USA',
            'province': 'California',
            'municipality': 'Los Angeles',
            'address': '123 Main St'
        }
        response = self.app.post('/customer/31', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Customer updated successfully" in response.json['message'])

    def test_delete_customer(self):
        response = self.app.post('/customer/delete', data={'customer_id': 31})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("deleted successfully" in response.json['message'])

if __name__ == '__main__':
    unittest.main()
        
if __name__ == "__main__":
    unittest.main()
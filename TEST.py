import unittest
import warnings
from CRUD_REST_API import app

class appTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        warnings.simplefilter("ignore", category=DeprecationWarning)
        
    def test_main_page(self):
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
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), html)
        
    def test_getcustomers(self):
        response = self.app.get("/customer")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Maria D. Beru" in response.data.decode())
        
if __name__ == "__main__":
    unittest.main()
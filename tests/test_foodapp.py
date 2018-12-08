import unittest
from flask  import json
from app.foodapp import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user = {
            "username": "jenny",
            "email": "jenny@gmail",
            "password": "password"
        }

    def test_register_successfully(self):
        response = self.client.post('/api/v1/register',data=json.dumps(self.user), content_type='application/json')
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual("User registered successfully", data["message"])
        self.assertEqual(201, response.status_code)
    

if __name__ == "__main__":
    unittest.main()
                







    
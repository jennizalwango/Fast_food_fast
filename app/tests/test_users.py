from flask  import json
from app.tests.base import BaseTestCase


class APITestCase(BaseTestCase):

    def test_register_successfully(self):
        with self.client:
            self.user = {
                "username": "jenny",
                "email": "jenny@gmail",
                "password": "password"
            }

            response = self.client.post('/api/v1/register',data=json.dumps(self.user), content_type='application/json')
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual("User registered successfully", data["message"])
            self.assertEqual(201, response.status_code)
     
import unittest
import requests
from requests.auth import HTTPBasicAuth

class TestSetProperties(unittest.TestCase):

    def test_put(self):
        response2 = requests.get('http://127.0.0.1:5000/auth/', auth=HTTPBasicAuth('write', '1'))
        tiket = response2.headers['Authorization']
        response3 = requests.put('http://127.0.0.1:5000/2/', data = '{"message":"lol"}', headers = {'Authorization': tiket})
        if response3.text != "changed":
            self.assertEqual(response3.text,"{\"2\":\"lol\"}\n")
        else:
            self.assertEqual(response3.text, "changed")

    def test_get(self):
        response2 = requests.get('http://127.0.0.1:5000/auth/', auth=HTTPBasicAuth('write', '1'))
        tiket_put = response2.headers['Authorization']
        requests.put('http://127.0.0.1:5000/3/', data='{"message":"kek"}', headers={'Authorization': tiket_put})
        response4 = requests.get('http://127.0.0.1:5000/auth/', auth=HTTPBasicAuth('read', '2'))
        tiket_get = response4.headers['Authorization']
        response5 = requests.get('http://127.0.0.1:5000/3/', headers={'Authorization': tiket_get})
        self.assertEqual(response5.text, "{\"message\":\"kek\"}\n")

    def test_delete(self):
        response1 = requests.get('http://127.0.0.1:5000/auth/', auth=HTTPBasicAuth('write', '1'))
        tiket_put = response1.headers['Authorization']
        response2 = requests.get('http://127.0.0.1:5000/auth/', auth=HTTPBasicAuth('delete', '3'))
        tiket_delete = response2.headers['Authorization']
        requests.put('http://127.0.0.1:5000/4/', data='{"message":"for deleting"}', headers={'Authorization': tiket_put})
        response3 = requests.delete('http://127.0.0.1:5000/4/', headers={'Authorization': tiket_delete})
        self.assertEqual(response3.status_code, 204)


if __name__ == '__main__':
    unittest.main()
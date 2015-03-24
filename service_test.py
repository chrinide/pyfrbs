#!/usr/bin/env python

import sys
import unittest
import json
import urllib3

class tests(unittest.TestCase):
    def test_get_variables(self):
        conn = urllib3.connection_from_url('http://127.0.0.1:5000/')
        r = conn.request('GET', '/api/variables')
        self.assertEqual(r.status, 200)
        data = json.loads(r.data.decode('utf-8'))
        self.assertIn('variables', data)

if __name__ == '__main__':
    unittest.main()

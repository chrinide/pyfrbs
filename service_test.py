#!/usr/bin/env python

from service import app

import sys
import argparse
import unittest
import json

class tests(unittest.TestCase):

    def setUp(self):
        app.config['host'] = opts.address.split(':')[0]
        app.config['port'] = opts.address.split(':')[1]
        app.config['database'] = opts.database
        app.config['username'] = opts.username
        app.config['password'] = opts.password
        self.app = app.test_client()

    def test_get_variables(self):
        r = self.app.get('/api/variables')
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data.decode('utf-8'))
        self.assertIn('variables', data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-a', dest='address', default='127.0.0.1:5432')
    parser.add_argument('-d', dest='database', default='fuzzy')
    parser.add_argument('-u', dest='username', default='user1')
    parser.add_argument('-p', dest='password', default='pass1')
    opts = parser.parse_args()
    runner = unittest.TextTestRunner()
    itersuite = unittest.TestLoader().loadTestsFromTestCase(tests)
    runner.run(itersuite)

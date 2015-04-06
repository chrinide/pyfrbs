#!/usr/bin/env python

from service import app

import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-a', dest='address', default='127.0.0.1:5432')
    parser.add_argument('-b', dest='bind_to', default='127.0.0.1:5000')
    parser.add_argument('-d', dest='database', default='db')
    parser.add_argument('-u', dest='username', default='user')
    parser.add_argument('-p', dest='password', default='pass')
    opts = parser.parse_args()
    app.config['host'] = opts.address.split(':')[0]
    app.config['port'] = opts.address.split(':')[1]
    app.config['database'] = opts.database
    app.config['username'] = opts.username
    app.config['password'] = opts.password
    app.run(host=opts.bind_to.split(':')[0], port=int(opts.bind_to.split(':')[1]), debug=True)

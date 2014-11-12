#!/usr/bin/python

import psycopg2

conn = psycopg2.connect(host="10.0.0.1", database="fuzzy", user="user1", password="pass1")
cur = conn.cursor()

cur.execute("SELECT * FROM variable;")
print(cur.fetchone())

conn.commit()
cur.close()
conn.close()

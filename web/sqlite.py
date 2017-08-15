__author__ = 'wangweijun'
# -*- coding: UTF-8 -*-
import sqlite3

sqliteconn = sqlite3.connect('d:/mysqlite.db3')
cur = sqliteconn.cursor()
#cur.execute('CREATE TABLE entries (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,'
 #        'content TEXT,posted_on DATETIME)')
cur.execute("select * from entries")
#cur.execute(" delete from entries where id= 5")
print cur.fetchall()
sqliteconn.commit()
cur.close()
sqliteconn.close()


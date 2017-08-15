#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import web
import datetime
import sqlite3
# 数据库连接
db = web.database(dbn = 'sqlite', db = 'd:/mysqlite.db3')
#获取所有文章
def get_posts():
    return db.select('entries', order = 'id DESC')
    
#获取文章内容
def get_post(id):
    try:
        return db.select('entries', where = 'id=$id', vars = locals())[0]
    except IndexError:
        return None
#新建文章
def new_post(title,text):
    db.insert('entries', title = title, content = text, posted_on = datetime.datetime.now())

#删除文章
def del_post(id):
    db.delete('entries', where = 'id = $id', vars = locals())
    
#修改文章
def update_post(id, title, text):
    db.update('entries',
        where = 'id = $id',
        vars = locals(),
        title = title,
        content = text,
		posted_on = datetime.datetime.now())

def transform_datestr(posted_time):
     datetime_obj = datetime.datetime.strptime(posted_time,'%Y-%m-%d %H:%M:%S.%f')
     return web.datestr(datetime_obj)


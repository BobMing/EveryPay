#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import sae.const
import MySQLdb
import web.db

def connectDB():
    db = web.database(
        dbn = 'mysql',
        host = sae.const.MYSQL_HOST,
        port = int(sae.const.MYSQL_PORT),
        user = sae.const.MYSQL_USER,
        passwd = sae.const.MYSQL_PASS,
        db = sae.const.MYSQL_DB
    )
    return db

# userid - str : requestid
# demand - str : demand
# quote - str : payment
# destination - str : destination
def release(userid, demand, quote, destination):
    db = connectDB()

    orderid = db.insert('orders', dmd = demand, quote = quote, requestid = userid, destination = destination)
    db.insert('dmdpool', orderid = orderid)

# username - str : username
# password - str : password
def login(username, password):
    db = connectDB()

    mmd5 = hashlib.md5()
    mmd5.update(password)
    pwd = mmd5.hexdigest()

    query = db.query("SELECT userid, username FROM user WHERE username = $usr AND password = $pwd", vars={'usr': username, 'pwd' : pwd})
    if len(query) == 1:
        for item in query:
            return [True, item.userid, item.username]
    else:
        return [False]

# username - str : username
# password - str : password
# telephone - int : tel number
# wechat - str : wechat number
# icon - int : icon number
def register(username, password, telephone, wechat, icon):
    db = connectDB()

    mmd5 = hashlib.md5()
    mmd5.update(password)
    pwd = mmd5.hexdigest()

    if not wechat:
        db.insert('user', username = username, password = pwd, telephone = telephone, icon = icon)
    else:
        db.insert('user', username = username, password = pwd, telephone = telephone, wechat = wechat, icon = icon)

# userid - str : serveid
# password - str : password
def recieveOrder(userid, orderid):
    db = connectDB()

    db.update('orders', where='orderid=$id', vars={'id': int(orderid)}, serveid = userid, status=0)
    db.delete('dmdpool', where='orderid=$id', vars={'id': int(orderid)})

def evaluate(status, orderid):
    db = connectDB()

    db.update('orders', where='orderid=$id', vars={'id': int(orderid)}, status=int(status))

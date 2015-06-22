#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import sae.const
import MySQLdb
import web.db

# userid - str : requestid
# password - str : password
def release(userid, demand, quote, destination):
    db = web.database(
        dbn = 'mysql',
        host = sae.const.MYSQL_HOST,
        port = int(sae.const.MYSQL_PORT),
        user = sae.const.MYSQL_USER,
        passwd = sae.const.MYSQL_PASS,
        db = sae.const.MYSQL_DB
    )

    orderid = db.insert('orders', dmd = demand, quote = quote, requestid = userid, destination = destination)
    db.insert('dmdpool', orderid = orderid)

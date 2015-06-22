#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import sae.const
import MySQLdb
import web.db

# username - str : username
# password - str : password
# telephone - int : tel number
# wechat - str : wechat number
# icon - int : icon number
def register(username, password, telephone, wechat, icon):
    db = web.database(
        dbn = 'mysql',
        host = sae.const.MYSQL_HOST,
        port = int(sae.const.MYSQL_PORT),
        user = sae.const.MYSQL_USER,
        passwd = sae.const.MYSQL_PASS,
        db = sae.const.MYSQL_DB
    )

    mmd5 = hashlib.md5()
    mmd5.update(password)
    pwd = mmd5.hexdigest()

    if not wechat:
        db.insert('user', username = username, password = pwd, telephone = telephone, icon = icon)
    else:
        db.insert('user', username = username, password = pwd, telephone = telephone, wechat = wechat, icon = icon)



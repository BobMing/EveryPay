#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import sae.const
import MySQLdb
import web.db

# username - str : username
# password - str : password
def login(username, password):
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

    query = db.query("SELECT userid, username FROM user WHERE username = $usr AND password = $pwd", vars={'usr': username, 'pwd' : pwd})
    if len(query) == 1:
        for item in query:
            return [True, item.userid, item.username]
    else:
        return [False]


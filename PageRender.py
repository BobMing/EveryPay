#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.wsgi
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

def renderDmdPool(obj, userid, username):
    db = connectDB()
    demands = []
    query = db.query("SELECT orders.requestid, orders.orderid, orders.dmd, orders.quote, orders.destination, orders.time FROM orders, dmdpool WHERE orders.orderid = dmdpool.orderid ORDER BY dmdpool.dmdid DESC")
    if len(query) > 0:
        for item in query:
            query2 = db.query("SELECT username, telephone FROM user WHERE userid = $rid AND userid <> $uid", vars = {'rid': item.requestid, 'uid': userid})
            for item2 in query2:
                demand = [item.dmd, item.destination, item2.username, item2.telephone, item.quote, item.time, item.orderid]
                demands.append(demand)

    obj.render('demandpool.html', userid = userid, username = username, demands = demands)

def renderRequest(obj, userid, username):
    db = connectDB()
    requests = []
    query = db.query("SELECT * FROM orders WHERE requestid = $uid  ORDER BY orderid DESC", vars={'uid': int(userid)})
    if len(query) > 0:
        for item in query:
            if item.serveid:
                query2 = db.query("SELECT username, telephone FROM user WHERE userid = $sid", vars = {'sid': int(item.serveid)})
                for item2 in query2:
                    request = [item.dmd, item.destination, item2.username, item2.telephone, item.quote, item.time, str(item.status), item.orderid]
                    requests.append(request)
            else:
                request = [item.dmd, item.destination, '', '', item.quote, item.time, str(item.status), item.orderid]
                requests.append(request)

    obj.render('request.html', userid = userid, username = username, requests = requests)

def renderService(obj, userid, username):
    db = connectDB()
    services = []
    query = db.query("SELECT * FROM orders WHERE serveid = $uid ORDER BY orderid DESC", vars={'uid': int(userid)})
    if len(query) > 0:
        for item in query:
            query2 = db.query("SELECT username, telephone FROM user WHERE userid = $uid", vars = {'uid': int(item.requestid)})
            for item2 in query2:
                service = [item.dmd, item.destination, item2.username, item2.telephone, item.quote, item.time, str(item.status), item.orderid]
                services.append(service)

    obj.render('service.html', userid = userid, username = username, services = services)


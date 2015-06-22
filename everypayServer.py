#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.wsgi
import sae.const
import MySQLdb
import web.db
import PageRender
import ServerOperation

class MainHandler(tornado.web.RequestHandler):

    # 处理网页访问
    def get(self):
        self.set_status(200)
        self.set_header("Accept-Charset","utf-8")
        self.webview_dispatch()

    # 处理post参数请求
    def post(self):
        self.set_status(200)
        self.set_header("Accept-Charset","utf-8")
        self.operation_dispatch()

    # post参数处理
    def operation_dispatch(self):
        op = self.get_argument('action')
        operation.get(op)(self)

    # 返回网页
    def webview_dispatch(self):
        op = self.get_argument('page')
        if not op.endswith('.html'):
            if op.rfind('.') > 0:
                op = op[:op.rfind('.')] + ".html"
            else:
                op = op + ".html"

        if op == 'demandpool.html':
            userid = self.get_argument('userid')
            username = self.get_argument('username')
            PageRender.renderDmdPool(self, userid, username)
        elif op == 'release.html':
            userid = self.get_argument('userid')
            username = self.get_argument('username')
            self.render(op, userid=userid, username=username)
        elif op == 'request.html':
            userid = self.get_argument('userid')
            username = self.get_argument('username')
            PageRender.renderRequest(self, userid, username)
        elif op == 'service.html':
            userid = self.get_argument('userid')
            username = self.get_argument('username')
            PageRender.renderService(self, userid, username)
        else:
            self.render(op)


    # 注册
    @staticmethod
    def _reg_(obj):
        username = obj.get_argument('username')
        password = obj.get_argument('password')
        telephone = int(obj.get_argument('telephone'))
        wechat = obj.get_argument('wechat', None)
        icon = int(obj.get_argument('icon', 0))

        # do registration
        ServerOperation.register(username, password, telephone, wechat, icon)
        dic = {'action': 'reg', 'status': 'success', 'reason':''}
        obj.write(str(dic) + "\n")
        obj.render('regsuc.html')

    # 登录
    @staticmethod
    def _log_(obj):
        username = obj.get_argument('username')
        password = obj.get_argument('password')

        # do login
        result = ServerOperation.login(username, password)
        if not result[0]:
            dic = {'action': 'log', 'status': 'failure', 'reason':'User Name or Password Error'}
            obj.write(str(dic) + '\n')
        else:
            dic = {'action': 'log', 'status': 'success', 'reason':'', "userid":str(result[1]), "username":result[2]}
            obj.write(str(dic) + '\n')

    #判断是否用户名重复
    @staticmethod
    def _usr_(obj):
        db = web.database(
            dbn = 'mysql',
            host = sae.const.MYSQL_HOST,
            port = int(sae.const.MYSQL_PORT),
            user = sae.const.MYSQL_USER,
            passwd = sae.const.MYSQL_PASS,
            db = sae.const.MYSQL_DB
        )

        username = obj.get_argument('username')
        query = db.query("SELECT * FROM user WHERE username = $usr", vars={'usr': username})
        if len(query) > 0:
            dic = {'action':'usr', 'status':'failure', 'reason':'User Name Exist'}
            obj.write(str(dic) + '\n')
        else:
            dic = {'action':'usr', 'status':'success', 'reason':''}
            obj.write(str(dic) + '\n')

    @staticmethod
    def _rel_(obj):
        userid = obj.get_argument('userid')
        demand = obj.get_argument('demand')
        quote = obj.get_argument('quote')
        destination = obj.get_argument('destination')

        ServerOperation.release(userid, demand, quote, destination)
        dic = {'action': 'rel', 'status': 'success', 'reason':''}
        obj.write(str(dic) + "\n")

    @staticmethod
    def _rco_(obj):
        userid = obj.get_argument('userid')
        orderid = obj.get_argument('orderid')

        ServerOperation.recieveOrder(userid, orderid)
        dic = {'action': 'rco', 'status': 'success', 'reason':''}
        obj.write(str(dic) + "\n")

    @staticmethod
    def _star_(obj):
        orderid = obj.get_argument('orderid')
        status = obj.get_argument('status')

        ServerOperation.evaluate(status, orderid)
        dic = {'action': 'star', 'status': 'success', 'reason':''}
        obj.write(str(dic) + "\n")

operation = {'reg': MainHandler._reg_ , 'log': MainHandler._log_, 'usr': MainHandler._usr_,\
                    'rel': MainHandler._rel_, 'rco': MainHandler._rco_, 'star': MainHandler._star_}

# -*- coding:utf-8 -*-

import time, json
import tornadoredis
import tornado.web
from tornado import escape,gen,websocket
from client import AsyncClient
from cache import cacheClient
from restApi import post
from config.appConfig import redisServer, logServer
import datetime, time


class BaseHandler(tornado.web.RequestHandler):
    url_pattern = None

    def __init__(self, application, request, **kwargs):
        self.client = AsyncClient()  # AsyncClient
        self.cache = cacheClient
        self.write_buffer = ""
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie("userId")

    def prepare(self): # comment me for debug
        allowURL = ["Login","login","h5page"]
        for url in allowURL:
            if url in self.request.path:
                return
        if not self.current_user:  # all api require login
            self.redirect("/login")
        else:
            return

    def sendLog(self, message=""):
        post(logServer,{
            "userId":self.get_secure_cookie("userId",u"-未登录-"),
            "userRealname":self.get_secure_cookie("userName",u"-未登录-"),
            "operateDate":int(time.time()*1000),
            "operateModule":self.request.path,
            "operate":"dummy",
            "description":json.dumps({
                "header":self.request.headers,
                "body":self.request.body,
                "message":message
            }),
        })

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', '*')
        #self.set_header('Content-type', 'application/json') #此行导致中文乱码

    def write(self, chunk):
        if isinstance(chunk, list):
            chunk = {
                "autoWrap":chunk,
                "info":"this api is returning a list, FCore wrapped it cause most browser has bug with this action, mimiron2.Ajax will auto unwrap this object."
            }
        return super(BaseHandler, self).write(chunk)

    # below is self use methods
    def getParams(self, theKey=None):
        body = json.loads(self.request.body)
        if theKey:
            return body.get(theKey)
        else:
            return body

    def getParmas(self, theKey=None): # REMOVE ME
        print("!!! sorry, this method name is misspelled, please change all self.getParmas to self.getParams in your coding, thx~")
        return self.getParams(theKey)



class WsHandler(tornado.websocket.WebSocketHandler):
    url_pattern = None
    clients = set()

    def __init__(self, application, request, **kwargs):
        super(WsHandler, self).__init__(application, request, **kwargs)

    def clean(self, *args, **kwargs):
        raise Exception('no implement exception', 'clean method need implement')

    def on_close(self):
        try:
            WsHandler.clients.remove(self)
            self.clean()
        except KeyError:
            pass
        except AttributeError:
            pass
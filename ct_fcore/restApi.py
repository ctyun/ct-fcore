# coding:utf-8
from handler import AsyncClient as AsyncClientForUCcore
from config import appConfig
import json, copy, logging
from tornado.gen import Task
from tornado import gen
from cache import cacheClient
from tornado.httpclient import AsyncHTTPClient,HTTPRequest

client_ucore = AsyncClientForUCcore()
client_normal = AsyncHTTPClient()
log = logging.getLogger("ct-fcore.rest_api")

@gen.coroutine
def post(url,body={},headers={},cache=None, contentType=None, mode="ucore"):
    kwstr = None
    if cacheClient and cache:
        kwcp = {}
        kwcp["url"] = url
        kwcp["headers"] = headers
        kwcp["body"] = body
        kwcp["method"] = "post"
        kwstr = json.dumps(kwcp)
        result = yield Task(cacheClient.get, kwstr)
        if result:
            try:
                resp = eval(result)
            except Exception,e:
                print (e)
                resp = {"error":str(e),"body":result}
            raise gen.Return(resp)
    if "http" not in url:
        url = appConfig.restApiServer+url
    try:
        if contentType:
            headers["Content-Type"] = contentType
        if mode == "ucore":
            if not contentType:
                headers["Content-Type"] = "application/x-www-form-urlencoded" #important!
            resp = yield client_ucore.fetch(url, headers, body, "POST",cache=cache)
        elif mode == "json":
            headers["Content-Type"] = "application/json"
            resp = yield client_normal.fetch(HTTPRequest(url=url,method="POST",headers=headers,body=json.dumps(body)))
            log.info(json.dumps({"response":resp.body,"body":json.dumps(body),"headers":headers,"url":url,"method":"POST"}))
            try:
                resp = json.loads(resp.body)
            except UnicodeDecodeError:
                resp = json.loads(resp.body, encoding="gb2312")
        elif mode == "normal":
            resp = yield client_normal.fetch(HTTPRequest(url=url,method="POST",headers=headers,body=body))
            log.info(json.dumps({"response":resp,"body":body,"headers":headers,"url":url,"method":"POST"}))
        else:
            raise Exception(u"你传入了一个稀奇古怪的mode:{}".format(mode))
    except Exception,e:
        resp={"error":str(e),"error_type":"fetch_error","url":url,"headers":headers,"body":body}
        log.error(json.dumps(resp))
    if cacheClient and cache:
        yield Task(cacheClient.set, kwstr, resp)
    raise gen.Return(resp)


@gen.coroutine
def get(url,headers={},body={},cache=None, mode="ucore"):
    kwstr = None
    if cacheClient and cache:
        kwcp = {}
        kwcp["url"] = url
        kwcp["headers"] = headers
        kwcp["body"] = body
        kwcp["method"] = "get"
        kwstr = json.dumps(kwcp)
        result = yield Task(cacheClient.get, kwstr)
        if result:
            try:
                resp = eval(result)
            except Exception,e:
                print (e)
                resp = {"error":str(e),"body":result}
            raise gen.Return(resp)
    if "http" not in url:
        url = appConfig.restApiServer+url
    try:
        if mode == "ucore":
            resp = yield client_ucore.fetch(url, headers, body, "GET",cache=cache)
        elif mode == "json":
            resp = yield client_normal.fetch(HTTPRequest(url=url,method="GET",headers=headers,body=json.dumps(body)))
            resp = json.loads(resp.body)
            log.info(json.dumps({"response":resp,"body":body,"headers":headers,"url":url,"method":"GET"}))
        elif mode == "normal":
            resp = yield client_normal.fetch(HTTPRequest(url=url,method="GET",headers=headers,body=body))
            log.info(json.dumps({"response":resp,"body":body,"headers":headers,"url":url,"method":"GET"}))
        else:
            raise Exception(u"你传入了一个稀奇古怪的mode:{}".format(mode))
    except Exception,e:
        resp={"error":str(e),"error_type":"fetch_error","url":url,"headers":headers,"body":body}
        log.error(json.dumps(resp))
    if cacheClient and cache:
        yield Task(cacheClient.set, kwstr, resp)
    raise gen.Return(resp)




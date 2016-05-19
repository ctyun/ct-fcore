# coding:utf-8
from handler import AsyncClient
from config import appConfig
import json, copy
from tornado.gen import Task
from tornado import gen
from cache import cacheClient

client = AsyncClient()

@gen.coroutine
def post(url,body={},headers={},cache=None, contentType="application/x-www-form-urlencoded"):
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
        headers["Content-Type"] = contentType #important!
        resp = yield client.fetch(url, headers, body, "POST",cache=cache)
    except Exception,e:
        resp={"error":str(e),"error_type":"fetch_error","url":url,"headers":headers,"body":body}
    if cacheClient and cache:
        yield Task(cacheClient.set, kwstr, resp)
    raise gen.Return(resp)


@gen.coroutine
def get(url,headers={},body={},cache=None):
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
        resp = yield client.fetch(url, headers, body, "GET",cache=cache)
    except Exception,e:
        resp={"error":str(e),"error_type":"fetch_error","url":url,"headers":headers,"body":body}
    if cacheClient and cache:
        yield Task(cacheClient.set, kwstr, resp)
    raise gen.Return(resp)


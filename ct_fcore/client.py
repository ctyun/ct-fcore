# -*- coding:utf-8 -*-
from tornado.concurrent import TracebackFuture
from tornado.escape import utf8, native_str
from tornado import httputil, stack_context
from tornado.ioloop import IOLoop
from tornado.util import Configurable
from tornado.gen import Task
from tornado import gen

from tornado.httpclient import AsyncHTTPClient,HTTPRequest,_RequestProxy,HTTPResponse,HTTPError
from tornado.simple_httpclient import SimpleAsyncHTTPClient

import time, json, copy, urllib

from cache import cacheClient


class AsyncClient(SimpleAsyncHTTPClient, AsyncHTTPClient):

    def fetch(self, url, headers=None, body=None, method="GET", callback=None, raise_error=True, cache=None, bodyFormat=None, **kwargs):
        headers = headers or {}
        body = body or "{}"
        """very simlar with AsyncHTTPClient.fetch
        """
        if self._closed:
            raise RuntimeError("fetch() called on closed AsyncHTTPClient")
        future = TracebackFuture()
        if bodyFormat == "json":
            body = json.dumps(body)
        elif bodyFormat == "dxts":
            if isinstance(body, dict):
                for k,v in body.items():
                    if v is None:
                        del body[k]
                body = urllib.urlencode(body)
        for k,v in headers.items(): #headers 只能接收str
            if v:
                headers[k] = str(headers[k])
            else:
                del headers[k]
        request = HTTPRequest(url=url,method=method,headers=headers,body=body, allow_nonstandard_methods=True, request_timeout=600 ,**kwargs)
        # We may modify this (to add Host, Accept-Encoding, etc),
        # so make sure we don't modify the caller's object.  This is also
        # where normal dicts get converted to HTTPHeaders objects.
        request.headers = httputil.HTTPHeaders(request.headers)
        request = _RequestProxy(request, self.defaults)
        if callback is not None:
            callback = stack_context.wrap(callback)

            def handle_future(future):
                exc = future.exception()
                if isinstance(exc, HTTPError) and exc.response is not None:
                    response = exc.response
                elif exc is not None:
                    response = HTTPResponse(
                        request, 599, error=exc,
                        request_time=time.time() - request.start_time)
                else:
                    response = future.result()
                self.io_loop.add_callback(callback, response)
            future.add_done_callback(handle_future)

        def handle_response(response):
            if raise_error and response.error:
                future.set_exception(response.error)
            else:
                try:
                    resp = json.loads(str(response.body))
                    if resp.get("statusCode") and resp.get("statusCode")==800:
                        future.set_result(resp)
                    else:
                        future.set_result({"error_type":"statusCode is not 800", "response":resp,"body":body,"headers":headers,"url":url})
                except Exception,e:
                    print (e)
                    future.set_result({"error_type":"json.loads failed!","error":str(e),"response.body":response.body,"body":body,"headers":headers,"url":url})

        self.fetch_impl(request, handle_response)
        return future
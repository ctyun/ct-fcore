# coding:utf-8
"""
基础模块, 扩展了 Tornado Web 服务器
"""
import tornado.web
from FCore.handler import BaseHandler, WsHandler
import os, sys
from importlib import import_module


class Application(tornado.web.Application):
    def __init__(self):
        handlers = None
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "../templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../static"),
            cookie_secret="itdoesnotreallymatter",
            xsrf_cookies=False,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
    """
    Tornado 应用实例
    """
    def load_handler_module(self, handler_module, perfix = ".*$"):
        """
        从模块加载 BaseHandler
            `handler_module` : 模块
            `perfix` : url 前缀
        """
        # 判断是否是有效的 BaseHandler (是类且是 BaseHandler 的子类)
        is_handler = lambda cls: isinstance(cls, type) \
                     and (issubclass(cls, BaseHandler) or issubclass(cls, WsHandler))
        # 判断是否拥有 url 规则
        has_pattern = lambda cls: hasattr(cls, 'url_pattern') \
                      and cls.url_pattern
        handlers = []
        # 迭代模块成员
        for i in dir(handler_module):
            cls = getattr(handler_module, i)
            if is_handler(cls) and has_pattern(cls):
                handlers.append((cls.url_pattern, cls))
        self.add_handlers(perfix, handlers)

    def _get_host_handlers(self, request):
        """
        覆盖父类方法, 一次获取所有可匹配的结果. 父类中该方法一次匹配成功就返回, 忽略后续
        匹配结果. 现通过使用生成器, 如果一次匹配的结果不能使用可以继续匹配.
        """
        host = request.host.lower().split(':')[0]
        # 使用生成器表达式而非列表推导式, 减少性能折扣
        handlers = (i for p, h in self.handlers for i in h if p.match(host))
        # Look for default host if not behind load balancer (for debugging)
        if not handlers and "X-Real-Ip" not in request.headers:
            handlers = [i for p, h in self.handlers for i in h if p.match(self.default_host)]
        return handlers

    def autoLoadModule(self, root):
        def deal(path):
            for rt, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        moduleName = rt.replace(sys.path[0],"").split(os.sep)[1:]
                        if moduleName[0]:
                            try:
                                moduleRealname = ".".join(moduleName)+"."+file.replace(".py","")
                                moduleIns = import_module(".".join(moduleName)+"."+file.replace(".py",""))
                                self.load_handler_module(moduleIns)
                            except ImportError,e:
                                print(str(e)+" @ "+file)
                                pass

        deal(root)
        return


def route(url_pattern):
    """
    路由装饰器, 只能装饰 BaseHandler和WsHandler 子类
    """
    def handler_wapper(cls):
        assert(issubclass(cls, BaseHandler) or issubclass(cls, WsHandler))
        cls.url_pattern = url_pattern
        return cls
    return handler_wapper
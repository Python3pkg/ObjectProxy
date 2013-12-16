# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

__all__ = ['Context']


@apply
def Context():

    _contexts = {}


    class ContextMeta(type):

        @property
        def contexts(cls):
            return set(_contexts.iteritems())


        @property
        def current(cls):
            return cls.__current

        @current.setter
        def current(cls, context):
            context = context or 'default'

            if isinstance(context, Context):
                cls.__current = context
                return

            try:
                cls.__current = _contexts[context]
            except KeyError:
                raise ValueError('context {} not found'.format(context))


        def find_proxy(cls, proxy):
            proxy_id = id(proxy)
            return [
                (name, context[proxy_id])
                for name, context in _contexts.iteritems()
                if proxy_id in context
            ]


        def __call__(cls, name_or_context):
            if isinstance(name_or_context, Context):
                return name_or_context

            self = _contexts.get(name_or_context)
            if not self:
                self = super(ContextMeta, cls).__call__(name_or_context)
                _contexts[name_or_context] = self

            return self


    class Context(object):

        __metaclass__ = ContextMeta


        def __init__(self, name):
            self.name = name
            self.reset()

            def activate():
                type(self).activate(self)
            self.activate = activate


        def __getitem__(self, key):
            try:
                return self.__proxies[key]
            except KeyError:
                raise NameError('context {} has no proxy {}'.format(self.name, key))


        def __setitem__(self, key, targetname):
            self.__proxies[key] = targetname


        def __contains__(self, proxy_id):
            return proxy_id in self.__proxies


        def reset(self):
            self.__proxies = {}


        def register(self, proxy, targetname):
            self[id(proxy)] = targetname


        @classmethod
        def activate(cls, context):
            cls.current = context


    Context.current = Context('default')
    return Context

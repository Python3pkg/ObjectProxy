# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from importlib import import_module
from weakref import ref as weakref
from ._lambda_relations import method_map
from .context import Context

__all__ = ['LazyProxy']


@apply
def LazyProxy():

    method_dict = dict(method_map)


    class ProxyBase(object):

        def __init__(self, targetname, context=None):
            ProxyBase.__setattr__(self, '__context', None)
            ProxyBase.__setattr__(self, '__is_weakref', False)
            context = Context(context or Context.current)
            context.register(self, targetname)


        def __import_target(self):
            context = Context.current
            ProxyBase.__setattr__(self, '__context', context)
            name = context[id(self)]
            if ':' in name:
                name, objname = name.split(':', 1)
            else:
                objname = None

            module = import_module(name)
            target = getattr(module, objname) if objname else module

            try:
                target = weakref(target)
            except TypeError:
                ProxyBase.__setattr__(self, '__is_weakref', False)
            else:
                ProxyBase.__setattr__(self, '__is_weakref', True)

            ProxyBase.__setattr__(self, '__target', target)


        @property
        def _target(self):
            context = ProxyBase.__getattribute__(self, '__context')
            if context != Context.current:
                ProxyBase.__import_target(self)
            target = ProxyBase.__getattribute__(self, '__target')
            if ProxyBase.__getattribute__(self, '__is_weakref'):
                target = target()
            return target


    class ProxyMeta(type):

        props = (
            '__all__', '__doc__', '__file__', '__name__', '__package__',
        )

        meths = (
            '__delete__', '__delitem__', '__delslice__', '__div__',
            '__enter__', '__exit__', '__get__', '__index__', '__nonzero__',
            '__set__', '__setattr__', '__setitem__', '__setslice__',
            '__sizeof__', '__subclasshook__',
        )


        def __new__(metaclass, name, bases, dct):
            for prop in metaclass.props:
                dct[prop] = metaclass.build_property(prop)

            for meth in metaclass.meths:
                dct[meth] = metaclass.build_proxy_method(meth)

            for meth in method_dict.iterkeys():
                dct[meth] = metaclass.build_special_method(meth)

            return type(name, bases, dct)


        @staticmethod
        def build_property(prop):
            return property(
                lambda self: getattr(super(LazyProxy, self)._target, prop)
            )


        @staticmethod
        def build_proxy_method(meth):
            return (
                lambda self, *args:
                    getattr(super(LazyProxy, self)._target, meth)(*args)
            )


        @staticmethod
        def build_special_method(meth):
            return (
                lambda self, *args:
                    method_dict[meth](super(LazyProxy, self)._target, *args)
            )


    class LazyProxy(ProxyBase):

        __metaclass__ = ProxyMeta
        __dict__ = property(lambda self: vars(super(LazyProxy, self)._target))

        def __repr__(self):
            context = Context.current
            try:
                target = context[id(self)]
                return "<LazyProxy to '{}'>".format(target)

            except NameError:
                return '<LazyProxy from another context>'


    return LazyProxy

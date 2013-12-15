# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from importlib import import_module
from weakref import ref as weakref
from ._lambda_relations import method_map

__all__ = ['Proxy']


class ProxyBase(object):

    def __init__(self, targetname):
        ProxyBase.__setattr__(self, '__targetname', targetname)
        ProxyBase.__setattr__(self, '__is_weakref', False)
        ProxyBase.__setattr__(self, '__set', False)


    def __import_target(self):
        name = ProxyBase.__getattribute__(self, '__targetname')
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
        ProxyBase.__setattr__(self, '__set', True)


    @property
    def _target(self):
        if not ProxyBase.__getattribute__(self, '__set'):
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
    ) + tuple(method_map.iterkeys())


    def __new__(metaclass, name, bases, dct):
        for prop in metaclass.props:
            dct[prop] = metaclass.build_property(prop)

        for meth in metaclass.meths:
            dct[meth] = metaclass.build_method(meth)

        return type(name, bases, dct)


    @staticmethod
    def build_property(prop):
        return property(
            lambda self: getattr(super(Proxy, self)._target, prop)
        )


    @staticmethod
    def build_method(meth):
        if meth in method_map:
            return (
                lambda self, *args:
                    method_map[meth](super(Proxy, self)._target, *args)
            )

        else:
            return (
                lambda self, *args:
                    getattr(super(Proxy, self)._target, meth)(*args)
            )



class Proxy(ProxyBase):

    __metaclass__ = ProxyMeta
    __dict__ = property(lambda self: vars(super(Proxy, self)._target))

# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from contextlib import wraps
from importlib import import_module
from weakref import ref as weakref

__all__ = ['Proxy']


def catch(wrapped, default=None):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        try:
            return wrapped(*args, **kwargs)
        except:
            return default
    return wrapper


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
    )


    def __new__(metaclass, name, bases, dct):
        for prop in metaclass.props:
            dct[prop] = metaclass.build_property(prop)

        for meth in metaclass.meths:
            dct[meth] = metaclass.build_method(meth)

        return type(name, bases, dct)


    @classmethod
    def build_property(metaclass, prop):
        return property(
            lambda self: getattr(super(Proxy, self)._target, prop)
        )


    @classmethod
    def build_method(metaclass, meth):
        return (
            lambda self, *args:
                getattr(super(Proxy, self)._target, meth)(*args)
        )



class Proxy(ProxyBase):

    __metaclass__ = ProxyMeta

    __dict__ = property(lambda self: vars(super(Proxy, self)._target))

    __abs__ = lambda self: abs(super(Proxy, self)._target)
    __add__ = lambda self, o: super(Proxy, self)._target + o
    __and__ = lambda self, o: super(Proxy, self)._target & o
    __bool__ = catch(lambda self: bool(super(Proxy, self)._target), False)
    __call__ = lambda self, *args, **kwargs: super(Proxy, self)._target(*args, **kwargs)
    __cmp__ = lambda self, o: cmp(super(Proxy, self)._target, o)
    __coerce__ = lambda self, o: coerce(super(Proxy, self)._target, o)
    __contains__ = lambda self, item: item in super(Proxy, self)._target
    __delattr__ = lambda self, attr: delattr(super(Proxy, self)._target, attr)
    __dir__ = catch(lambda self: dir(super(Proxy, self)._target), [])
    __divmod__ = lambda self, o: divmod(super(Proxy, self)._target, o)
    __float__ = lambda self: float(super(Proxy, self)._target)
    __floordiv__ = lambda self, o: super(Proxy, self)._target // o
    __eq__ = lambda self, o: super(Proxy, self)._target == o
    __ge__ = lambda self, o: super(Proxy, self)._target >= o
    __getattr__ = lambda self, attr: getattr(super(Proxy, self)._target, attr)
    __getitem__ = lambda self, key: super(Proxy, self)._target[key]
    __getslice__ = lambda self, i, j: super(Proxy, self)._target[i:j]
    __gt__ = lambda self, o: super(Proxy, self)._target > o
    __hash__ = lambda self: hash(super(Proxy, self)._target)
    __hex__ = lambda self: hex(super(Proxy, self)._target)
    __instancecheck__ = lambda self, instance: isinstance(instance, super(Proxy, self)._target)
    __int__ = lambda self: int(super(Proxy, self)._target)
    __invert__ = lambda self: ~(super(Proxy, self)._target)
    __iter__ = lambda self: iter(super(Proxy, self)._target)
    __le__ = lambda self, o: super(Proxy, self)._target <= o
    __len__ = lambda self: len(super(Proxy, self)._target)
    __long__ = lambda self: long(super(Proxy, self)._target)
    __lshift__ = lambda self, o: super(Proxy, self)._target << o
    __lt__ = lambda self, o: super(Proxy, self)._target < o
    __mod__ = lambda self, o: super(Proxy, self)._target % o
    __mul__ = lambda self, o: super(Proxy, self)._target * o
    __ne__ = lambda self, o: super(Proxy, self)._target != o
    __neg__ = lambda self: -(super(Proxy, self)._target)
    __oct__ = lambda self: oct(super(Proxy, self)._target)
    __or__ = lambda self, o: super(Proxy, self)._target | o
    __pos__ = lambda self: +(super(Proxy, self)._target)
    __pow__ = lambda self, o: super(Proxy, self)._target ** o
    __radd__ = lambda self, o: o + super(Proxy, self)._target
    __rand__ = lambda self, o: o & super(Proxy, self)._target
    __rcmp__ = lambda self, o: cmp(o, super(Proxy, self)._target)
    __rdiv__ = lambda self, o: o.__div__(super(Proxy, self)._target)
    __repr__ = lambda self: '<Proxy to {}>'.format(repr(super(Proxy, self)._target))
    __reversed__ = lambda self: reversed(super(Proxy, self)._target)
    __rfloordiv__ = lambda self, o: o // super(Proxy, self)._target
    __rlshift__ = lambda self, o: o << super(Proxy, self)._target
    __rmod__ = lambda self, o: o % super(Proxy, self)._target
    __rmul__ = lambda self, o: o * super(Proxy, self)._target
    __ror__ = lambda self, o: o | super(Proxy, self)._target
    __rpow__ = lambda self, o: o ** super(Proxy, self)._target
    __rrshift__ = lambda self, o: o >> super(Proxy, self)._target
    __rshift__ = lambda self, o: super(Proxy, self)._target >> o
    __rsub__ = lambda self, o: o - super(Proxy, self)._target
    __rtruediv__ = lambda self, o: o / super(Proxy, self)._target
    __rxor__ = lambda self, o: o ^ super(Proxy, self)._target
    __str__ = lambda self: str(super(Proxy, self)._target)
    __sub__ = lambda self, o: super(Proxy, self)._target - o
    __truediv__ = lambda self, o: super(Proxy, self)._target / o
    __unicode__ = lambda self: unicode(super(Proxy, self)._target)
    __xor__ = lambda self, o: super(Proxy, self)._target ^ o

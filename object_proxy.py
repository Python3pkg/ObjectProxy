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
            pass
        ProxyBase.__setattr__(self, '__target', target)
        ProxyBase.__setattr__(self, '__set', True)


    @property
    def _target(self):
        if not ProxyBase.__getattribute__(self, '__set'):
            ProxyBase.__import_target(self)
        target = ProxyBase.__getattribute__(self, '__target')
        if isinstance(target, weakref):
            target = target()
        return target


class Proxy(ProxyBase):

    __all__ = property(lambda self: getattr(super(Proxy, self), '_target').__all__)
    __dict__ = property(lambda self: vars(getattr(super(Proxy, self), '_target')))
    __doc__ = property(lambda self: getattr(super(Proxy, self), '_target').__doc__)
    __file__ = property(lambda self: getattr(super(Proxy, self), '_target').__file__)
    __name__ = property(lambda self: getattr(super(Proxy, self), '_target').__name__)
    __package__ = property(lambda self: getattr(super(Proxy, self), '_target').__package__)

    __abs__ = lambda self: abs(getattr(super(Proxy, self), '_target'))
    __add__ = lambda self, o: getattr(super(Proxy, self), '_target') + o
    __and__ = lambda self, o: getattr(super(Proxy, self), '_target') & o
    __bool__ = catch(lambda self: bool(getattr(super(Proxy, self), '_target')), False)
    __call__ = lambda self, *args, **kwargs: getattr(super(Proxy, self), '_target')(*args, **kwargs)
    __cmp__ = lambda self, o: cmp(getattr(super(Proxy, self), '_target'), o)
    __coerce__ = lambda self, o: coerce(getattr(super(Proxy, self), '_target'), o)
    __contains__ = lambda self, item: item in getattr(super(Proxy, self), '_target')
    __delattr__ = lambda self, attr: delattr(getattr(super(Proxy, self), '_target'), attr)
    __delete__ = lambda self, instance: getattr(super(Proxy, self), '_target').__delete__(instance)
    __delitem__ = lambda self, key: getattr(super(Proxy, self), '_target').__delitem__(key)
    __delslice__ = lambda self, i, j: getattr(super(Proxy, self), '_target').__delslice__(i, j)
    __dir__ = catch(lambda self: dir(getattr(super(Proxy, self), '_target')), [])
    __div__ = lambda self, o: getattr(super(Proxy, self), '_target').__div__(o)
    __divmod__ = lambda self, o: divmod(getattr(super(Proxy, self), '_target'), o)
    __float__ = lambda self: float(getattr(super(Proxy, self), '_target'))
    __floordiv__ = lambda self, o: getattr(super(Proxy, self), '_target') // o
    __enter__ = lambda self: getattr(super(Proxy, self), '_target').__enter__()
    __eq__ = lambda self, o: getattr(super(Proxy, self), '_target') == o
    __exit__ = lambda self, exc_type, exc_value, traceback: getattr(super(Proxy, self), '_target').__exit__(exc_type, exc_value, traceback)
    __ge__ = lambda self, o: getattr(super(Proxy, self), '_target') >= o
    __get__ = lambda self, instance, owner: getattr(super(Proxy, self), '_target').__get__(instance, owner)
    __getattr__ = lambda self, attr: getattr(getattr(super(Proxy, self), '_target'), attr)
    __getitem__ = lambda self, key: getattr(super(Proxy, self), '_target')[key]
    __getslice__ = lambda self, i, j: getattr(super(Proxy, self), '_target')[i:j]
    __gt__ = lambda self, o: getattr(super(Proxy, self), '_target') > o
    __hash__ = lambda self: hash(getattr(super(Proxy, self), '_target'))
    __hex__ = lambda self: hex(getattr(super(Proxy, self), '_target'))
    __index__ = lambda self: getattr(super(Proxy, self), '_target').__index__()
    __instancecheck__ = lambda self, instance: isinstance(instance, getattr(super(Proxy, self), '_target'))
    __int__ = lambda self: int(getattr(super(Proxy, self), '_target'))
    __invert__ = lambda self: ~(getattr(super(Proxy, self), '_target'))
    __iter__ = lambda self: iter(getattr(super(Proxy, self), '_target'))
    __le__ = lambda self, o: getattr(super(Proxy, self), '_target') <= o
    __len__ = lambda self: len(getattr(super(Proxy, self), '_target'))
    __long__ = lambda self: long(getattr(super(Proxy, self), '_target'))
    __lshift__ = lambda self, o: getattr(super(Proxy, self), '_target') << o
    __lt__ = lambda self, o: getattr(super(Proxy, self), '_target') < o
    __mod__ = lambda self, o: getattr(super(Proxy, self), '_target') % o
    __mul__ = lambda self, o: getattr(super(Proxy, self), '_target') * o
    __ne__ = lambda self, o: getattr(super(Proxy, self), '_target') != o
    __neg__ = lambda self: -(getattr(super(Proxy, self), '_target'))
    __nonzero__ = lambda self: getattr(super(Proxy, self), '_target').__nonzero__()
    __oct__ = lambda self: oct(getattr(super(Proxy, self), '_target'))
    __or__ = lambda self, o: getattr(super(Proxy, self), '_target') | o
    __pos__ = lambda self: +(getattr(super(Proxy, self), '_target'))
    __pow__ = lambda self, o: getattr(super(Proxy, self), '_target') ** o
    __radd__ = lambda self, o: o + getattr(super(Proxy, self), '_target')
    __rand__ = lambda self, o: o & getattr(super(Proxy, self), '_target')
    __rcmp__ = lambda self, o: cmp(o, getattr(super(Proxy, self), '_target'))
    __rdiv__ = lambda self, o: o.__div__(getattr(super(Proxy, self), '_target'))
    __repr__ = lambda self: '<Proxy to {}>'.format(repr(getattr(super(Proxy, self), '_target')))
    __reversed__ = lambda self: reversed(getattr(super(Proxy, self), '_target'))
    __rfloordiv__ = lambda self, o: o // getattr(super(Proxy, self), '_target')
    __rlshift__ = lambda self, o: o << getattr(super(Proxy, self), '_target')
    __rmod__ = lambda self, o: o % getattr(super(Proxy, self), '_target')
    __rmul__ = lambda self, o: o * getattr(super(Proxy, self), '_target')
    __ror__ = lambda self, o: o | getattr(super(Proxy, self), '_target')
    __rpow__ = lambda self, o: o ** getattr(super(Proxy, self), '_target')
    __rrshift__ = lambda self, o: o >> getattr(super(Proxy, self), '_target')
    __rshift__ = lambda self, o: getattr(super(Proxy, self), '_target') >> o
    __rsub__ = lambda self, o: o - getattr(super(Proxy, self), '_target')
    __rtruediv__ = lambda self, o: o / getattr(super(Proxy, self), '_target')
    __rxor__ = lambda self, o: o ^ getattr(super(Proxy, self), '_target')
    __set__ = lambda self, instance, value: getattr(super(Proxy, self), '_target').__set__(instance, value)
    __setattr__ = lambda self, attr, value: setattr(getattr(super(Proxy, self), '_target'), attr, value)
    __setitem__ = lambda self, key, value: getattr(super(Proxy, self), '_target').__setitem__(key, value)
    __setslice__ = lambda self, i, j, sequence: getattr(super(Proxy, self), '_target').__setslice__(i, j, sequence)
    __sizeof__ = lambda self: getattr(super(Proxy, self), '_target').__sizeof__()
    __str__ = lambda self: str(getattr(super(Proxy, self), '_target'))
    __sub__ = lambda self, o: getattr(super(Proxy, self), '_target') - o
    __subclasshook__ = lambda self, *args, **kwargs: getattr(super(Proxy, self), '_target').__subclasshook__(*args, **kwargs)
    __truediv__ = lambda self, o: getattr(super(Proxy, self), '_target') / o
    __unicode__ = lambda self: unicode(getattr(super(Proxy, self), '_target'))
    __xor__ = lambda self, o: getattr(super(Proxy, self), '_target') ^ o

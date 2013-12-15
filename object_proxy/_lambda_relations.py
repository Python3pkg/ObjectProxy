# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from contextlib import wraps

__all__ = ['get', 'has']


def has(meth):
    return meth in meths


def get(meth):
    return meths[meth]


def catch(wrapped, default=None):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        try:
            return wrapped(*args, **kwargs)
        except:
            return default
    return wrapper


meths = {
    '__abs__': lambda target: abs(target),
    '__add__': lambda target, o: target + o,
    '__and__': lambda target, o: target & o,
    '__bool__': catch(lambda target: bool(target), False),
    '__call__': lambda target, *args, **kwargs: target(*args, **kwargs),
    '__cmp__': lambda target, o: cmp(target, o),
    '__coerce__': lambda target, o: coerce(target, o),
    '__contains__': lambda target, item: item in target,
    '__delattr__': lambda target, attr: delattr(target, attr),
    '__dir__': catch(lambda target: dir(target), []),
    '__divmod__': lambda target, o: divmod(target, o),
    '__float__': lambda target: float(target),
    '__floordiv__': lambda target, o: target // o,
    '__eq__': lambda target, o: target == o,
    '__ge__': lambda target, o: target >= o,
    '__getattr__': lambda target, attr: getattr(target, attr),
    '__getitem__': lambda target, key: target[key],
    '__getslice__': lambda target, i, j: target[i:j],
    '__gt__': lambda target, o: target > o,
    '__hash__': lambda target: hash(target),
    '__hex__': lambda target: hex(target),
    '__instancecheck__': lambda target, instance: isinstance(instance, target),
    '__int__': lambda target: int(target),
    '__invert__': lambda target: ~(target),
    '__iter__': lambda target: iter(target),
    '__le__': lambda target, o: target <= o,
    '__len__': lambda target: len(target),
    '__long__': lambda target: long(target),
    '__lshift__': lambda target, o: target << o,
    '__lt__': lambda target, o: target < o,
    '__mod__': lambda target, o: target % o,
    '__mul__': lambda target, o: target * o,
    '__ne__': lambda target, o: target != o,
    '__neg__': lambda target: -(target),
    '__oct__': lambda target: oct(target),
    '__or__': lambda target, o: target | o,
    '__pos__': lambda target: +(target),
    '__pow__': lambda target, o: target ** o,
    '__radd__': lambda target, o: o + target,
    '__rand__': lambda target, o: o & target,
    '__rcmp__': lambda target, o: cmp(o, target),
    '__rdiv__': lambda target, o: o.__div__(target),
    '__repr__': lambda target: '<Proxy to {}>'.format(repr(target)),
    '__reversed__': lambda target: reversed(target),
    '__rfloordiv__': lambda target, o: o // target,
    '__rlshift__': lambda target, o: o << target,
    '__rmod__': lambda target, o: o % target,
    '__rmul__': lambda target, o: o * target,
    '__ror__': lambda target, o: o | target,
    '__rpow__': lambda target, o: o ** target,
    '__rrshift__': lambda target, o: o >> target,
    '__rshift__': lambda target, o: target >> o,
    '__rsub__': lambda target, o: o - target,
    '__rtruediv__': lambda target, o: o / target,
    '__rxor__': lambda target, o: o ^ target,
    '__str__': lambda target: str(target),
    '__sub__': lambda target, o: target - o,
    '__truediv__': lambda target, o: target / o,
    '__unicode__': lambda target: unicode(target),
    '__xor__': lambda target, o: target ^ o,
}

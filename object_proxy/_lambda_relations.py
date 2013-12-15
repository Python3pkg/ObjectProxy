# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from contextlib import wraps

__all__ = ['method_map']


def catch(wrapped, default=None):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        try:
            return wrapped(*args, **kwargs)
        except:
            return default
    return wrapper


method_map = {
    '__abs__': abs,
    '__add__': lambda target, o: target + o,
    '__and__': lambda target, o: target & o,
    '__bool__': catch(bool, False),
    '__call__': lambda target, *args, **kwargs: target(*args, **kwargs),
    '__cmp__': cmp,
    '__coerce__': coerce,
    '__contains__': lambda target, item: item in target,
    '__delattr__': delattr,
    '__dir__': catch(dir, []),
    '__divmod__': divmod,
    '__float__': float,
    '__floordiv__': lambda target, o: target // o,
    '__eq__': lambda target, o: target == o,
    '__ge__': lambda target, o: target >= o,
    '__getattr__': getattr,
    '__getitem__': lambda target, key: target[key],
    '__getslice__': lambda target, i, j: target[i:j],
    '__gt__': lambda target, o: target > o,
    '__hash__': hash,
    '__hex__': hex,
    '__instancecheck__': lambda target, instance: isinstance(instance, target),
    '__int__': int,
    '__invert__': lambda target: ~(target),
    '__iter__': iter,
    '__le__': lambda target, o: target <= o,
    '__len__': len,
    '__long__': long,
    '__lshift__': lambda target, o: target << o,
    '__lt__': lambda target, o: target < o,
    '__mod__': lambda target, o: target % o,
    '__mul__': lambda target, o: target * o,
    '__ne__': lambda target, o: target != o,
    '__neg__': lambda target: -(target),
    '__oct__': oct,
    '__or__': lambda target, o: target | o,
    '__pos__': lambda target: +(target),
    '__pow__': lambda target, o: target ** o,
    '__radd__': lambda target, o: o + target,
    '__rand__': lambda target, o: o & target,
    '__rcmp__': lambda target, o: cmp(o, target),
    '__rdiv__': lambda target, o: o.__div__(target),
    '__repr__': lambda target: '<Proxy to {}>'.format(repr(target)),
    '__reversed__': reversed,
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
    '__str__': bytes,
    '__sub__': lambda target, o: target - o,
    '__truediv__': lambda target, o: target / o,
    '__unicode__': unicode,
    '__xor__': lambda target, o: target ^ o,
}

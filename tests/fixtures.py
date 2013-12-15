# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

__all__ = ['num', 'X']


num = 23
mylist = [0, 1, 2, 3]
mydict = { 'a': 1, 'b': 2 }


class base(object):
    pass


class X(base):
    """class X"""

    __dict__ = { 'name': 'X' }
    element = 'some element'
    deletable_attr = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


mutablestring = list('abcdef')
changeable_x = X()
changeable_list_1 = [0, 1]
changeable_list_2 = [0, 1, 2, 3]


incr = lambda x: x + 1

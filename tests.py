#!/usr/bin/env python
# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from os import path
from operator import index
from unittest import main, skip, TestCase
from object_proxy import Proxy


class TestProxy(TestCase):

    def setUp(self):
        self.testp = Proxy('testp')
        self.num = Proxy('testp:num')
        self.mylist = Proxy('testp:mylist')
        self.X = Proxy('testp:X')


    def test_all(self):
        self.assertEqual(self.testp.__all__, ['num', 'X'])

    def test_dict(self):
        self.assertEqual(vars(self.X()), { 'name': 'X' })

    def test_doc(self):
        self.assertEqual(self.X.__doc__, 'class X')

    def test_file(self):
        self.assertTrue(
            path.basename(self.testp.__file__) in ('testp.py', 'testp.pyc'))

    def test_name(self):
        self.assertEqual(self.X.__name__, 'X')

    def test_package(self):
        self.assertTrue(self.testp.__package__ is None)

    def test_abs(self):
        self.assertEqual(abs(self.num), 23)

    def test_add(self):
        self.assertEqual(self.num + 2, 25)

    def test_and(self):
        self.assertEqual(self.num & 15, 7)

    def test_bool(self):
        self.assertTrue(bool(self.num))

    def test_call(self):
        incr = Proxy('testp:incr')
        self.assertEqual(incr(2), 3)

    def test_cmp(self):
        self.assertEqual(cmp(self.num, 20), 1)
        self.assertEqual(cmp(self.num, 23), 0)
        self.assertEqual(cmp(self.num, 25), -1)

    def test_coerce(self):
        self.assertEqual(coerce(self.num, 12), coerce(23, 12))

    def test_contains(self):
        self.assertTrue(1 in self.mylist)

    def test_delattr(self):
        assert hasattr(self.X, 'deletable_attr')
        del self.X.deletable_attr
        self.assertFalse(hasattr(self.X, 'deletable_attr'))

    @skip('Called to delete the attribute on an instance of the owner class.')
    def test_delete(self):
        pass

    def test_delitem(self):
        mydict = Proxy('testp:mydict')
        assert 'a' in mydict
        del mydict['a']
        self.assertFalse('a' in mydict)

    def test_delslice(self):
        mutablestring = Proxy('testp:mutablestring')
        assert mutablestring == ['a', 'b', 'c', 'd', 'e', 'f']
        del mutablestring[1:3]
        self.assertEqual(mutablestring, ['a', 'd', 'e', 'f'])

    def test_dir(self):
        self.assertEqual(dir(self.num), dir(23))

    def test_div(self):
        self.assertEqual(self.num.__div__(3), 7)

    def test_divmod(self):
        self.assertEqual(divmod(self.num, 3), (7, 2))

    def test_float(self):
        value = float(self.num)
        self.assertEqual(value, 23.)
        self.assertTrue(isinstance(value, float))

    def test_floordiv(self):
        self.assertEqual(self.num // 3, 7)

    def test_enter_exit(self):
        with self.X() as x:
            self.assertTrue(isinstance(x, self.X._target))

    def test_eq(self):
        self.assertFalse(self.num == 20)
        self.assertTrue(self.num == 23)
        self.assertFalse(self.num == 25)

    def test_ge(self):
        self.assertTrue(self.num >= 20)
        self.assertTrue(self.num >= 23)
        self.assertFalse(self.num >= 25)

    @skip('Called to get the attribute of the owner class.')
    def test_get(self):
        pass

    def test_getattr(self):
        self.assertEqual(getattr(self.X, 'element'), 'some element')

    def test_getitem(self):
        self.assertEqual(self.mylist[1], 1)

    def test_getslice(self):
        self.assertEqual(self.mylist[1:3], [1, 2])

    def test_gt(self):
        self.assertTrue(self.num > 20)
        self.assertFalse(self.num > 23)
        self.assertFalse(self.num > 25)

    def test_hash(self):
        self.assertEqual(hash(self.num), hash(23))

    def test_hex(self):
        self.assertEqual(hex(self.num), '0x17')

    def test_index(self):
        self.assertEqual(index(self.num), 23)

    def test_instancecheck(self):
        x = self.X()
        self.assertTrue(isinstance(x, self.X))

    def test_int(self):
        value = int(self.num)
        self.assertEqual(value, 23)
        self.assertTrue(isinstance(value, int))

    def test_invert(self):
        self.assertEqual(~self.num, -24)

    def test_iter(self):
        self.assertEqual([x for x in iter(self.mylist)], [0, 1, 2, 3])

    def test_le(self):
        self.assertFalse(self.num <= 20)
        self.assertTrue(self.num <= 23)
        self.assertTrue(self.num <= 25)

    def test_len(self):
        self.assertEqual(len(self.mylist), 4)

    def test_long(self):
        value = long(self.num)
        self.assertEqual(value, 23L)
        self.assertTrue(isinstance(value, long))

    def test_lshift(self):
        self.assertEqual(self.num << 2, 92)

    def test_lt(self):
        self.assertFalse(self.num < 20)
        self.assertFalse(self.num < 23)
        self.assertTrue(self.num < 25)

    def test_mod(self):
        self.assertEqual(self.num % 3, 2)

    def test_mul(self):
        self.assertEqual(self.num * 2, 46)

    def test_ne(self):
        self.assertTrue(self.num != 20)
        self.assertFalse(self.num != 23)
        self.assertTrue(self.num != 25)

    def test_neg(self):
        self.assertEqual(-self.num, -23)

    @skip('Called to implement truth value testing and the built-in operation bool()')
    def test_nonzero(self):
        pass

    def test_oct(self):
        self.assertEqual(oct(self.num), '027')

    def test_or(self):
        self.assertEqual(self.num | 15, 31)

    def test_pos(self):
        self.assertEqual(+self.num, 23)

    def test_pow(self):
        self.assertEqual(self.num ** 2, 529)
        self.assertEqual(pow(self.num, 2), 529)

    def test_radd(self):
        self.assertEqual(2 + self.num, 25)

    def test_rand(self):
        self.assertEqual(15 & self.num, 7)

    def test_rcmp(self):
        self.assertEqual(cmp(20, self.num), -1)
        self.assertEqual(cmp(23, self.num), 0)
        self.assertEqual(cmp(25, self.num), 1)

    def test_rdiv(self):
        self.assertEqual(self.num.__rdiv__(70), 3)

    def test_repr(self):
        self.assertEqual(repr(self.num), '<Proxy to 23>')
        self.assertEqual(repr(self.mylist), '<Proxy to [0, 1, 2, 3]>')
        self.assertEqual(repr(self.testp),
                         "<Proxy to <module 'testp' from '{}'>>".format(self.testp.__file__))

    def test_reversed(self):
        self.assertEqual([x for x in reversed(self.mylist)], [3, 2, 1, 0])

    def test_rfloordiv(self):
        self.assertEqual(70 // self.num, 3)

    def test_rlshift(self):
        self.assertEqual(1 << self.num, 8388608)

    def test_rmod(self):
        self.assertEqual(70 % self.num, 1)

    def test_rmul(self):
        self.assertEqual(2 * self.num, 46)

    def test_ror(self):
        self.assertEqual(15 | self.num, 31)

    def test_rpow(self):
        self.assertEqual(2 ** self.num, 8388608)
        self.assertEqual(pow(2, self.num), 8388608)

    def test_rrshift(self):
        self.assertEqual(16777216 >> self.num, 2)

    def test_rshift(self):
        self.assertEqual(self.num >> 2, 5)

    def test_rsub(self):
        self.assertEqual(25 - self.num, 2)

    def test_rtruediv(self):
        self.assertEqual(70 / self.num, 70. / 23.)

    def test_rxor(self):
        self.assertEqual(15 ^ self.num, 24)

    @skip('Called to set the attribute on an instance of the owner class to a new value.')
    def test_set(self):
        pass

    def test_setattr(self):
        x = Proxy('testp:changeable_x')
        setattr(x, 'set_attr', 'set')
        self.assertEqual(x.set_attr, 'set')

    def test_setitem(self):
        l = Proxy('testp:changeable_list_1')
        assert l == [0, 1]
        l[1] = 2
        self.assertEqual(l, [0, 2])

    def test_setslice(self):
        l = Proxy('testp:changeable_list_2')
        assert l == [0, 1, 2, 3]
        l[1:3] = [4]
        self.assertEqual(l, [0, 4, 3])

    @skip('How to test sizeof?')
    def test_sizeof(self):
        pass

    def test_str(self):
        value = str(self.num)
        self.assertEqual(value, b'23')
        self.assertTrue(isinstance(value, str))

    def test_sub(self):
        self.assertEqual(self.num - 2, 21)

    def test_subclasshook(self):
        base = Proxy('testp:base')
        self.assertTrue(issubclass(self.X, base._target))

    def test_truediv(self):
        self.assertEqual(self.num / 3, 23. / 3.)

    def test_unicode(self):
        value = unicode(self.num)
        self.assertEqual(value, '23')
        self.assertTrue(isinstance(value, unicode))

    def test_xor(self):
        self.assertEqual(self.num ^ 15, 24)


if __name__ == '__main__':
    main()

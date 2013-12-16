# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from unittest import skip, TestCase
from object_proxy.lazy import LazyProxy
from object_proxy.context import Context

__all__ = ['TestContext']


class TestContext(TestCase):

    def setUp(self):
        self.default = Context('default')
        self.other = Context('other')

    def tearDown(self):
        Context.activate('default')
        self.default.reset()
        self.other.reset()

    def test_proxy_with_context(self):
        context = self.other
        proxy = LazyProxy('tests.fixtures:num', context=context)
        Context.activate(context)
        self.assertEqual(proxy + 1, 24)

    def test_proxy_from_another_context(self):
        context = self.other
        proxy = LazyProxy('tests.fixtures:num', context=self.default)
        Context.activate(context)
        self.assertRaises(NameError, lambda: proxy + 1)

    def test_use_current_context_by_default(self):
        context = self.other
        Context.activate(context)
        proxy = LazyProxy('tests.fixtures:num')
        self.assertEqual(proxy + 1, 24)
        Context.activate('default')
        self.assertRaises(NameError, lambda: proxy + 1)

    def test_multiple_values(self):
        context = self.other
        proxy = LazyProxy('tests.fixtures:num')
        context.register(proxy, 'tests.fixtures:mylist')

        self.assertEqual(proxy, 23)
        Context.activate(context)
        self.assertEqual(proxy, [0, 1, 2, 3])

    def test_activate(self):
        context = self.other
        assert Context.current == self.default
        Context.activate(context)
        self.assertEqual(Context.current, context)

    def test_activate_str(self):
        context = self.other
        assert Context.current == self.default
        Context.activate('other')
        self.assertEqual(Context.current, context)

    def test_activate_method(self):
        context = self.other
        assert Context.current == self.default
        context.activate()
        self.assertEqual(Context.current, context)

    def test_activate_method_sanity(self):
        context = self.other
        default = self.default
        context.activate()
        default.activate()
        self.assertEqual(Context.current, default)


    def test_inexistent_context(self):
        self.assertRaises(ValueError, Context.activate, 'unknown')

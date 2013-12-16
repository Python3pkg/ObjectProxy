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

    def test_list_contexts(self):
        contexts = Context.contexts
        self.assertEqual(contexts, {
            ('default', Context('default')),
            ('other', Context('other')),
        })

    def test_contain_proxy_1(self):
        context = self.other
        default = self.default
        proxy1 = LazyProxy('tests.fixtures', context=default)
        proxy2 = LazyProxy('tests.fixtures:num', context=context)
        self.assertTrue(id(proxy1) in default)
        self.assertTrue(id(proxy2) in context)
        self.assertFalse(id(proxy1) in context)
        self.assertFalse(id(proxy2) in default)

    def test_contain_proxy_2(self):
        context = self.other
        default = self.default
        proxy = LazyProxy('tests.fixtures', context=default)
        context.register(proxy, 'tests.fixtures:num')
        self.assertTrue(id(proxy) in default)
        self.assertTrue(id(proxy) in context)

    def test_find_proxy_1(self):
        context = self.other
        default = self.default
        proxy1 = LazyProxy('tests.fixtures', context=default)
        proxy2 = LazyProxy('tests.fixtures:num', context=context)

        self.assertEqual(Context.find_proxy(proxy1), {('default', 'tests.fixtures')})
        self.assertEqual(Context.find_proxy(proxy2), {('other', 'tests.fixtures:num')})

    def test_find_proxy_2(self):
        context = self.other
        default = self.default
        proxy = LazyProxy('tests.fixtures', context=default)
        context.register(proxy, 'tests.fixtures:num')
        self.assertEqual(Context.find_proxy(proxy), {
            ('default', 'tests.fixtures'),
            ('other', 'tests.fixtures:num'),
        })

    def test_default_get_child(self):
        context = self.default.get_child('child')
        try:
            self.assertEqual(context.name, 'child')
        finally:
            Context.delete_context(context)

    def test_get_child(self):
        context = self.other.get_child('child')
        try:
            self.assertEqual(context.name, 'other.child')
        finally:
            Context.delete_context(context)

    def test_subcontext_inherits_super_environment(self):
        try:
            context = self.other.get_child('child')
            proxy = LazyProxy('tests.fixtures', context=self.other)
            context.activate()
            self.assertEqual(proxy.__name__, 'tests.fixtures')

        finally:
            Context.delete_context(context)

# coding: UTF-8

# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

__all__ = ['Context']


@apply
def Context():

    _contexts = {}


    class ContextMeta(type):

        @property
        def contexts(cls):
            return set(_contexts.items())


        @property
        def current(cls):
            return cls.__current

        @current.setter
        def current(cls, context):
            context = context or 'default'

            if isinstance(context, Context):
                cls.__current = context
                return

            try:
                cls.__current = _contexts[context]
            except KeyError:
                raise ValueError('context {} not found'.format(context))


        def activate(cls, context):
            cls.current = context


        def find_proxy(cls, proxy):
            proxy_id = id(proxy)
            return [
                (name, context[proxy_id])
                for name, context in _contexts.items()
                if proxy_id in context
            ]


        def delete_context(cls, context):
            _contexts.pop(context.name)


        def __call__(cls, name_or_context):
            if isinstance(name_or_context, Context):
                return name_or_context

            self = _contexts.get(name_or_context)
            if not self:
                self = super(ContextMeta, cls).__call__(name_or_context)
                _contexts[name_or_context] = self

            return self


    class Context(object, metaclass=ContextMeta):

        def __init__(self, name):
            self.name = name
            self.reset()

            # Override activate() class method
            # with simulated instance method
            def activate():
                type(self).activate(self)
            self.activate = activate


        def __get_proxy(self, key):
            proxies = self.__proxies
            if key in proxies:
                return True, proxies[key]
            else:
                return False, None


        def __getitem__(self, key):
            found, proxy = self.__get_proxy(key)
            if found:
                return proxy

            name = self.name
            index = name.rfind('.')

            try:
                if index == -1:
                    raise NameError

                name = name[:index]
                return Context(name)[key]

            except NameError:
                raise NameError('context {} has no proxy {}'.format(self.name, key))


        def __setitem__(self, key, targetname):
            self.__proxies[key] = targetname


        def __contains__(self, proxy_id):
            return proxy_id in self.__proxies


        def get_child(self, name):
            if self.name != 'default':
                name = '.'.join((self.name, name))
            return type(self)(name)


        def reset(self):
            self.__proxies = {}


        def register(self, proxy, targetname):
            self[id(proxy)] = targetname


    Context.current = Context('default')
    return Context

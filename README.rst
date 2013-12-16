.. _BSD New: http://opensource.org/licenses/BSD-3-Clause
.. _GitHUB: https://github.com/Montegasppa/ObjectProxy
.. _mail me: mailto:batalema@cacilhas.info
.. _project issues: https://github.com/Montegasppa/ObjectProxy/issues


=============
 ObjectProxy
=============

This module provides a way to build lazy proxies to any kind of Python
entity.


Use
===


Lazy proxy
----------

To make a proxy to a module, instanciate the ``Proxy`` class with a
string representing the import name of the module as parameter::

    from object_proxy.lazy import LazyProxy

    path = LazyProxy('os.path')


Only when the proxy is used for the first time, the target module is
imported.

To make a proxy to an object or a class, use the colon (``:``) syntax::

    environ = LazyProxy('os:environ')


When the proxy is used, it’s equivalent to::

    from os import environ


Note
~~~~

The functions ``repr()`` and ``id()`` are **not** proxied to target.


Context-dependent proxy
-----------------------

The proxy can be context-dependent.

You must instanciate a context::

    from object_proxy.lazy import LazyProxy
    from object_proxy.context import Context

    gevent_context = Context('gevent')
    eventlet_context = Context('eventlet')

    patch = LazyProxy('gevent.monkey:patch_all', context=gevent_context)
    eventlet_context.register(patch, 'eventlet:monkey_patch')

    # Run monkey patch from gevent
    Context.activate('gevent')
    # Or:
    Context.activate(gevent_context)
    # Or:
    gevent_context.activate()
    # And then:
    patch()

    # Run monkey patch from eventlet
    Context.activate('eventlet')
    # Identical to the previous
    patch()


You can know whether a proxy belongs to a context using ``id()`` and
``in``::

    id(patch) in gevent_context
    # Evaluates to True


To discover which contexts a proxy belongs::

    Context.find_proxy(patch)
    # Evaluates to [('gevent', 'gevent.monkey:patch_all'),
    #               ('eventlet', 'eventlet:monkey_patch')]


Download and install
====================

ObjectProxy can be downloaded from GitHUB_ or installed using ``pip``::

    pip install ObjectProxy


TODO
----

There’s a lot work to do. You can `mail me`_ with suggestions or see the
`project issues`_.


License
=======

ObjectProxy is licensed under `BSD New`_. See ``LICENSE`` file.


Author
------

Rodrigo Cacilhας <batalema@cacilhas.info>

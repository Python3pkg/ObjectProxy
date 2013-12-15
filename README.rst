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


LazyProxy
---------

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


PyPy.js website
===============

pypyjs.github.io is the source for the http://pypyjs.org website, which is hosted via github pages.

.. image:: https://travis-ci.org/pypyjs/pypyjs.github.io.svg?branch=master
    :target: https://travis-ci.org/pypyjs/pypyjs.github.io

PyPy.js: PyPy JIT-compiling to JavaScript at runtime. Because why not.
The main PyPy.js repository is here:

    https://github.com/pypyjs/pypyjs/

All code is available under the MIT License.

unittests
~~~~~~~~~

If you would like to run the unittests, e.g.::

 ~ $ virtualenv pypyjs_env
 ~ $ cd pypyjs_env/
 ~/pypyjs_env $ source bin/activate
 (pypyjs_env)~/pypyjs_env $ pip install --upgrade pip
 (pypyjs_env)~/pypyjs_env $ pip install nose selenium
 (pypyjs_env)~/pypyjs_env $ pip install -e git+https://github.com/pypyjs/pypyjs.git#egg=pypyjs
 (pypyjs_env)~/pypyjs_env $ cd src/pypyjs/
 (pypyjs_env)~/pypyjs_env/src/pypyjs$ nosetests

To run only a subset of tests, e.g.::

 (pypyjs_env)~/pypyjs_env/src/pypyjs$ nosetests tests.test_editor
 (pypyjs_env)~/pypyjs_env/src/pypyjs$ nosetests tests.test_console:PyPyJSSeleniumTests.test_standard_out_streams


Repository Overview
~~~~~~~~~~~~~~~~~~~

+-------------------------+-------------------------------------------------------------------------------------+
| `pypyjs`_               | Main repository to built a PyPyJS release                                           |
+-------------------------+-------------------------------------------------------------------------------------+
| `pypy`_                 | Fork of PyPy with support for compiling to javascript                               |
+-------------------------+-------------------------------------------------------------------------------------+
| `pypyjs-release`_       | Latest release build of PyPyJS, as a handy git submodule                            |
+-------------------------+-------------------------------------------------------------------------------------+
| `pypyjs-release-nojit`_ | Latest release build of PyPyJS, without a JIT                                       |
+-------------------------+-------------------------------------------------------------------------------------+
| `pypyjs-examples`_      | Examples/snippets usage of `pypyjs-release`_ and `pypyjs-release-nojit`_            |
+-------------------------+-------------------------------------------------------------------------------------+
| `pypyjs.github.io`_     | source for `pypyjs.org`_ website use `pypyjs-release`_ and `pypyjs-release-nojit`_  |
+-------------------------+-------------------------------------------------------------------------------------+

.. _pypyjs: https://github.com/pypyjs/pypyjs
.. _pypy: https://github.com/pypyjs/pypy
.. _pypyjs-release: https://github.com/pypyjs/pypyjs-release
.. _pypyjs-release-nojit: https://github.com/pypyjs/pypyjs-release-nojit
.. _pypyjs-examples: https://github.com/pypyjs/pypyjs-examples
.. _pypyjs.github.io: https://github.com/pypyjs/pypyjs.github.io
.. _pypyjs.org: https://pypyjs.org

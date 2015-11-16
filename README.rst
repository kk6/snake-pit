snake-pit
=========

|CircleCI| |Coverage Status| |Requires.io| |Code Climate| |Code Health|
|GitHub license| |PyPI|

*It's Five O'Clock Somewhere*

Depending on the installation or uninstall packages, and then edit the
requirements file.

This package, I was prepared for the purpose of cooperation with
`pip-tools <https://github.com/nvie/pip-tools>`__. Without editing in
the editor ``requirements.in``, it is because I wanted to write
automatically to ``requirements.in`` just by install.

Install snake-pit
-----------------

.. code:: console

    $ pip install snake-pit

Usage
-----

install packages
~~~~~~~~~~~~~~~~

.. code:: console

    $ echo '#requirements.in' > requirements.in

    $ pit install flask pytest
    ...
    Successfully installed Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.1 flask-0.10.1 itsdangerous-0.24 py-1.4.30 pytest-2.8.2
    Append the following packages in requirements.in: flask, pytest

    $ cat requirements.in
    #requirements.in
    flask
    pytest

uninstall packages
~~~~~~~~~~~~~~~~~~

.. code:: console

    $ cat requirements.in
    #requirements.in
    requests
    nose

    $ pit uninstall nose
    Do you want to continue? [y/N]: y
    Uninstalling nose-1.3.7:
      Successfully uninstalled nose-1.3.7
    Remove the following packages from requirements.in: nose

    $ cat requirements.in
    #requirements.in
    requests

Command aliases
---------------

.. code:: console

    $ pit i django  # install django
    $ pit u django  # uninstall django

Configuration
-------------

If you want to use the request file if a complex structure, it is
possible to use a configuration file of YAML format.

Writing configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

For example, we have a structure such as the following:

::

    requirements
    ├── base.in
    └── dev
        ├── base.in
        └── mysql.in

In this case, yaml is described as follows:

.. code:: yaml

    requirements:
      default:
        requirements/base.in
      dev:
        requirements/dev/base.in
      mysql:
        requirements/dev/mysql.in

The program looks for the ``requirements`` key in the YAML file. And as
its child elements, the key name to be passed to the ``--name`` option
of command, it will specify the path to the file to the value.

In addition, the program, if you do not specify the ``--name`` option
refers to the value of the ``default`` of a child element of the
implicit ``requirements``.

If you do not want to set the ``default`` key to the child element of
the ``requirements``, provides a ``default`` key at the top level of the
YAML, among the child elements of the ``requirements`` in its value, key
names that reference by default it is also possible to specify.

Like this:

.. code:: yaml

    default: base
    requirements:
      base:
        requirements/base.in
      dev:
        requirements/dev/base.in
      mysql:
        requirements/dev/mysql.in

And, if you specify the ``--name`` option to run the command,
requirements file that is specified in the YAML is updated.

.. code:: console


    $ pit install mycli -n mysql
    ...
    Successfully installed PyMySQL-0.6.7 Pygments-2.0.2 configobj-5.0.6 mycli-1.5.2 prompt-toolkit-0.46 pycrypto-2.6.1 six-1.10.0 sqlparse-0.1.18 wcwidth-0.1.5
    Append the following packages in requirements/dev/mysql.in: mycli
    requirements/dev/mysql.in has been updated as follows:
    # requirements.mysql.in
    mycli

To set YAML name to the environment variable.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The program looks for the file named 'pit.yml' by default. This file
name can be changed by specifying the file name in the environment
variable ``PIT_CONFIG``.

.. code:: bash:.bashrc

    export PIT_CONFIG=.pitrc

For development
---------------

Update README
~~~~~~~~~~~~~

.. code:: console

    $ pandoc -f markdown -t rst README.md > README.rst

License
-------

Licensed under the MIT, see ``LICENSE``.

.. |CircleCI| image:: https://img.shields.io/circleci/project/kk6/snake-pit.svg?style=flat-square
   :target: https://circleci.com/gh/kk6/snake-pit
.. |Coverage Status| image:: https://img.shields.io/coveralls/kk6/snake-pit.svg?style=flat-square
   :target: https://coveralls.io/github/kk6/snake-pit?branch=master
.. |Requires.io| image:: https://img.shields.io/requires/github/kk6/snake-pit.svg?style=flat-square
   :target: https://requires.io/github/kk6/snake-pit/requirements/
.. |Code Climate| image:: https://img.shields.io/codeclimate/github/kk6/snake-pit/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/kk6/snake-pit
.. |Code Health| image:: https://landscape.io/github/kk6/snake-pit/master/landscape.svg?style=flat-square
   :target: https://landscape.io/github/kk6/snake-pit/master
.. |GitHub license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
   :target: https://raw.githubusercontent.com/kk6/snake-pit/master/LICENSE
.. |PyPI| image:: https://img.shields.io/pypi/v/snake-pit.svg?style=flat-square
   :target: https://pypi.python.org/pypi/snake-pit

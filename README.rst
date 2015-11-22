snake-pit
=========

|CircleCI| |Coverage Status| |Requires.io| |Code Climate| |Code Health|
|GitHub license| |PyPI|

*It's Five O'clock Somewhere*

Introduction
------------

Design Concepts
~~~~~~~~~~~~~~~

I'm using ordinary `pip-tools <https://github.com/nvie/pip-tools>`__ .
pip-tools is great, but the package of installation, is to edit the
``requirements.in`` file every time the uninstall in the editor it was
somewhat cumbersome. So, I have developed a snake-pit. snake-pit, which
takes you by writing automatically package name to ``requirements.in``
After the installation of the package is successful. Even when the
uninstall, will remove the automatically package name from
requirements.in.

Stand-alone
~~~~~~~~~~~

snake-pit is desirable to use in combination with a pip-tools, but it
does not mean that its never dependent to pip-tools. snake-pit is
available in stand-alone. It is a good idea to use instead of
``pip freeze> requirements.txt``.

Installation
------------

Using pip
~~~~~~~~~

snake-pit is possible to install pip.

.. code:: console


    $ pip install snake-pit

Get the Code
~~~~~~~~~~~~

It is also possible to get the source code from Github.

.. code:: console


    $ git clone git@github.com:kk6/snake-pit.git

You may want to install in the pip editable mode.

.. code:: console


    $ pip install -e .

Usage
-----

Installing Packages
~~~~~~~~~~~~~~~~~~~

To install the Python package using the snake-pit, do the following. It
is only different character and if you use a pip.

.. code:: console


    $ pit install flask

Unlike pip, snake-pit will write the package name to automatically
requirements file. Once you have successfully installed the package.

Requirements Files
~~~~~~~~~~~~~~~~~~

Although I mentioned earlier, snake-pit has been designed to be aware of
the combination of the pip-tools. Therefore, the **Requirements file**
to say here, as that term is pip-tools, is a file, such as a specified
to ``requirements.in`` to pip-tools's ``pip-compile`` command.

As below, it is possible to specify a file path to reference
``--requirements, in -r`` option. This is priority than the set of
configuration files, which will be described later.

.. code:: console


    $ pit install pytest -r dev-requirements.in

Configuration Files
~~~~~~~~~~~~~~~~~~~

If the ``--requirements`` option is not specified, snake-pit uses the
configuration file to search for the requirements file.

Config file is intended to be managed by a name in the path to the
requirements file. Please describe in YAML format file.In hash it will
describe as ``<name of the file path> : <path to file>``. The only
required key is ``default``. This is referred to by default when
``--name, -n`` option is not specified.

If there is no configuration file, or if the configuration file can not
be read, the default configuration is used. By default, it will read and
write ``requirements.in``.

For example, you are managing by dividing the requirements file as
follows:

::

    requirements
    ├── base.in
    └── dev
        ├── base.in
        └── mysql.in

As follows, It is troublesome to specify the long file path for each
installation.

.. code:: console


    $ pit install mycli -r requirements/dev/mysql.in

So, we will use the configuration file. Let's described as follows:

.. code:: yaml


    default:
      requirements/base.in
    dev:
      requirements/dev/base.in
    mysql:
      requirements/dev/mysql.in

Save as ``pit.yml``. By default, snake-pit enforce this file name, but
this can be changed by setting environment variables (see below).

Now you need only to specify the name to ``--name`` option.

.. code:: console


    $ pit install mycli -n mysql
    ...
    Successfully installed PyMySQL-0.6.7 Pygments-2.0.2 configobj-5.0.6 mycli-1.5.2 prompt-toolkit-0.46 pycrypto-2.6.1 six-1.10.0 sqlparse-0.1.18 wcwidth-0.1.5
    Append the following packages in requirements/dev/mysql.in: mycli
    requirements/dev/mysql.in has been updated as follows:
    # requirements.mysql.in
    mycli

Default Configuration
~~~~~~~~~~~~~~~~~~~~~

If the configuration file fails to load or did not exist, the default
configuration is used. By default, this is as follows.

.. code:: yaml


    default:
        requirements.in

Set the configuration file name in the environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to set the path to the configuration file in the
environment variable ``PIT_CONFIG_PATH``. If this environment variable
is set, snake-pit looks for a there instead of ``pit.yml`` immediately
below.

.. code:: console


    $ mv pit.yml .pitrc
    $ export PIT_CONFIG_PATH=.pitrc

Uninstall Packages
~~~~~~~~~~~~~~~~~~

Uninstall Packages also, is almost the same as the installation.

.. code:: console


    $ pit uninstall nose

As well as the installation, ``--requirements, -r`` and ``--name, -n``
options are available.

.. code:: console


    $ pit uninstall pytest -n test

Further, by using the ``--auto, -a`` options, of all the packages to the
specified package depends, is possible to remove at once what is
unnecessary.

.. code:: console

    $ pit uninstall bpython httpie --auto
    Specified package and becomes unnecessary by which they are removed, it will remove the following packages:

    curtsies
    httpie
    greenlet
    blessings
    bpython

    Are you sure? [y/N]:

Aliases
-------

snake-pit You can also use the alias of sub-command.

.. code:: console

    $ pit i django  # install django
    $ pit u django  # uninstall django

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

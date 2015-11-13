# pip-require
[![CircleCI](https://img.shields.io/circleci/project/kk6/pip-require.svg?style=flat-square)](https://circleci.com/gh/kk6/pip-require)
[![Requires.io](https://img.shields.io/requires/github/kk6/pip-require.svg?style=flat-square)](https://requires.io/github/kk6/pip-require/requirements/)

Depending on the installation or uninstall packages, and then edit the requirements file.

## Install

```
$ python setup.py install
```

## Usage

### install

```
$ echo '#requirements.in' > requirements.in

$ pir install flask pytest
...
Successfully installed Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.1 flask-0.10.1 itsdangerous-0.24 py-1.4.30 pytest-2.8.2
Append the following packages in requirements.in: flask, pytest

$ cat requirements.in
#requirements.in
flask
pytest
```

### uninstall

```
$ cat requirements.in
#requirements.in
requests
nose

$ pir uninstall nose
Do you want to continue? [y/N]: y
Uninstalling nose-1.3.7:
  Successfully uninstalled nose-1.3.7
Remove the following packages from requirements.in: nose

$ cat requirements.in
#requirements.in
requests
```

## Aliases

```
$ pir i django  # install django
$ pir u django  # uninstall django
```

## Develop

### Update README

```
$ pandoc -f markdown -t rst README.md > README.rst
```

## License
MIT

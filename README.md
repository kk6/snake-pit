# pip-require

Depending on the installation or uninstall packages, and then edit the requirements file.

## Install

```
$ python setup.py install
```

## Example

```
$ echo '#requirements.in' > requirements.in

$ pir flask pytest
...
Successfully installed Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.1 flask-0.10.1 itsdangerous-0.24 py-1.4.30 pytest-2.8.2
Append the following packages in requirements.in: flask, pytest

$ cat requirements.in
#requirements.in
flask
pytest
```

## Develop

### Update README

```
$ pandoc -f markdown -t rst README.md > README.rst
```

## License
MIT

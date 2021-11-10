# Telliot Release Process

This project uses [semantic versioning](https://packaging.python.org/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme), which is used for releases on [PyPI](https://pypi.org/) and in the Github release tags.

## How to manually publish to PyPI

1) Create the config file. `~/.pypirc`:
```
[distutils]
index-servers =
   pypi
   testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = tellorofficial

[testpypi]
repository = https://test.pypi.org/legacy/
username = tellorofficial
```
2) Update the `__version__` within `__init__.py` in the project's source directory. 
3) After, in the project's home directory, use [flit](https://github.com/takluyver/flit) to publish to PyPI with the command `flit publish`. You can publish to the test PyPI server with `flit publish --repository testpypi`.


## Github release tags

TODO
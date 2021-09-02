from setuptools import setup
from setuptools import find_packages

from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

name = 'pytelliot'
version = '0.0'
release = '0.0.0'

setup(
    name=name,
    version=release,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='www.tellor.io',
    license='MIT',
    cmdclass=cmdclass,
    author='Tellor Contributors',
    author_email='info@tellor.io',
    description='Tellor Client',
    python_requires='>=3.8',
    install_requires=['sphinx',
                      'sphinx-rtd-theme'],
    tests_require=['pytest',
                   'pytest-cov',
                   'tox',
                   'tox-travis'],
    command_options={
        'build_sphinx': {
        'project': ('setup.py', name),
        'version': ('setup.py', version),
        'release': ('setup.py', release),
        'source_dir': ('setup.py', 'docs/source')}},

)

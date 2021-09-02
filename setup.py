from setuptools import setup
from setuptools import find_packages

setup(
    name='pytelliot',
    version='0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='www.tellor.io',
    license='MIT',
    author='Tellor Contributors',
    author_email='info@tellor.io',
    description='Tellor Client',
    python_requires='>=3.8',
    install_requires=['atom'],
    tests_require=['pytest',
                   'pytest-cov',
                   'tox',
                   'tox-travis']
)

# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

PACKAGE = 'django_auto_sluggable'
VERSION = '0.1'

setup(
    name=PACKAGE, version=VERSION,
    description="Tiny Django app to make working with slugs a little easier.",
    packages=[ 'django_auto_sluggable' ],
    license='MIT',
    author='James Aylett',
    url = 'http://tartarus.org/james/computers/django/',
)

# coding=utf-8
"""Setup file for distutils / pypi."""
try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages

setup(
    name='django-user-map',
    version='0.1.2',
    author='Akbar Gumbira',
    author_email='akbargumbira@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[],
    url='http://pypi.python.org/pypi/django-user-map/',
    license='LICENSE.txt',
    description=('A simple app for creating a community user map in your '
                 'django web site.'),
    long_description=open('README.md').read(),
    install_requires=[
        "Django==1.7",
        "django-leaflet==0.14.1",
        "psycopg2==2.5.4",
        "factory-boy==2.4.1",
        "django-bootstrap-form==3.1",
    ],
    test_suite='user_map.run_tests.run',
)

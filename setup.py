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
    version='1.1.1',
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
        "Django>=1.8",
        "django-leaflet==0.18.0",
        "psycopg2",
        "django-bootstrap-form",
        "djangorestframework",
        "djangorestframework-gis",
        "Pillow"
    ],
    tests_require=[
        "factory-boy>=2.4.1",
    ],
    test_suite='user_map.run_tests.run',
)

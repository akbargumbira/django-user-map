# coding=utf-8
"""Setup file for distutils / pypi."""
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name='insafe-user-map',
    version='0.1.0',
    author='Akbar Gumbira',
    author_email='akbar.gumbira@aifdr.org',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[],
    url='http://pypi.python.org/pypi/inasafe-user-map/',
    license='LICENSE.txt',
    description='A simple app for creating a user map in your django web site.',
    long_description=open('README.md').read(),
    install_requires=[
        "Django==1.6.6",
        "django-leaflet==0.14.1",
        "psycopg2==2.5.3",
        "factory-boy==2.4.1",
        "django-bootstrap-form==3.1",
    ],
)

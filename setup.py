# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# if you change this version, also change __init__.py and cmdline.py
version = "0.1.d"

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.TXT') as f:
    license = f.read()

tests_require = [
    'nose',
    'virtualenv>=1.7',
    'scripttest>=1.1.1',
    'mock',
]

install_requires = [
    'APScheduler==2.0.3',
    'flask==0.8',
    'PyYAML==3.10',
]

data = dict(
    name    = 'speedrack',
    version = version,

    author       = 'Clint Howarth',
    author_email = 'clint.howarth@gmail.com',

    url = 'https://bitbucket.org/clinthowarth/speedrack',

    install_requires = install_requires,
    tests_require    = tests_require,
    extras_require   = {'test': tests_require},
    test_suite       = 'nose.collector',

    packages             = find_packages(exclude=('tests')),
    entry_points         = {
        'console_scripts' : [ 'speedrack = speedrack.cmdline:main', ]
    },
    include_package_data = True,
    
    license          = 'BSD License',
    description      = 'yet another task runner, with web interface and execution history',
    long_description = readme,
    keywords         = "speedrack cron webcron",
    classifiers      = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Logging',
    ],
)

setup(**data)

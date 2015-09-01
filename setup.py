#!/usr/bin/env python

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

version = "0.0.1"

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.md').read()

long_description = readme

if sys.argv[-1] == 'readme':
    print(long_description)
    sys.exit()

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='aws_info',
    version=version,
    author='Jon Hadfield',
    author_email='jon.hadfield@lessknown.co.uk',
    url='http://github.com/jonhadfield/aws_info',
    install_requires=['boto>=2.38.0'],
    description='Get info on an aws account.',
    long_description=long_description,
    packages=['aws_info'],
    platforms='any',
    license='MIT',
    scripts=['bin/aws_info'],
    package_dir={'aws_info': 'aws_info'},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Operating System',
        'Topic :: System :: Networking',
    ],
    keywords=(
        'hosts, Python, network'
    ),
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)

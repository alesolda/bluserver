#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""
import sys
import uuid
from setuptools import setup, find_packages

try:
    from pip import req
except ImportError:
    from pip._internal import req


# with open('README.md') as readme_file:
    # readme = readme_file.read()

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported.')

requirements = [str(ir.req) for ir in req.parse_requirements('requirements.txt', session=uuid.uuid1()) if ir.req]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]


package_name = 'bluserver'


setup(
    name=package_name,
    version='0.1.0',
    url='https://github.com/alesolda/bluserver',
    description='bluserver',
    # long_description=readme,
    author='Alejandro Solda',
    author_email='alejandrosolda at g m a i l dot c o m',
    packages=find_packages(include=['bluserver*', ]),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='bluserver',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'bluserver = bluserver.__main__:main',
        ]
    },
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

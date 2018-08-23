# coding: utf-8

from codecs import open
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

__version__ = None
with open(os.path.join(here, 'legipy', 'version.py')) as version:
    exec(version.read())
assert __version__ is not None

with open(os.path.join(here, 'README.md')) as readme:
    LONG_DESC = readme.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='legipy',
    version=__version__,

    description='Python client for legifrance.gouv.fr website',
    long_description=LONG_DESC,
    license="MIT",

    url='https://github.com/regardscitoyens/legipy',
    author='Regards Citoyens',
    author_email='contact@regardscitoyens.org',

    include_package_data=True,

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    keywords='scraping politics data france',

    packages=find_packages(),

    install_requires=requirements,

    # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies
    extras_require={
        'test':
            [
                'coverage < 4.5, >= 4.4',
                'pytest < 3.5, >= 3.4',
                'pytest-cov < 2.6, >= 2.5',
                'vcrpy < 1.12, >= 1.11',  # vcr
            ]
    },

    entry_points={
        'console_scripts': [
            'legipy = legipy.__main__:cli'
        ]
    },

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
)

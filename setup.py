import os
import re

from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

requires = []


def get_version():
    init = open(os.path.join(ROOT, 'cerberus_docs', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='Cerberus-docs',
    version=get_version(),
    description='Cerberus docs generator',
    long_description=open('README.rst').read(),
    author='NODA Intelligent Systems',
    author_email='mikael.brorsson@noda.se',
    url='https://github.com/noda/cerberus-docs',
    scripts=[],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['cerberus-docs = cerberus_docs.cli:main']
    },
    install_requires=requires,
    license='MIT License',
    python_requires='>= 3.7',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)

from setuptools import setup
setup( name = 'csh'
    , version = '0.1.1'
    , description = 'A collection of utilities for interacting with CSH services.'
    , author = 'Matt Gambogi'
    , author_email = 'gambogi@csh.rit.edu'
    , url = 'http://www.github.com/gambogi/cshpy'
    , packages = ['csh']
    , license = 'MIT'
    , install_requires=[
        "sasl==0.1.3",
        "python-ldap==2.4.15",
        "requests==2.3.0",
        "wsgiref==0.1.2",
    ],
    )

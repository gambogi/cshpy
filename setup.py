from setuptools import setup

with open('requirements.txt') as r:
    requirements = r.readlines()

with open('VERSION') as v:
    version = v.read()

setup(name='csh',
      version=version,
      author='Matt Gambogi',
      author_email='gambogi@csh.rit.edu',
      url=('https://github.com/gambogi/cshpy'),
      packages=['csh'],
      description = 'A collection of utilities for interacting with CSH '
                    'services.',
      install_requires=requirements
)

from setuptools import setup, find_packages

setup(name='csh',
      version=open('VERSION').read().strip(),
      author='Matt Gambogi',
      author_email='gambogi@csh.rit.edu',
      url=('https://github.com/gambogi/cshpy'),
      packages=['csh'],
      description = 'A collection of utilities for interacting with CSH '
                    'services.',
      install_requires=open('requirements.txt').readlines(),
      include_package_data=True)

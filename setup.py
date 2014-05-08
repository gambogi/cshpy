from distutils.core import setup
setup( name='csh'
	 , version='0.1'
	 , description='A collection of utilities for interacting with CSH services.'
	 ,  author='Matt Gambogi'
	 ,  author_email='gambogi@csh.rit.edu'
	 ,  url='http://www.github.com/gambogi/csh-py'
	 ,  py_modules=[ 'ldap'
		           , 'webnews'
		           , 'member'
		           ]
     ,  license="MIT"
	 )

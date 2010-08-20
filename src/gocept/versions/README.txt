===============
gocept.versions
===============

Basic usage
===========


Create a package to include versions information:

>>> import os
>>> mkdir('customversions')
>>> os.chdir('customversions')
>>> write('setup.py',
... """
... from setuptools import setup
...
... setup(
...     name='customversions',
...     packages=('customversions',),
...     include_package_data=True,
...     version='0.1')
... """)
>>> write('README.txt', 'readme')
>>> mkdir('customversions')
>>> write('customversions', '__init__.py', '# package')
>>> write('customversions', 'versions.cfg',
... """
... [versions]
... Foo-Package = 17.5
... """)
>>> write('MANIFEST.in',
... """
... recursive-include customversions *.cfg
... """)

Create an sdist:

>>> print system(buildout + ' setup setup.py sdist')  # doctest: +ELLIPSIS
Running setup script 'setup.py'.
...
hard linking customversions/versions.cfg -> customversions-0.1/customversions
...
>>> ls(sample_buildout, 'customversions', 'dist')
-  customversions-0.1.tar.gz


In a buildout use gocept.versions as extension with ``customversions`` as
package which contains the versions:

>>> import zc.buildout.testing
>>> zc.buildout.testing.install_develop(
...     'zc.recipe.egg', os.path.join(sample_buildout, 'develop-eggs'))
>>> os.chdir(sample_buildout)
>>> write('buildout.cfg',
... """
... [buildout]
... extensions = gocept.versions
... versions-specification = customversions:versions.cfg
... find-links = %s
... parts = install-foo
...
... [install-foo]
... recipe = zc.recipe.egg
... eggs = Foo-Package
...
... """ % os.path.join(sample_buildout, 'customversions', 'dist'))

The extension pins the version to 17.5:

>>> print system(buildout), # doctest: +ELLIPSIS
Getting distribution for 'customversions'.
install_dir /sample-buildout/eggs/...
Got customversions 0.1.
Setting versions from customversions:versions.cfg /sample-buildout/eggs/customversions-0.1-py...egg/customversions/versions.cfg)
Installing install-foo.
Getting distribution for 'Foo-Package==17.5'.
zip_safe flag not set; analyzing archive contents...
Couldn't find index page for 'zc.recipe.egg' (maybe misspelled?)
Couldn't find index page for 'Foo-Package' (maybe misspelled?)
While:
  Installing install-foo.
  Getting distribution for 'Foo-Package==17.5'.
Error: Couldn't find a distribution for 'Foo-Package==17.5'.


It is also possible to pin the version of the version package:

>>> write('buildout.cfg',
... """
... [buildout]
... extensions = gocept.versions
... versions-specification = customversions:versions.cfg
... versions = versions
... find-links = %s
... parts = install-foo
...
... [versions]
... customversions = 0.2
...
... [install-foo]
... recipe = zc.recipe.egg
... eggs = Foo-Package
...
... """ % os.path.join(sample_buildout, 'customversions', 'dist'))
>>> print system(buildout),
Getting distribution for 'customversions==0.2'.
While:
  Installing.
  Loading extensions.
  Getting distribution for 'customversions==0.2'.
Error: Couldn't find a distribution for 'customversions==0.2'.


Using the versions egg as develop egg is not as easy as it seems, though. The
develop eggs are registered *after* the extensions have been run. 

Change the version in the versions package:

>>> write('customversions', 'customversions', 'versions.cfg',
... """
... [versions]
... Foo-Package = 18.5
... """)


In the first run, buildout doesn't pick up the new versions, because it is
still using the old versions package:

>>> write('buildout.cfg',
... """
... [buildout]
... extensions = gocept.versions
... develop = ${buildout:directory}/customversions
... versions-specification = customversions:versions.cfg
... find-links = %s
... parts = install-foo
...
... [install-foo]
... recipe = zc.recipe.egg
... eggs = Foo-Package
...
... """ % os.path.join(sample_buildout, 'customversions', 'dist'))
>>> print system(buildout),  # doctest: +ELLIPSIS
Setting versions from customversions:versions.cfg /sample-buildout/eggs/customversions-0.1-py...egg/customversions/versions.cfg)
Develop: '/sample-buildout/customversions'
install_dir /sample-buildout/develop-eggs/...
Installing install-foo.
Getting distribution for 'Foo-Package==17.5'.
Couldn't find index page for 'zc.recipe.egg' (maybe misspelled?)
Couldn't find index page for 'Foo-Package' (maybe misspelled?)
While:
  Installing install-foo.
  Getting distribution for 'Foo-Package==17.5'.
Error: Couldn't find a distribution for 'Foo-Package==17.5'.

In the second run it is picking up the new version and using the customversions
package as development package:

>>> print system(buildout),  # doctest: +ELLIPSIS
Setting versions from customversions:versions.cfg /sample-buildout/customversions/customversions/versions.cfg)
Develop: '/sample-buildout/customversions'
install_dir /sample-buildout/develop-eggs/...
Installing install-foo.
Getting distribution for 'Foo-Package==18.5'.
Couldn't find index page for 'zc.recipe.egg' (maybe misspelled?)
Couldn't find index page for 'Foo-Package' (maybe misspelled?)
While:
  Installing install-foo.
  Getting distribution for 'Foo-Package==18.5'.
Error: Couldn't find a distribution for 'Foo-Package==18.5'.

That the develop versions egg is picked up too late is problem when a develop
egg should be used in the initial run. To demonstrate this, clean up a bit
first:


>>> write('buildout.cfg',
... """
... [buildout]
... parts =
... """)
>>> _ = system(buildout), 
>>> remove('eggs', 'customversions-0.1-py2.7.egg')  # XXX
>>> remove('develop-eggs', 'customversions.egg-link')

Create a buildout which uses customversions as develop egg:

>>> write('buildout.cfg',
... """
... [buildout]
... extensions = gocept.versions
... develop = ${buildout:directory}/customversions
... versions-specification = customversions:versions.cfg
... parts = install-foo
...
... [install-foo]
... recipe = zc.recipe.egg
... eggs = Foo-Package
...
... """)

Buildout fails now, as it cannot load the customversions egg:

>>> print system(buildout),
Getting distribution for 'customversions'.
Couldn't find index page for 'customversions' (maybe misspelled?)
While:
  Installing.
  Loading extensions.
  Getting distribution for 'customversions'.
Error: Couldn't find a distribution for 'customversions'.


To allow using the versions as develop egg, special treat is required:

>>> write('buildout.cfg',
... """
... [buildout]
... extensions = gocept.versions
... versions-specification = customversions:versions.cfg
... versions-specification-develop = ${buildout:directory}/customversions
... parts = install-foo
...
... [install-foo]
... recipe = zc.recipe.egg
... eggs = Foo-Package
...
... """)
>>> print system(buildout),  # doctest: +ELLIPSIS +REPORT_NDIFF
install_dir /sample-buildout/develop-eggs/...
Setting versions from customversions:versions.cfg /sample-buildout/customversions/customversions/versions.cfg)
Installing install-foo.
Getting distribution for 'Foo-Package==18.5'.
Couldn't find index page for 'Foo-Package' (maybe misspelled?)
While:
  Installing install-foo.
  Getting distribution for 'Foo-Package==18.5'.
Error: Couldn't find a distribution for 'Foo-Package==18.5'.


Recursive versions
==================

The configuration file in the custom versions package is loaded like a normal
buildout configuration: extends is honoured:

>>> write('customversions', 'customversions', 'versions.cfg',
... """
... [buildout]
... extends = otherversions.cfg
... """)
>>> write('customversions', 'customversions', 'otherversions.cfg',
... """
... [versions]
... Foo-Package = 19.5
... """)
>>> print system(buildout),  # doctest: +ELLIPSIS +REPORT_NDIFF
install_dir /sample-buildout/develop-eggs/...
Setting versions from customversions:versions.cfg /sample-buildout/customversions/customversions/versions.cfg)
Installing install-foo.
Getting distribution for 'Foo-Package==19.5'.
Couldn't find index page for 'Foo-Package' (maybe misspelled?)
While:
  Installing install-foo.
  Getting distribution for 'Foo-Package==19.5'.
Error: Couldn't find a distribution for 'Foo-Package==19.5'.

Specifying the versions section
===============================

Not implemented, yet. Currently the versions section must be named
``[versions]``.


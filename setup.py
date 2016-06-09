from setuptools import setup, find_packages


setup(
    name='gocept.versions',
    version='0.3dev',
    author='gocept gmbh & co. kg',
    author_email='mail@gocept.com',
    url='https://bitbucket.org/gocept/gocept.versions',
    description='Buildout version managment extension',
    long_description=(
        open('README.txt').read() +
        '\n\n' +
        open('CHANGES.txt').read()),

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='ZPL',
    namespace_packages=['gocept'],
    install_requires=[
        'setuptools',
        'zc.buildout',
    ],
    extras_require=dict(test=[
        'zc.recipe.egg',
        'zope.testing',
    ]),
    entry_points="""
    [zc.buildout.extension]
    default = gocept.versions.versions:extension
    """,
)

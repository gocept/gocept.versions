# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import ConfigParser
import pkg_resources
import zc.buildout
import zc.buildout.easy_install

class Versions(object):

    def __init__(self, buildout):
        self.buildout = buildout
        self.versions = self.buildout['buildout'].get('versions')
        if not self.versions:
            self.versions = self.buildout['buildout']['version'] = 'versions'
        self.spec = self.buildout['buildout']['versions-specification']
        self.versions_package, self.versions_path = self.spec.split(':', 1)

    def __call__(self):
        self._install_package()
        self._install_versions()

    def _install_package(self):
        path = [self.buildout['buildout']['develop-eggs-directory']]
        # XXX offline mode
        dest = self.buildout['buildout']['eggs-directory']
        zc.buildout.easy_install.install(
            [self.versions_package], dest, path=path,
            working_set=pkg_resources.working_set,
            links = self.buildout['buildout'].get('find-links', '').split(),
            index = self.buildout['buildout'].get('index'),
            newest=self.buildout.newest,
            allow_hosts=self.buildout._allow_hosts)

    def _install_versions(self):
        versions = {}
        parser = ConfigParser.RawConfigParser()
        parser.optionxform = lambda s: s
        filename = pkg_resources.resource_filename(
            self.versions_package, self.versions_path)
        print "Setting versions from %s (%s)" % (self.spec, filename)
        parser.read(filename)
        versions = dict(parser.items('versions'))
        zc.buildout.easy_install.default_versions(versions)

def extension(buildout):
    Versions(buildout)()

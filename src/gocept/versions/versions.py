# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import os.path
import pkg_resources
import sys
import zc.buildout
import zc.buildout.buildout
import zc.buildout.easy_install

class Versions(object):

    def __init__(self, buildout):
        self.buildout = buildout
        self.versions = self.buildout['buildout'].get('versions')
        if not self.versions:
            self.versions = self.buildout['buildout']['version'] = 'versions'
        self.spec = self.buildout['buildout']['versions-specification']
        self.versions_package, self.versions_path = self.spec.split(':', 1)
        self.develop = self.buildout['buildout'].get(
            'versions-specification-develop')

    def __call__(self):
        self._install_package()
        self._install_versions()

    def _install_package(self):
        # XXX offline mode
        path = self.buildout['buildout']['develop-eggs-directory']
        requirement = pkg_resources.Requirement.parse(self.versions_package)
        if requirement not in pkg_resources.working_set:
            if self.develop:
                self._old_path = sys.path[:]
                sys.path.insert(0, path)
                zc.buildout.easy_install.develop(self.develop, path)
            dest = self.buildout['buildout']['eggs-directory']
            zc.buildout.easy_install.install(
                [self.versions_package], dest, path=[path],
                working_set=pkg_resources.working_set,
                links=self.buildout['buildout'].get(
                    'find-links', '').split(),
                index=self.buildout['buildout'].get('index'),
                newest=self.buildout.newest,
                    allow_hosts=self.buildout._allow_hosts)

    def _install_versions(self):
        versions = {}
        # XXX we're using an internal function here
        filename = pkg_resources.resource_filename(
            self.versions_package, self.versions_path)
        config = zc.buildout.buildout._open(
            os.path.dirname(filename), filename, [],
            self.buildout._annotated['buildout'].copy(), {})
        print "Setting versions from %s (%s)" % (self.spec, filename)
        config = zc.buildout.buildout._unannotate(config)
        versions = config['versions']
        zc.buildout.easy_install.default_versions(versions)


def extension(buildout):
    Versions(buildout)()

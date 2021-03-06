# -*- coding: utf-8 -*-
"""
Package Updater
"""

#*****************************************************************************
#       Copyright (C) 2015 Volker Braun <vbraun.name@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import re
import os

import logging
log = logging.getLogger()

from sage_bootstrap.env import SAGE_ROOT
from sage_bootstrap.package import Package
from sage_bootstrap.download import Download



class PackageUpdater(object):

    def __init__(self, package_name, new_version):
        self.__package = None
        self.package_name = package_name
        self._update_version(new_version)

    def _update_version(self, new_version):
        old = Package(self.package_name)
        package_version_txt = os.path.join(old.path, 'package-version.txt')
        with open(package_version_txt, 'w') as f:
            f.write(new_version.strip() + '\n')

    @property
    def package(self):
        if self.__package is None:
            self.__package = Package(self.package_name)
        return self.__package
        
    def download_upstream(self, download_url):
        tarball = self.package.tarball
        print('Downloading tarball to {0}'.format(tarball.upstream_fqn))
        Download(download_url, tarball.upstream_fqn).run()

    def fix_checksum(self):
        checksums_ini = os.path.join(self.package.path, 'checksums.ini')
        with open(checksums_ini, 'w') as f:
            f.write(self.checksums_ini())

    def checksums_ini(self):
        tarball = self.package.tarball
        result = [
            'tarball=' + self.package.tarball_pattern,
            'sha1=' + tarball._compute_sha1(),
            'md5=' + tarball._compute_md5(), 
            'cksum=' + tarball._compute_cksum(),
            ''   # newline at end
        ]
        return '\n'.join(result)

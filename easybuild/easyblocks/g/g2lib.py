##
# Copyright 2009-2012 Ghent University
# Copyright 2009-2012 Stijn De Weirdt
# Copyright 2010 Dries Verdegem
# Copyright 2010-2012 Kenneth Hoste
# Copyright 2011 Pieter De Baets
# Copyright 2011-2012 Jens Timmerman
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing g2lib, implemented as an easyblock
"""

import os
import shutil

from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.modules import get_software_root


class EB_g2lib(ConfigureMake):
    """Support for building g2clib GRIB2 library."""

    def configure_step(self):
        """No configuration needed"""
        pass

    def build_step(self):
        """Build by supplying required make options, and running build_step."""

        jasper = get_software_root('JASPER')
        if not jasper:
            self.log.error("JasPer module not loaded?")

        makeopts = 'CC="%s" FC="%s" INCDIR="-I%s/include"' % (os.getenv('CC'), os.getenv('F90'), jasper)
        self.cfg.update('makeopts', makeopts)

        super(EB_g2lib, self).build_step()

    def install_step(self):
        """Install by copying generated library to install directory."""

        try:
            targetdir = os.path.join(self.installdir, "lib")
            os.mkdir(targetdir)
            fn = "libg2.a"
            shutil.copyfile(os.path.join(self.cfg['start_dir'], fn), os.path.join(targetdir, fn))
        except OSError, err:
            self.log.error("Failed to copy files to install dir: %s" % err)

    def sanity_check_step(self):
        """Custom sanity check for g2lib."""

        custom_paths = {
                        'files': ["lib/libg2.a"],
                        'dirs': []
                       }

        super(EB_g2lib, self).sanity_check_step(custom_paths=custom_paths)

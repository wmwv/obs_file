#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2008-2013 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
from lsst.pipe.tasks.processCcd import ProcessCcdTask
from lsst.pipe.base.argumentParser import ArgumentParser
import lsst.afw.table as afwTable

from .fileisr import FileIsrTask


class ProcessFileConfig(ProcessCcdTask.ConfigClass):
    """Config for ProcessFile"""

    def setDefaults(self):
        ProcessCcdTask.ConfigClass.setDefaults(self)
        self.isr.retarget(FileIsrTask)
        self.calibrate.doAstrometry = False
        self.calibrate.doPhotoCal = False


class ProcessFileTask(ProcessCcdTask):
    """Process a CCD

    Available steps include:
    - calibrate
    - detect sources
    - measure sources
    """
    ConfigClass = ProcessFileConfig
    _DefaultName = "processFile"

    def makeIdFactory(self, sensorRef):
        expBits = sensorRef.get("ccdExposureId_bits")
        expId = long(sensorRef.get("ccdExposureId"))
        return afwTable.IdFactory.makeSource(expId, 64 - expBits)

    @classmethod
    def _makeArgumentParser(cls):
        """Create an argument parser
        """
        parser = ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument("--id", "raw", "data ID, e.g. visit=1 raft=2,2 sensor=1,1 snap=0")
        return parser

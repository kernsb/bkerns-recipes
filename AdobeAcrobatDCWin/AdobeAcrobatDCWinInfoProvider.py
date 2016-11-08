#!/usr/bin/python
#
# Copyright 2014: wycomco GmbH (choules@wycomco.de)
#           2015: modifications by Tim Sutton
#			2015: modifications by Sam Novak
#			2016: modifications by Brandon Kerns
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for AdobeReaderURLProvider class"""
# Disabling warnings for env members and imports that only affect recipe-
# specific processors.
# pylint: disable=e1101

import urllib2

from autopkglib import Processor, ProcessorError
from ftplib import FTP

__all__ = ["AdobeAcrobatDCWinInfoProvider"]

MAJOR_VERSION_DEFAULT = "AcrobatDC"

AR_UPDATER_DOWNLOAD_URL = (
    "http://download.adobe.com/"
    "pub/adobe/acrobat/win/%s/%s/%sUpd%s.msp")


class AdobeAcrobatDCWinInfoProvider(Processor):
    """Provides URL to the latest Adobe Acrobat Pro update."""
    description = __doc__
    input_variables = {
        "major_version": {
            "required": False,
            "description": ("Major version. Examples: 'AcrobatDC', 'Acrobat2015'. Defaults to "
                            "%s" % MAJOR_VERSION_DEFAULT)
        }
    }
    output_variables = {
        "url": {
            "description": "URL to the latest Adobe Acrobat Pro update.",
        },
        "version": {
            "description": "Version for this update.",
        },
        "vercode": {
            "description": "Version code for this update. (unformatted)",
        },
        "file_fldr_vers": {
            "description": "File style version.",
        },
    }

    def get_reader_updater_msp_url(self, major_version):
        '''Returns download URL for Adobe Acrobat Pro updater MSP'''
        
        ftp = FTP('ftp.adobe.com')
        ftp.login()
        ftp.cwd('/pub/adobe/acrobat/win/AcrobatDC')
        items = ftp.nlst()
        citems = [ x for x in items if x.isdigit() ]
        versioncode = max(citems)
        version_string = versioncode[:2] + "." + versioncode[3:5].zfill(3) + "." + versioncode[-5:].zfill(5)
        file_ver = versioncode[:2] + "." + versioncode[3:5].lstrip("0") + "." + versioncode[-5:].zfill(5) + ".000000"
        
        url = AR_UPDATER_DOWNLOAD_URL % (major_version, versioncode, major_version, versioncode)
        
        return (url, version_string, versioncode, file_fldr_vers)

    def main(self):
        major_version = self.env.get("major_version", MAJOR_VERSION_DEFAULT)

        (url, version, vercode) = self.get_reader_updater_msp_url(major_version)

        self.env["url"] = url
        self.env["version"] = version
        self.env["vercode"] = vercode
        self.env["file_fldr_vers"] = file_fldr_vers

        self.output("Found URL %s" % self.env["url"])


if __name__ == "__main__":
    PROCESSOR = AdobeAcrobatDCWinInfoProvider()
    PROCESSOR.execute_shell()

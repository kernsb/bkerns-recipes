#!/usr/bin/python

import CoreFoundation
from CoreFoundation import *

from autopkglib import Processor, ProcessorError


__all__ = ["IntVerProcessor"]

class IntVerProcessor(Processor):
    """Shared processor to return a comparable integer representation of a version/subversion/build number."""
    description = __doc__
    input_variables = {
        "target": {
            "required": False,
            "description": ("Location of application or plug-in"
                            "that will be evaluated."),
        },
        "version": {
            "required": False,
            "description": ("If the proper version has already been detected,"
                            "supply it directly with version. Defaults to nothing.")
        },
        "verkey": {
            "required": False,
            "description": ("Info.plist key name to use as the source version."
                            "Defaults to CFBundleShortVersionString.")
        },
        "bldkey": {
            "required": False,
            "description": ("Info.plist key name to use if there is a build version"
                            "to be considered. Defaults to nothing.")
        },
        "minplace": {
            "required": False,
            "description": ("Minimum number of places per version field."
                            "Defaults to 3.")
        },
    }
    output_variables = {
        "intver": {
            "description": "An integer representation of the input version string.",
        },
    }

    def makeIntVer( self, ver, bld, min ):
        ver = ver.replace(' ', '.')
        ver = ver.replace('-', '.')
        ver = ver.split('.')
        if bld:
            ver.append(bld)
        fields = len(ver)
        while fields < 3:
            ver += "0"
            fields = len(ver)
        for i, field in enumerate(ver):
            output = ""
            for character in field:
                if character.isdigit():
                    output += str(character)
                else:
                    number = ord(character.lower()) - 97
                    output += str(number).zfill(2)
            ver[i] = output
        maxl = max(len(s) for s in ver)
        if maxl < min:
            maxl = min
        for i, field in enumerate(ver[1:]):
            ver[i+1] = field.zfill(maxl)
        ver = "".join(ver)
        return ver

    def main(self):
    	target = self.env.get("target")
        if "verkey" in self.env:
        	verkey = self.env.get("verkey")
        else:
            verkey = "CFBundleShortVersionString"
        if "bldkey" in self.env:
        	bldkey = self.env.get("bldkey")
        else:
            bldkey = ""
        if "minplace" in self.env:
        	minplace = self.env.get("minplace")
        else:
            minplace = 3
        if "version" in self.env:
        	version = self.env.get("version")
        else:
            version = CoreFoundation.CFPreferencesCopyValue(verkey, "%s/Contents/Info" % (target), kCFPreferencesAnyUser, kCFPreferencesCurrentHost)
        if bldkey:
            build = CoreFoundation.CFPreferencesCopyValue(bldkey, "%s/Contents/Info" % (target), kCFPreferencesAnyUser, kCFPreferencesCurrentHost)
        else:
            build = ""
        self.env["intver"] = self.makeIntVer( version, build, minplace )


if __name__ == '__main__':
    PROCESSOR = IntVerProcessor()
    PROCESSOR.execute_shell()

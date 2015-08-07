#!/usr/bin/python

import sys
import os
import subprocess
import CoreFoundation
from CoreFoundation import *

googleSoftwareUpdate = "/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle"
chromeBundleID = "com.google.Chrome"

ksadmin = os.path.join(googleSoftwareUpdate, "Contents/MacOS/ksadmin")
if os.path.exists(ksadmin):
    ksadminProcess = [  ksadmin, '--delete', '--productid',  chromeBundleID]
    subprocess.call(ksadminProcess)

agentinstaller = os.path.join(googleSoftwareUpdate, "/Contents/Resources/GoogleSoftwareUpdateAgent.app/Contents/Resources/install.py")
if os.path.exists(agentinstaller):
    agentinstallerProcess = [  agentinstaller, '--uninstall']
    subprocess.call(agentinstallerProcess)

CoreFoundation.CFPreferencesSetValue("checkInterval", 0, "Library/Preferences/com.google.Keystone.Agent", kCFPreferencesAnyUser, kCFPreferencesCurrentHost)
CoreFoundation.CFPreferencesSynchronize("Library/Preferences/com.google.Keystone.Agent", kCFPreferencesAnyUser, kCFPreferencesCurrentHost)

base_dir = os.listdir('/System/Library/User Template')
template_dirs = [item for item in base_dir]
users_dir = os.listdir('/Users')
home_dirs = [item for item in users_dir if not item.startswith('.') and item != 'Shared']

for folder in template_dirs:
    CoreFoundation.CFPreferencesSetValue("checkInterval", 0, "/System/Library/User Template/%s/Library/Preferences/com.google.Keystone.Agent" % (folder), kCFPreferencesAnyUser, kCFPreferencesCurrentHost)
    CoreFoundation.CFPreferencesSynchronize("/System/Library/User Template/%s/Library/Preferences/com.google.Keystone.Agent" % (folder), kCFPreferencesAnyUser, kCFPreferencesCurrentHost)

for folder in home_dirs:
    CoreFoundation.CFPreferencesSetValue("checkInterval", 0, "/Users/%s/Library/Preferences/com.google.Keystone.Agent" % (folder), kCFPreferencesAnyUser, kCFPreferencesCurrentHost)
    CoreFoundation.CFPreferencesSynchronize("/Users/%s/Library/Preferences/com.google.Keystone.Agent" % (folder), kCFPreferencesAnyUser, kCFPreferencesCurrentHost)

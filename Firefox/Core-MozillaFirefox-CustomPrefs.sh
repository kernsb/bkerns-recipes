#!/bin/sh

localprefs="/Applications/Firefox.app/Contents/Resources/defaults/pref/local-settings.js"
custprefs="/Applications/Firefox.app/Contents/Resources/mozilla.cfg"

if [ ! -f "${localprefs}" ]; then
    touch "${localprefs}"
    echo "// Purdue IT additions" >> "${localprefs}"
    echo "pref(\"general.config.filename\", \"mozilla.cfg\");" >> "${localprefs}"
    echo "pref(\"general.config.obscure_value\", 0);" >> "${localprefs}"
fi

if [ ! -f "${custprefs}" ]; then
    touch "${custprefs}"
    echo "lockPref(\"app.update.auto\", false);" >> "${custprefs}"
    echo "lockPref(\"app.update.enabled\", false);" >> "${custprefs}"
    echo "lockPref(\"extensions.update.enabled\", false);" >> "${custprefs}"
    echo "lockPref(\"extensions.update.autoUpdateDefault\", false);" >> "${custprefs}"
    echo "lockPref(\"browser.search.update\", false);" >> "${custprefs}"
    echo "pref(\"browser.shell.checkDefaultBrowser\", false);" >> "${custprefs}"
fi

exit 0
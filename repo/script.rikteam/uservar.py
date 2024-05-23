import xbmcaddon

import os

#########################################################
#         Global Variables - DON'T EDIT!!!              #
#########################################################
ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'media')
#########################################################

#########################################################
#        User Edit Variables                            #
#########################################################
ADDONTITLE = '[COLOR goldenrod]Script RikTeam[/COLOR]'
BUILDERNAME = 'RikTeam'
EXCLUDES = [ADDON_ID, 'repository.rebase']
# Text File with build info in it.
BUILDFILE = 'https://raw.githubusercontent.com/fontsvr/repo-fontsVR/main/wizardfiles/ajustes.txt'
# How often you would like it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK = 0
# Text File with apk info in it.  Leave as 'http://' to ignore
APKFILE = ''
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE = 'Youtube Video'
YOUTUBEFILE = 'http://'
# Text File for addon installer.  Leave as 'http://' to ignore
# https://raw.githubusercontent.com/fontsvr/fontsvr.github.io/main/wizard/xml/skins.json
ADDONFILE = 'https://raw.githubusercontent.com/fontsvr/fontsvr.github.io/main/wizard/xml/skins.json'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE = 'http://'
#########################################################

#########################################################
#        Theming Menu Items                             #
#########################################################
# If you want to use locally stogold icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'https://www.yourhost.com/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS = os.path.join(ART, 'wizard.png')
ICONMAINT = os.path.join(ART, 'maintenance.png')
ICONSPEED = os.path.join(ART, 'clean.png')
ICONAPK = os.path.join(ART, 'skins.png')
ICONTOOLS = os.path.join(ART, 'tools.png')
ICONADDONS = os.path.join(ART, 'addoninstaller.png')
ICONYOUTUBE = os.path.join(ART, 'youtube.png')
ICONSAVE = os.path.join(ART, 'savedata.png')
ICONTRAKT = os.path.join(ART, 'keeptrakt.png')
ICONREAL = os.path.join(ART, 'alfa.png')
ICONLOGIN = os.path.join(ART, 'backup.png')
ICONCONTACT = os.path.join(ART, 'information.png')
ICONACE = os.path.join(ART, 'acestream.png')
ICONURL = os.path.join(ART, 'url.png')
ICONAPI = os.path.join(ART, 'api.png')
ICONBUFFER = os.path.join(ART, 'buffer.png')
ICONHDFULL = os.path.join(ART, 'hdfull.png')
ICONSETTINGS = os.path.join(ART, 'settings.png')
# Hide the section separators 'Yes' or 'No'
HIDESPACERS = 'No'
# Character used in separator
SPACER = ''

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1 = 'goldenrod'
COLOR2 = 'white'
# Primary menu items   / {0} is the menu item and is required
THEME1 = u'[COLOR {color1}][COLOR {color2}]{{}}[/COLOR]'.format(color1=COLOR1, color2=COLOR2)
# Build Names          / {0} is the menu item and is required
THEME2 = u'[COLOR {color1}]{{}}[/COLOR]'.format(color1=COLOR1)
# Alternate items      / {0} is the menu item and is required
THEME3 = u'[COLOR {color1}]{{}}[/COLOR]'.format(color1=COLOR1)
# Current Build Header / {0} is the menu item and is required
THEME4 = u'[COLOR {color1}]Ajuste Instalado: [/COLOR] [COLOR {color2}]{{}}[/COLOR]'.format(color1=COLOR1, color2=COLOR2)
# Current Theme Header / {0} is the menu item and is required
THEME5 = u'[COLOR {color1}]Tema actual: [/COLOR] [COLOR {color2}]{{}}[/COLOR]'.format(color1=COLOR1, color2=COLOR2)

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT = 'Yes'
# You can add \n to do line breaks
CONTACT = ''
# Images used for the contact window.  http:// for default icon and fanart
CONTACTICON = 'http://'
CONTACTFANART = 'http://_'
#########################################################

#########################################################
#        Auto Update For Those With No Repo             #
#########################################################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE = 'No'
#########################################################

#########################################################
#        Auto Install Repo If Not Installed             #
#########################################################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL = 'No'
# Addon ID for the repository
REPOID = 'repository.fontsvr'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML = 'https://raw.githubusercontent.com/fontsvr/repo-fontsVR/main/addons/zips/addons.xml'
# Url to folder zip is located in
REPOZIPURL = 'https://raw.githubusercontent.com/fontsvr/repo-fontsVR/main/addons/zips/'
#########################################################

#########################################################
#        Notification Window                            #
#########################################################
# Enable Notification screen Yes or No
ENABLE = 'No'
# Url to notification file
NOTIFICATION = 'https://raw.githubusercontent.com/fontsvr/repo-fontsVR/main/wizardfiles/RV/Notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE = 'Text'
# Font size of header
FONTHEADER = 'Font14'
HEADERMESSAGE = '[COLOR white][B]Script[/B][/COLOR] [COLOR orange]RikTeam[/COLOR]'
# url to image if using Image 424x180
HEADERIMAGE = 'https://res.cloudinary.com/dsmvomgrd/image/upload/v1683640913/build/banner.png'
# Font for Notification Window
FONTSETTINGS = 'Font13'
# Background for Notification Window
BACKGROUND = 'https://res.cloudinary.com/dsmvomgrd/image/upload/v1683640927/build/fandrart.png'
#########################################################



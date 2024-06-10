################################################################################
#      Copyright (C) 2019 drinfernoo                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc
import xbmcgui

import os
import time

from xml.etree import ElementTree

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools

ORDER = ['fenad', 'fenpm', 'fenrd',
         'gaiaad', 'gaiard', 'gaiapm',
         'pmzer',
         'serenad', 'serenpm', 'serenpm-oauth', 'serenrd', 
         'shadowad', 'shadowpm', 'shadowrd',
         'rurlad', 'rurlpm', 'rurlrd',
         'urlad', 'urlpm', 'urlrd',]

alfaID = {
    'gaiaad': {
        'name': 'Gaia AD',
        'plugin': 'plugin.video.gaia',
        'saved': 'gaiaad',
        'path': os.path.join(CONFIG.ADDONS, 'plugin.video.gaia'),
        'icon': os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart': os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file': os.path.join(CONFIG.alfaFOLD, 'gaia_allalfa'),
        'settings': os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'settings.xml'),
        'default': 'accounts.alfa.allalfa.user',
        'data': ['accounts.alfa.allalfa.enabled',
                 'accounts.alfa.allalfa.user', 'accounts.alfa.allalfa.pass'],
        'activate': 'RunPlugin(plugin://plugin.video.gaia/?action=allalfaSettings)'},
    'gaiard': {
        'name'     : 'Gaia RD',
        'plugin'   : 'plugin.video.gaia',
        'saved'    : 'gaiard',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'gaia_alfa'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'settings.xml'),
        'default'  : 'accounts.alfa.realalfa.id',
        'data'     : ['accounts.alfa.realalfa.auth', 'accounts.alfa.realalfa.enabled', 'accounts.alfa.realalfa.id', 'accounts.alfa.realalfa.refresh', 'accounts.alfa.realalfa.secret', 'accounts.alfa.realalfa.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=realalfaAuthentication)'},
    'gaiapm': {
        'name'     : 'Gaia PM',
        'plugin'   : 'plugin.video.gaia',
        'saved'    : 'gaiapm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'gaia_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'settings.xml'),
        'default'  : 'accounts.alfa.premiumize.auth',
        'data'     : [ 'accounts.alfa.premiumize.enabled', 'accounts.alfa.premiumize.token', 'accounts.alfa.premiumize.auth'],
        'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=premiumizeSettings)'},
    'serenad': {
        'name'     : 'Seren AD',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'seren_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'allalfa.username',
        'data'     : ['allalfa.enabled', 'allalfa.username', 'allalfa.token'],
        'activate' : 'RunPlugin(plugin.video.seren/?action=openSettings)'},
    'serenrd': {
        'name'     : 'Seren RD',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'seren_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'rd.username',
        'data'     : [ 'rd.auth', 'rd.client_id', 'rd.expiry', 'rd.refresh', 'rd.secret', 'rd.username', 'realalfa.enabled'],
        'activate' : 'RunPlugin(plugin://plugin.video.seren/?action=authRealalfa)'},
    'serenpm': {
        'name'     : 'Seren PM (API Key)',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'seren_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'premiumize.pin',
        'data'     : ['premiumize.enabled', 'premiumize.pin'],
        'activate' : 'RunPlugin(plugin.video.seren/?action=openSettings)'},
    'serenpm-oauth': {
        'name'     : 'Seren PM (OAuth)',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenpm-oauth',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'seren_pmoauth'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.enabled', 'premiumize.username', 'premiumize.token'],
        'activate' : 'RunPlugin(plugin.video.seren/?action=openSettings)'},
    'urlrd': {
        'name'     : 'URLResolver RD',
        'plugin'   : 'script.module.urlresolver',
        'saved'    : 'urlrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'url_alfa'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.urlresolver', 'settings.xml'),
        'default'  : 'RealalfaResolver_client_id',
        'data'     : ['RealalfaResolver_autopick', 'RealalfaResolver_client_id', 'RealalfaResolver_client_secret', 'RealalfaResolver_enabled', 'RealalfaResolver_login', 'RealalfaResolver_priority', 'RealalfaResolver_refresh', 'RealalfaResolver_token', 'RealalfaResolver_torrents'],
        'activate' : 'RunPlugin(plugin://script.module.urlresolver/?mode=auth_rd)'},
    'urlad': {
        'name': 'URLResolver AD',
        'plugin': 'script.module.urlresolver',
        'saved': 'urlad',
        'path': os.path.join(CONFIG.ADDONS, 'script.module.urlresolver'),
        'icon': os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'icon.png'),
        'fanart': os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'fanart.jpg'),
        'file': os.path.join(CONFIG.alfaFOLD, 'url_allalfa'),
        'settings': os.path.join(CONFIG.ADDON_DATA, 'script.module.urlresolver', 'settings.xml'),
        'default': 'AllalfaResolver_client_id',
        'data': ['AllalfaResolver_enabled', 'AllalfaResolver_login', 'AllalfaResolver_priority',
                 'AllalfaResolver_token', 'AllalfaResolver_torrents', 'AllalfaResolver_cached_only'],
        'activate': 'RunPlugin(plugin://script.module.urlresolver/?mode=auth_ad)'},
    'rurlrd': {
        'name'     : 'ResolveURL RD',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'resurl_alfa'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'RealalfaResolver_client_id',
        'data'     : ['RealalfaResolver_autopick', 'RealalfaResolver_client_id', 'RealalfaResolver_client_secret', 'RealalfaResolver_enabled', 'RealalfaResolver_login', 'RealalfaResolver_priority', 'RealalfaResolver_refresh', 'RealalfaResolver_token', 'RealalfaResolver_torrents', 'RealalfaResolver_cached_only'],
        'activate' : 'RunPlugin(plugin://script.module.resolveurl/?mode=auth_rd)'},
    'rurlad': {
        'name': 'ResolveURL AD',
        'plugin': 'script.module.resolveurl',
        'saved': 'rurlad',
        'path': os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon': os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart': os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file': os.path.join(CONFIG.alfaFOLD, 'resurl_allalfa'),
        'settings': os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default': 'AllalfaResolver_client_id',
        'data': ['AllalfaResolver_enabled', 'AllalfaResolver_login', 'AllalfaResolver_priority',
                 'AllalfaResolver_token', 'AllalfaResolver_torrents', 'AllalfaResolver_cached_only'],
        'activate': 'RunPlugin(plugin://script.module.resolveurl/?mode=auth_ad)'},
    'urlpm': {
        'name'     : 'URLResolver PM',
        'plugin'   : 'script.module.urlresolver',
        'saved'    : 'urlpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'pmurl_alfa'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.urlresolver', 'settings.xml'),
        'default'  : 'PremiumizeMeResolver_password',
        'data'     : ['PremiumizeMeResolver_enabled', 'PremiumizeMeResolver_login', 'PremiumizeMeResolver_password', 'PremiumizeMeResolver_priority', 'PremiumizeMeResolver_torrents'],
        'activate' : ''},
    'rurlpm': {
        'name'     : 'ResolveURL PM',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'pmrurl_alfa'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'PremiumizeMeResolver_token',
        'data'     : ['PremiumizeMeResolver_enabled', 'PremiumizeMeResolver_priority', 'PremiumizeMeResolver_token', 'PremiumizeMeResolver_torrents', 'PremiumizeMeResolver_cached_only'],
        'activate' : ''},
    'pmzer': {
        'name'     : 'Premiumizer',
        'plugin'   : 'plugin.video.premiumizer',
        'saved'    : 'pmzer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'premiumizer_alfa'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizer', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.status', 'premiumize.token', 'premiumize.refresh'],
        'activate' : 'RunPlugin(plugin://plugin.video.premiumizer/?action=authPremiumize)'},
    'fenrd': {
        'name'     : 'Fen RD',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'fanart.png'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'fen_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'rd.username',
        'data'     : ['rd.username', 'rd.token', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret'],
        'activate' : 'RunPlugin(plugin://plugin.video.fen/?mode=real_alfa.authenticate)'},
    'fenpm': {
        'name'     : 'Fen PM',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'fanart.png'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'fen_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.account_id', 'pm.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.fen/?mode=premiumize.authenticate)'},
    'fenad': {
        'name'     : 'Fen AD',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'fanart.png'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'fen_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'ad.account_id',
        'data'     : ['ad.account_id', 'ad.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.fen/?mode=allalfa.authenticate)'},
    'shadowrd': {
        'name'     : 'Shadow RD',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'shadow_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'rd.auth',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret'],
        'activate' : 'RunPlugin(plugin://plugin.video.shadow?mode=138&url=www)'},
    'shadowpm': {
        'name'     : 'Shadow PM',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'shadow_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.shadow?mode=140&url=www)'},
    'shadowad': {
        'name'     : 'Shadow AD',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.alfaFOLD, 'shadow_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'allalfa.username',
        'data'     : ['allalfa.username', 'allalfa.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.shadow?mode=142&url=www)'}
# need to save rdauth.json :(
#	'realizer': {
#		'name'     : 'Realizer',
#		'plugin'   : 'plugin.video.realizer',
#		'saved'    : 'realizer',
#		'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer'),
#		'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'icon.png'),
#		'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
#		'file'     : os.path.join(CONFIG.alfaFOLD, 'realizer_alfa'),
#		'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.realizer', 'settings.xml'),
#		'default'  : 'premiumize.token',
#		'data'     : ['premiumize.status', 'premiumize.token', 'premiumize.refresh'],
#		'activate' : 'RunPlugin(plugin://plugin.video.realizer/?action=authRealalfa)'}
}


def alfa_user(who):
    user = None
    if alfaID[who]:
        if os.path.exists(alfaID[who]['path']):
            try:
                add = tools.get_addon_by_id(alfaID[who]['plugin'])
                user = add.getSetting(alfaID[who]['default'])
            except:
                pass
    return user


def alfa_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.alfaFOLD):
        os.makedirs(CONFIG.alfaFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(alfaID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(alfaID[log]['plugin'])
                    default = alfaID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_alfa(do, log)
                except:
                    pass
            else:
                logging.log('[alfa Info] {0}({1}) is not installed'.format(alfaID[log]['name'], alfaID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('alfanextsave', tools.get_date(days=3, formatted=True))
    else:
        if alfaID[who]:
            if os.path.exists(alfaID[who]['path']):
                update_alfa(do, who)
        else:
            logging.log('[alfa Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)


def clear_saved(who, over=False):
    if who == 'all':
        for alfa in alfaID:
            clear_saved(alfa,  True)
    elif alfaID[who]:
        file = alfaID[who]['file']
        if os.path.exists(file):
            os.remove(file)
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, alfaID[who]['name']),
                               '[COLOR {0}]alfa Info: Removed![/COLOR]'.format(CONFIG.COLOR2),
                               2000,
                               alfaID[who]['icon'])
        CONFIG.set_setting(alfaID[who]['saved'], '')
    if not over:
        xbmc.executebuiltin('Container.Refresh()')


def update_alfa(do, who):
    file = alfaID[who]['file']
    settings = alfaID[who]['settings']
    data = alfaID[who]['data']
    addonid = tools.get_addon_by_id(alfaID[who]['plugin'])
    saved = alfaID[who]['saved']
    default = alfaID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = alfaID[who]['name']
    icon = alfaID[who]['icon']

    if do == 'update':
        if not user == '':
            try:
                root = ElementTree.Element(saved)
                
                for setting in data:
                    alfa = ElementTree.SubElement(root, 'alfa')
                    id = ElementTree.SubElement(alfa, 'id')
                    id.text = setting
                    value = ElementTree.SubElement(alfa, 'value')
                    value.text = addonid.getSetting(setting)
                  
                tree = ElementTree.ElementTree(root)
                tree.write(file)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                
                logging.log('alfa Info Saved for {0}'.format(name), level=xbmc.LOGNOTICE)
            except Exception as e:
                logging.log("[alfa Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('alfa Info Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('alfa'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('alfa Info Restored for {0}'.format(name), level=xbmc.LOGNOTICE)
            except Exception as e:
                logging.log("[alfa Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('alfa Info Not Found for {0}'.format(name))
    elif do == 'clearaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings))
        if os.path.exists(settings):
            try:
                tree = ElementTree.parse(settings)
                root = tree.getroot()
                
                for setting in root.findall('setting'):
                    if setting.attrib['id'] in data:
                        logging.log('Removing Setting: {0}'.format(setting.attrib))
                        root.remove(setting)
                            
                tree.write(settings)
                
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Addon Data: Cleared![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[alfa Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
    xbmc.executebuiltin('Container.Refresh()')


def auto_update(who):
    if who == 'all':
        for log in alfaID:
            if os.path.exists(alfaID[log]['path']):
                auto_update(log)
    elif alfaID[who]:
        if os.path.exists(alfaID[who]['path']):
            u = alfa_user(who)
            su = CONFIG.get_setting(alfaID[who]['saved'])
            n = alfaID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                alfa_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]alfa Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springreen]Save alfa[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No, Cancel[/COLOR][/B]"):
                    alfa_it('update', who)
            else:
                alfa_it('update', who)


def import_list(who):
    if who == 'all':
        for log in alfaID:
            if os.path.exists(alfaID[log]['file']):
                import_list(log)
    elif alfaID[who]:
        if os.path.exists(alfaID[who]['file']):
            file = alfaID[who]['file']
            addonid = tools.get_addon_by_id(alfaID[who]['plugin'])
            saved = alfaID[who]['saved']
            default = alfaID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = alfaID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('alfa'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]alfa Info: Imported![/COLOR]'.format(CONFIG.COLOR2))


def activate_alfa(who):
    if alfaID[who]:
        if os.path.exists(alfaID[who]['path']):
            act = alfaID[who]['activate']
            addonid = tools.get_addon_by_id(alfaID[who]['plugin'])
            if act == '':
                addonid.openSettings()
            else:
                xbmc.executebuiltin(alfaID[who]['activate'])
        else:
            dialog = xbmcgui.Dialog()

            dialog.ok(CONFIG.ADDONTITLE,
                          '{0} is not currently installed.'.format(alfaID[who]['name']))
    else:
        xbmc.executebuiltin('Container.Refresh()')
        return

    check = 0
    while not alfa_user(who):
        if check == 30:
            break
        check += 1
        time.sleep(10)
    xbmc.executebuiltin('Container.Refresh()')


#########################################################
#         TRADUCIDO POR CHIKIRY                         #
#    WIZARD DE DIGGZ, AL CUAL DAMOS LAS GRACIAS         #
#########################################################
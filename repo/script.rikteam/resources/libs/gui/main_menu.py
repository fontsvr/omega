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

import os

from resources.libs.common import directory
from resources.libs.common.config import CONFIG


class MainMenu:

    def get_listing(self):
        from resources.libs import check
        from resources.libs.common import logging
        from resources.libs.common import tools

        errors = int(logging.error_checking(count=True))
        errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'

        if CONFIG.AUTOUPDATE == 'Yes':
            response = tools.open_url(CONFIG.BUILDFILE, check=True)

            if response:
                ver = check.check_wizard('version')
                if ver:
                    if ver > CONFIG.ADDON_VERSION:
                        directory.add_file(
                            '{0} [v{1}] [COLOR green][B][ACTUALIZACION v{2}][/B][/COLOR]'.format(CONFIG.ADDONTITLE,
                                                                                        CONFIG.ADDON_VERSION, ver),
                            {'mode': 'wizardupdate'}, themeit=CONFIG.THEME2)
                    else:
                        directory.add_file('{0}'.format(CONFIG.ADDONTITLE),
                                           themeit=CONFIG.THEME2)
            else:
                directory.add_file('{0}'.format(CONFIG.ADDONTITLE),
                                   themeit=CONFIG.THEME2)
        if len(CONFIG.BUILDNAME) > 0:
            version = check.check_build(CONFIG.BUILDNAME, 'version')
            build = 'Ajuste Actual: {0}'.format(CONFIG.BUILDNAME)
            if version > CONFIG.BUILDVERSION:
                build = 'Ajustes [COLOR yellow]- Nueva versión disponible[/COLOR]'.format(build)
            directory.add_dir(build, {'mode': 'builds', 'name': CONFIG.BUILDNAME}, themeit=CONFIG.THEME1)

        else:
            directory.add_dir('Ajustes', {'mode': 'builds'}, icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME1)
        directory.add_dir('Skins', {'mode': 'addons'}, icon=CONFIG.ICONAPK, themeit=CONFIG.THEME1)
        directory.add_file('Limpiar Aplicación', {'mode': 'fullclean'}, icon=CONFIG.ICONSPEED, themeit=CONFIG.THEME1)
        directory.add_dir('Copias de Seguridad', {'mode': 'maint', 'name': 'copias'}, icon=CONFIG.ICONLOGIN, themeit=CONFIG.THEME1)
        directory.add_dir('Herramientas', {'mode': 'maint'}, icon=CONFIG.ICONTOOLS, themeit=CONFIG.THEME1)
        directory.add_dir('Ajustes del Addon', {'mode': 'settings', 'name': CONFIG.ADDON_ID}, icon=CONFIG.ICONSETTINGS, themeit=CONFIG.THEME1)
        directory.add_file('Telegram: [COLOR blue]@fontsvr[/COLOR]', {'mode': 'saveda'}, icon=CONFIG.ICONCONTACT, themeit=CONFIG.THEME1)

        

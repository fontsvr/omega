# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mitelechopo - XBMC Add-on by Torete
# Version 0.2.5 (15.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
import os
import sys
import re
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import plugintools
import requests
import six
import xbmcvfs
addon = xbmcaddon.Addon()
addonname = '[B][COLOR white]RikTeam_[COLOR aqua]fonts[/COLOR][/B]'
icon = addon.getAddonInfo('icon')
myaddon = xbmcaddon.Addon("plugin.RikTeam_fonts")
Set_Color = myaddon.getSetting('SetColor')
Set_View = myaddon.getSetting('SetView')
     
def run():
 
    plugintools.set_view(plugintools.LIST)
 
    # Get params
    params = plugintools.get_params()
 
    if params.get("action") is None:
        ejecucion(params)
    else:
       action = params.get("action")
       url = params.get("url")
       exec(action+"(params)")
    plugintools.close_item_list()
#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------
#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------
#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------


#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------
#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------
#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------


   
#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------
#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------
#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------#---------MENU PRINCIPAL-----------------------MENU PRINCIPAL----------------------------MENU PRINCIPAL---------------------------------------

 

def main_list(params):
    
    url = params.get ( "url" )
    
    if url:
      plugintools.add_item(action = "" , title = "[B][COLOR aqua]---------------------"+addonname+"[B][COLOR aqua]--------------------------------------[/COLOR][/B]", thumbnail ="https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519183/build/fonts_ico.png", fanart = "https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519184/build/fonts_fanart.jpg",  folder = False )   
 
    
      plugintools.add_item(action = "" , title = "[B][COLOR white][LOWERCASE][CAPITALIZE]   A C T U A L I Z A D O R [COLOR yellow]  D E [COLOR aqua]  F U E N T E S[/CAPITALIZE][/LOWERCASE][/COLOR][/B]",  thumbnail ="https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519183/build/fonts_ico.png", fanart = "https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519184/build/fonts_fanart.jpg",  folder = False ) 

    
      plugintools.add_item(action = "ejecucion" , title = "[COLOR yellow]         << Iniciar el instalador de fuentes >>[/COLOR]", info_labels={"Title":addonname, "Plot":addonname+"\n\nIniciar el instalador de las fuentes más populares para dotar a tu mediacenter de los complementos necesarios para una máxima experiencia."}, thumbnail ="https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519183/build/fonts_icon.png", fanart = "https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519184/build/fonts_fanart.jpg",  folder = False )   
      
      
      plugintools.set_view(plugintools.EPISODES)
      
      
      plugintools.add_item(action = "" , title = "[B][COLOR aqua]---------------------"+addonname+"[B][COLOR aqua]--------------------------------------[/COLOR][/B]", thumbnail ="https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519183/build/fonts_ico.png", fanart = "https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519184/build/fonts_fanart.jpg",  folder = False )   
      
      plugintools.add_item(action = "plugintools.browse" , title = "Abrir archivos y explorar carpetas de Kodi (visor texto)", thumbnail ="https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519183/build/fonts_ico.png", fanart = "https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519184/build/fonts_fanart.jpg",  folder = False )   

      
      plugintools.add_item(action = "salir" , title = "[B]                                  S A L I R[/B]", thumbnail ="https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519183/build/fonts_ico.png", fanart = "https://res.cloudinary.com/dsmvomgrd/image/upload/v1684519184/build/fonts_fanart.jpg",  folder = False )   
      
    else:
      ejecucion()
    

def ejecucion(params):

    if six.PY2:
        translatePath = xbmc.translatePath
    elif six.PY3:
        translatePath = xbmcvfs.translatePath


    site = "https://pastebin.com/raw/kY3W2iRB"
    try:
        r = requests.get(site,timeout=3)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        #print ("OOps: Something Else",err)
        di='\n[COLOR red]Servidor caído[/COLOR]\n'+ str(err)
        xbmcgui.Dialog().notification("[COLOR yellow]info[/COLOR]", di, xbmcgui.NOTIFICATION_INFO, 15000, False)
        #xbmcgui.Dialog().textviewer("[COLOR yellow]info[/COLOR]", di)
        r = requests.get("https://raw.githubusercontent.com/fontsvr/repo-fontsVR/main/sources/sources.xml")
    except requests.exceptions.HTTPError as errh:
        di='\n[COLOR red]Http Error:[/COLOR]\n'+ str(errh)
        xbmcgui.Dialog().textviewer("[COLOR yellow]info[/COLOR]", di)
    except requests.exceptions.ConnectionError as errc:
        di='\n[COLOR red]Error Connecting:[/COLOR]\n'+ str(errc)
        xbmcgui.Dialog().textviewer("[COLOR yellow]info[/COLOR]", di)
    except requests.exceptions.Timeout as errt:
        di='\n[COLOR red]Timeout Error:[/COLOR]\n'+ str(errt)
        xbmcgui.Dialog().textviewer("[COLOR yellow]info[/COLOR]", di)
    

    t = r.text
    sources = xbmcvfs.translatePath('special://profile/sources.xml')    
    respuesta = xbmcgui.Dialog().yesno(addonname, "[COLOR yellow]\nPulsa Ok para borrar tus fuentes y añadir las pricipales fuentes actualizadas. [COLOR lightpink]Después deberás reiniciar Kodi para que coja los cambios.[/COLOR]", "[B][COLOR red] No [/COLOR][/B]","[B][COLOR green]OK[/COLOR][/B]")
   

    if respuesta:       
        if not os.path.isfile(sources):
            file = open(sources, 'w+')
            source_data = file.read()
            #file.truncate(0)
            file.seek(0)
            for linea in t:
                file.write(linea)
            file.seek(0)    
            file.close()
            xbmcgui.Dialog().notification(addonname, '[COLOR lightgreen]'+'COPIA DE FUENTES REALIZADA.'+'[/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)
            
        else:
            file = open(sources,'w+')
            file.seek(0)
            file.truncate(0)
            for linea in t:
                file.write(linea)
            file.seek(0)    
            file.close()
            xbmcgui.Dialog().notification(addonname, '[COLOR green]COPIA DE FUENTES REALIZADA EXITOSAMENTE.[/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)
            xbmc.sleep(1500)
            choice = 1
            choice = plugintools.dialog_yesno(addonname, ' Cerrar Kodi para aplicar cambios. ', '[COLOR greenyellow][B]¿ Quieres Cerrar ?[/B][/COLOR]')
            try:
               if choice == 1:
                  os._exit(1)
               elif choice == 0:
                  pass
               else:
                  xbmc.executebuiltin("Action(Close)")
            except:
                pass
    else:
        xbmcgui.Dialog().notification('Info', 'CANCELADA LA COPIA DE FUENTES.', xbmcgui.NOTIFICATION_ERROR, 4000) 
        params["url"]=addonname
        main_list(params)
        #exit(0)
def salir(params):
    xbmc.executebuiltin("Action(Close)") 
    
run()

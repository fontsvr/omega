import sys, os, xbmc,xbmcaddon,xbmcgui,base64,shutil,re,fileinput
import errno,json,os,hashlib,urllib,xbmcplugin,time

if sys.version_info[0] >= 3:
    import xbmcvfs

    translatePath = xbmcvfs.translatePath
else:
    translatePath = xbmc.translatePath

id = 'pvr.iptvsimple'
skin="skin.estuary"
activar = False



'''if activar: 
    #xbmc.executebuiltin('InstallAddon(%s)' % (id))'''
    
    

def show(string):
    #return base64.b64decode(b'%s'%string)
    return base64.b64decode(string)          
def hide(string):
    #return base64.b64encode(b'%s'%string)
    return base64.b64encode(string)   
def exe(string):
    xbmc.executebuiltin(string)

def updateaddons():
    exe('UpdateLocalAddons')

def reloadkeymaps():
    exe('Action(reloadkeymaps)')

def window(window):
    exe('ActivateWindow(%s)'%window)

def condition(string):
    return xbmc.getCondVisibility(string)

def pvr(toggle):
    
    id="pvr.iptvsimple"
    skin="skin.estuary"

    if toggle:
        if sys.argv[1]== "estuary":
          #xbmcgui.Dialog().notification('a skin', 'Estuary', xbmcgui.NOTIFICATION_INFO)
          #query1 = xbmc.executeJSONRPC('{{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","params":{{"addonid":"skin.estuary", "properties": ["enabled"]}},"id":1 }}' ) #% id)
          #query = '{{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{{"setting":"lookandfeel.skin","value":{0}}},"id":1}}'.format(skin)  #,"value":"<skin.name>"
          #if '"enabled":true' in query1:
          if choice("   Quieres canviar a [COLOR white]"+ str(skin) + "[/COLOR]?"):
              xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params": {"setting":"lookandfeel.skin","value":"skin.estuary"}, "id":1}') #ok  
        
        elif sys.argv[1]== "sonidos":
          if choice("   Apagar los sonidos de la interfaz de Kodi [COLOR white](resource.ui.sounds.kodi)[/COLOR]?"):
              xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params": {"setting":"lookandfeel.soundskin","value":""}, "id":1}')
              #xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.SetMute", "params": {"mute": "true"}, "id": 1}') #no
              xbmcgui.Dialog().notification('Sonidos Desactivados', '', xbmcgui.NOTIFICATION_INFO)
          else:
              xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params": {"setting":"lookandfeel.soundskin","value":"resource.ui.sounds.kodi"}, "id":1}')
              xbmcgui.Dialog().notification('Sonidos Activados', '', xbmcgui.NOTIFICATION_INFO)
        elif sys.argv[1]== "volumen50":
          if choice("   Quieres canviar volumen general a 50?"):
              xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Application.SetVolume","params": {"volume": 50}, "id":1}' )
          else:
              xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Application.SetVolume","params": {"volume": 100}, "id":1}' ) 
              
        elif sys.argv[1]== "pvrtoggle":
          if choice("   Quieres desactivar [COLOR white]"+ str(id) + "[/COLOR]?"):
            disableaddon(id)
        else:
          if choice("   Quieres activar [COLOR white]"+ str(id) + "[/COLOR]?"):
            enableaddon(id)
                    
def disableaddon(id,value='false'):
    query = '{{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{{"addonid":"{0}","enabled":{1}}}, "id":1}}'.format(id, value)
    xbmc.executeJSONRPC(query)
    xbmcgui.Dialog().notification('Desactivado', str(id), xbmcgui.NOTIFICATION_INFO)

def enableaddon(id,value='true'):
    query = '{{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{{"addonid":"{0}","enabled":{1}}}, "id":1}}'.format(id, value)
    xbmc.executeJSONRPC(query)
    xbmcgui.Dialog().notification('Activado', str(id), xbmcgui.NOTIFICATION_INFO)
    #xbmc.executebuiltin("ReloadSkin()")

def toogle_PVR(toggle):
    id="pvr.iptvsimple"
    if toggle:
      if sys.argv[1]== "desactivaraddon":
       if choice("   Quieres desactivar [COLOR $VAR[ThemeLabelColor]]"+ str(id) + "[/COLOR]?"):
         value='false'
         query = '{{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{{"addonid":"{0}","enabled":{1}}}, "id":1}}'.format(id, value)
         xbmc.executeJSONRPC(query)
         xbmcgui.Dialog().notification('Desactivado', str(id), xbmcgui.NOTIFICATION_INFO)
      elif sys.argv[1]== "activaraddon":
       if choice("   Quieres activar [COLOR $VAR[ThemeLabelColor]]"+ str(id) + "[/COLOR]?"): #$VAR[HighlightBarColor]
          value='true'
          query = '{{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{{"addonid":"{0}","enabled":{1}}}, "id":1}}'.format(id, value)
          xbmc.executeJSONRPC(query)
          xbmcgui.Dialog().notification('Activado', str(id), xbmcgui.NOTIFICATION_INFO)

def get_global_setting(setting):
    #Get a Kodi setting
    result = jsonrpc(method='Settings.GetSettingValue', params=dict(setting=setting))
    return result.get('result', {}).get('value')

def vol50(toggle):
    if toggle:
       if sys.argv[1]== "volumen50":
         if choice("   Quieres canviar volumen general a 50?"):
           xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Application.SetVolume","params": {"volume": 50}, "id":1}' )
       else:
           xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Application.SetVolume","params": {"volume": 95}, "id":1}' )

def vol(value): #toggle=True value='true'
    #jsonrpc(method='Application.SetMute', params=dict(mute=toggle))
    query = '{{"jsonrpc": "2.0", "method": "Application.SetMute", "params": {{ "mute": "{0}" }}, "id": 1}}'.format(value) #"mute": "toggle"
    xbmc.executeJSONRPC(query)

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create(addon('id'),"Downloading Content",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
    try: 
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0 and not percent == 100: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0
        kbps_speed = kbps_speed / 1024 
        type_speed = 'KB'
        if kbps_speed >= 1024:
            kbps_speed = kbps_speed / 1024 
            type_speed = 'MB'
        total = float(filesize) / (1024 * 1024) 
        mbs = '[COLOR red][B]Size:[/B] [COLOR green]%.02f[/COLOR] MB of [COLOR green]%.02f[/COLOR] MB[/COLOR]'%(currently_downloaded, total) 
        e   = '[COLOR red][B]Speed:[/B] [COLOR green]%.02f [/COLOR]%s/s ' % (kbps_speed, type_speed)
        e  += '[B]ETA:[/B] [COLOR green]%02d:%02d[/COLOR][/COLOR]' % divmod(eta, 60)
        dp.update(percent, '', mbs, e)
    except Exception as e: #, e:
        return str(e)
    if dp.iscanceled(): 
        dp.close()
        sys.exit()

def forceclose(name="This Function"):
    if choice('In Order To Enable %s, You Must Force Close'%(name),"Force Close","Later"): os._exit(1)

def read(file):
    return open(file, 'r').read()

def search(query,file):
    return re.findall(query,file)

def action(string):
    exe('Action(%s)'%(string))

def info(string):
    return xbmc.getInfoLabel(string)

def refreshContainer():
    exe('Container.Refresh')

def updateContainer():
    exe('Container.Update')

def startpvr():
    exe('StartPVRManager')

def controlMessage(control):
    exe('Control.Message(%s)')%(control)

def RunAddon(id):
    exe('RunAddon(%s)')%(id)

def RunPlugin(id):
    exe('RunPlugin(%s)')%(id)

'''def enableaddon(id,enable='true'):
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "%s", "enabled": "%s" }}'%(id,enable))
'''
def hasaddon(addon):
    try:
        if xbmcaddon.Addon(addon): return True
    except: return False

def copy(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def addon(item,id="skin.aeon.nox.silvo.fontsvr"):
    try:
        if item     == 'id'                : return xbmcaddon.Addon(id).getAddonInfo('id')
        elif item    == 'name'            : return xbmcaddon.Addon(id).getAddonInfo('name')
        elif item     == 'path'            : return xbmcaddon.Addon(id).getAddonInfo('path')
        elif item     == 'icon'            : return xbmcaddon.Addon(id).getAddonInfo('icon')
        elif item     == 'fanart'            : return xbmcaddon.Addon(id).getAddonInfo('fanart')
        elif item     == 'author'            : return xbmcaddon.Addon(id).getAddonInfo('author')
        elif item     == 'fanart'            : return xbmcaddon.Addon(id).getAddonInfo('fanart')
        elif item     == 'version'        : return xbmcaddon.Addon(id).getAddonInfo('version')
        elif item     == 'summary'        : return xbmcaddon.Addon(id).getAddonInfo('summary')
        elif item     == 'description'    : return xbmcaddon.Addon(id).getAddonInfo('description')
    except: return False

def data(string):
    return json.loads(string)

def openURL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', addon('id'))
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def notification(message,title=addon('name')):
    xbmcgui.Dialog().notification(title,message)

def ok(line1,line2=None,line3=None,title=addon('name')):
    xbmcgui.Dialog().ok(title, line1=line1,line2=line2,line3=line3)

def choice(string,y='SI',n='NO',title=addon('name')):
    return xbmcgui.Dialog().yesno(title,string,yeslabel=y,nolabel=n)

def input(heading=addon('name')):
    return xbmcgui.Dialog().input(heading, type=xbmcgui.INPUT_ALPHANUM)

def cut(string):
    exec(string)

def log(string):
    xbmc.log(string)

def setting(id,value=None,addon=addon('id')):
    if not value                     : return xbmcaddon.Addon(addon).getSetting(id)
    else                             : return xbmcaddon.Addon(addon).setSetting(id,value)

def insertline(file,search,add):
    includes = []
    for line in fileinput.FileInput(file,inplace=1):
        if search in line:
            line=line.replace(line,line+add)
        includes.append(line)
    with open(file, "a") as myfile:
        for line in includes:
            myfile.write(line)
    
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def addItemGUI(conrol,label1=None,label2=None,icon=None,thumb=None):
    self.self.window.getControl(control).addItem(xbmcgui.ListItem(label1, label2=url, iconImage=icon, thumbnailImage=thumb))

def addDir(display, mode=None,username=None,password=None,icon=addon(show('aWNvbg==')),description=addon(show('aWQ='))):
    u = sys.argv[0]
    if not mode == None:         u += show("P21vZGU9JXM=") % urllib.quote_plus(mode)
    ok=True
    liz=xbmcgui.ListItem(display, iconImage=show("RGVmYXVsdEZvbGRlci5wbmc="), thumbnailImage=icon)
    liz.setInfo( type="Video", infoLabels={ show("VGl0bGU="): display, show("UGxvdA=="): description} )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addItem(display, mode=None,username=None,password=None,icon=addon(show('aWNvbg==')),description=addon(show('aWQ='))):
    u = sys.argv[0]
    if not mode == None:        u += show("P21vZGU9JXM=") % urllib.quote_plus(mode)
    ok=True
    liz=xbmcgui.ListItem(display, iconImage=show("RGVmYXVsdEZvbGRlci5wbmc="), thumbnailImage=icon)
    liz.setInfo( type="Video", infoLabels={ show("VGl0bGU="): display, show("UGxvdA=="): description} )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
    return ok

def skinres():
    results = search(r'aspect="(.+?)" .+? folder="(.+?)"',read(xbmc.translatePath('special://skin/addon.xml')))
    for item in results:
        if info('Skin.AspectRatio') in item:
            for listitem in item:
                if not info('Skin.AspectRatio') in listitem:
                    xbmc.log(listitem)
                    return listitem

def get(path,file=None):
    if 'ystem'         in path:                         return xbmc.translatePath('special://xbmc/'+file)                                     if file else xbmc.translatePath('special://xbmc/')
    elif 'ome'         in path:                          return xbmc.translatePath('special://home/'+file)                                     if file else xbmc.translatePath('special://home/')
    elif 'ddons'     in path:                         return xbmc.translatePath('special://home/addons/'+file)                             if file else xbmc.translatePath('special://home/addons/')
    elif 'serdata'     in path:                         return xbmc.translatePath('special://userdata/'+file)                                 if file else xbmc.translatePath('special://userdata/')
    elif 'atabase'     in path:                         return xbmc.translatePath('special://userdata/Database/'+file)                         if file else xbmc.translatePath('special://userdata/Database/')
    elif 'eymaps'     in path:                         return xbmc.translatePath('special://userdata/keymaps/'+file)                         if file else xbmc.translatePath('special://userdata/keymaps/')
    elif 'ddon'     in path and 'ata' in path:         return xbmc.translatePath('special://userdata/addon_data/'+file)                     if file else xbmc.translatePath('special://userdata/addon_data')
    elif 'lugin.'     in path:                         return xbmc.translatePath('special://home/addons/'+path+"/"+file)                     if file else xbmc.translatePath('special://home/addons/%s/'%path)
    elif 'cript.'     in path:                         return xbmc.translatePath('special://home/addons/'+path+"/"+file)                     if file else xbmc.translatePath('special://home/addons/%s/'%path)
    elif 'kin'         in path and 'addon.xml' in file:return xbmc.translatePath('special://skin/%s'%(file))
    elif 'kin'         in path and 'debug' in file:     return xbmc.translatePath('special://skin/media/%s'%(file))
    elif 'kin'         in path:                        return xbmc.translatePath('special://skin/%s/%s'%(skinres(),file))                  if file else xbmc.translatePath('special://skin/') 

# --- Script Entry Point ---#  
if __name__ == '__main__':
     addonfolder = translatePath(os.path.join('special://home/addons', id))
     #if len(sys.argv[1]) > 0:
     #if xbmc.getCondVisibility('System.HasAddon(id)'):
     try: 
      if sys.argv[1] == "pvrtoggle":
        pvr(sys.argv[1])
      elif sys.argv[1] == "pvron":
        pvr(sys.argv[1]) 
      elif sys.argv[1] == "desactivaraddon":
        toogle_PVR(sys.argv[1]) 
      elif sys.argv[1] == "activaraddon":
        toogle_PVR(sys.argv[1])
      elif sys.argv[1] == "volumen50":
        pvr(sys.argv[1]) 
      elif sys.argv[1] == "estuary":
        pvr(sys.argv[1])
      elif sys.argv[1] == "sonidos":
        pvr(sys.argv[1])
     except:
        pass

            
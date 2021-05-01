#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------#
#  coded by Lululla  #
#   skin by MMark    #
#     01/05/2021     #
#--------------------#
#Info http://t.me/tivustream
# from __future__ import print_function
from . import _
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import *
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import *
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap
from enigma import *
from enigma import RT_HALIGN_LEFT, loadPNG, RT_HALIGN_RIGHT, RT_HALIGN_CENTER
from enigma import eTimer, eListboxPythonMultiContent, eListbox, eConsoleAppContainer, gFont
from enigma import getDesktop
from os import path, listdir, remove, mkdir, chmod
                            
from twisted.web.client import downloadPage, getPage
from xml.dom import Node, minidom
import base64
import gettext
import os
import re
import sys
import glob
import shutil
import ssl
           
import six
                 
from sys import version_info
from . import Lcn      
global isDreamOS
global pngx, pngl, pngs

currversion      = '1.5'
title_plug   = '..:: TiVuStream Settings V. %s ::..' % currversion
name_plug        = 'TiVuStream Settings'

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse
    from urllib.parse import urlencode, quote
    from urllib.request import urlretrieve
else:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urlparse import urlparse
    from urllib import urlencode, quote
    from urllib import urlretrieve


if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context= sslContext)
    else:
        return urlopen(url)

isDreamOS = False
try:
    from enigma import eMediaDatabase
    isDreamOS = True
except:
    isDreamOS = False
try:
    from enigma import eDVBDB
except ImportError:
    eDVBDB = None

try:
    import zipfile
except:
    pass

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

                                                                          


                      
                      
                      
def checkStr(txt):
    if PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(six.text_type())):
            txt = txt.encode('utf-8')
    return txt

def checkInternet():
    try:
        response = checkStr(urlopen("http://google.com", None, 5))
        response.close()
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True
def ReloadBouquet():
    print('\n----Reloading bouquets----')
    if eDVBDB:
        eDVBDB.getInstance().reloadBouquets()
        print('bouquets reloaded...')
    else:
        os.system('wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &')
        print('bouquets reloaded...')

def resettings():
    if set == 1:
        terrestrial_rest()
        os.system("wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &")

def deletetmp():
    os.system('rm -rf /tmp/unzipped;rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz')
    return

os.system('rm -fr /usr/lib/enigma2/python/Plugins/Extensions/tvSettings/temp/*')# clean /temp


# DESKHEIGHT   = getDesktop(0).size().height()
plugin_path  = os.path.dirname(sys.modules[__name__].__file__)
skin_path        = plugin_path
ico_path         = plugin_path + '/logo.png'
pngx             = plugin_path + '/res/pics/plugins.png'
pngl             = plugin_path + '/res/pics/plugin.png'
pngs             = plugin_path + '/res/pics/setting.png'
HD           = getDesktop(0).size()

if HD.width() > 1280:
    if isDreamOS:
        skin_path = plugin_path + '/res/skins/fhd/dreamOs/'
    else:
        skin_path = plugin_path + '/res/skins/fhd/'
else:
    if isDreamOS:
        skin_path = plugin_path + '/res/skins/hd/dreamOs/'
    else:
        skin_path = plugin_path + '/res/skins/hd/'


Panel_Dlist = [
 ('SETTINGS BI58'),
 ('SETTINGS CIEFP'),
 ('SETTINGS CYRUS'),                      
 ('SETTINGS COLOMBO'),
 ('SETTINGS MANUTEK'),
 ('SETTINGS MILENKA61'),
 ('SETTINGS MORPHEUS'),
 ('SETTINGS PREDRAG'),
 ('SETTINGS VHANNIBAL'),
 ('UPDATE SATELLITES.XML'),
 ('UPDATE TERRESTRIAL.XML')
 ]

class SetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 22))
        self.l.setFont(2, gFont('Regular', 24))
        self.l.setFont(3, gFont('Regular', 26))
        self.l.setFont(4, gFont('Regular', 28))
        self.l.setFont(5, gFont('Regular', 30))
        self.l.setFont(6, gFont('Regular', 32))
        self.l.setFont(7, gFont('Regular', 34))
        self.l.setFont(8, gFont('Regular', 36))
        self.l.setFont(9, gFont('Regular', 40))
        if HD.width() > 1280:
            self.l.setItemHeight(50)
        else:
            self.l.setItemHeight(50)
            
class OneSetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if HD.width() > 1280:
            self.l.setItemHeight(50)
            textfont = int(34)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(22)
            self.l.setFont(0, gFont('Regular', textfont))

def DListEntry(name, idx):
    res = [name]
    if HD.width() > 1280:

        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png =loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1900, 50), font=6, text =name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:

        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(60, 5), size=(1000, 50), font=1, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res

def OneSetListEntry(name):
    res = [name]
    if HD.width() > 1280:
        res.append(MultiContentEntryPixmapAlphaTest(pos =(10, 12), size =(34, 25), png =loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(60, 0), size =(1900, 50), font =0, text =name, color = 0xa6d1fe, flags =RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos =(10, 6), size =(34, 25), png =loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(60, 5), size =(1000, 50), font=0, text =name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res

def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(OneSetListEntry(name))
        icount = icount+1
        list.setList(plist)


class MainSetting(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('MainSetting')
        Screen.__init__(self, session)
                           
        self.setTitle(_(title_plug))
        self['text'] = SetList([])
        self.working = False
        self.selection = 'all'
        self['title'] = Label(_(title_plug))
        self['info'] = Label('')
        self['info'].setText(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self['key_yellow'] = Button(_('Lcn'))
        if isDreamOS:
                self['key_yellow'].hide()
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions', ], {'ok': self.okRun,
         'green': self.okRun,
         'back': self.closerm,
         'red': self.closerm,
         'yellow': self.Lcn,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def Lcn(self):
        self.mbox = self.session.open(MessageBox, _('Reorder Terrestrial channels with Lcn rules'), MessageBox.TYPE_INFO, timeout=5)
        lcnstart()

    def closerm(self):
        self.close()

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        for x in Panel_Dlist:
            list.append(DListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)
        self['info'].setText(_('Please select ...'))

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        if sel == _('UPDATE SATELLITES.XML'):
            self.okSATELLITE()
        elif sel == _('UPDATE TERRESTRIAL.XML'):
            self.okTERRESTRIAL()
        elif sel == ('SETTINGS CIEFP'):
            self.session.open(SettingCiefp3)
        elif sel == ('SETTINGS CYRUS'):
            self.session.open(CirusSetting)                                         
        elif sel == ('SETTINGS COLOMBO'):
            self.session.open(tvColombo)
        elif sel == ('SETTINGS BI58'):
            self.session.open(tvSettingBi58)
        elif sel == ('SETTINGS MANUTEK'):
            self.session.open(SettingManutek)
        elif sel == ('SETTINGS MILENKA61'):
            self.session.open(SettingMilenka6121)
        elif sel == ('SETTINGS MORPHEUS'):
            self.session.open(SettingMorpheus2)
        elif sel == ('SETTINGS PREDRAG'):
            self.session.open(SettingPredrag)
        elif sel == ('SETTINGS VHANNIBAL'):
            self.session.open(SettingVhan)

    def okSATELLITE(self):
        self.session.openWithCallback(self.okSatInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okSatInstall(self, result):
        if result:
            if checkInternet():
                try:
                    url_sat_oealliance              = 'http://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/satellites.xml'
                    link_sat = ssl_urlopen(url_sat_oealliance)
                    dirCopy = '/etc/tuxbox/satellites.xml'
                    # urlretrieve(url_sat_oealliance, dirCopy, context= ssl._create_unverified_context())
                    urlretrieve(link_sat, dirCopy)
                    self.mbox = self.session.open(MessageBox, _('Satellites.xml Updated!'), MessageBox.TYPE_INFO, timeout=5)
                    self['info'].setText(_('Installation done !!!'))
                except:
                    return
            else:
                session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

    def okTERRESTRIAL(self):
        self.session.openWithCallback(self.okTerrInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okTerrInstall(self, result):
        if result:
            if checkInternet():
                try:
                    url_sat_oealliance              = 'https://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/terrestrial.xml'
                    link_ter = ssl_urlopen(url_sat_oealliance)
                    dirCopy                         = '/etc/tuxbox/terrestrial.xml'
                    # urlretrieve(url_sat_oealliance, dirCopy, context= ssl._create_unverified_context())
                    urlretrieve(link_ter, dirCopy) # , context= ssl._create_unverified_context())
                    self.mbox = self.session.open(MessageBox, _('Terrestrial.xml Updated!'), MessageBox.TYPE_INFO, timeout=5)
                    self['info'].setText(_('Installation done !!!'))
                except:
                    return
            else:
                session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

class tvColombo(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Colombo')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL2NvbG9tYm8uYWx0ZXJ2aXN0YS5vcmcvY29sb21iby9jb2xvbWJvLw==")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            regex = '<a href="(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            for url in match:
                if 'zip' in url.lower():
                    if 'setting' in url.lower():
                        if '.php' in url.lower():
                            continue
                        name = url
                        url64b = base64.b64decode("aHR0cDovL2NvbG9tYm8uYWx0ZXJ2aXN0YS5vcmc=")
                        url = url64b + url

                        name = name.replace("/colombo/colombo/", "")
                        name = name.replace(".zip", "")
                        name = name.replace("%20", " ")
                        name = name.replace("_", " ")
                        name = name.replace("-", " ")
                        self.urls.append(url)
                        self.names.append(name)
                        self.downloading = True
                        self['info'].setText(_('Please select ...'))
                    else:
                        self['info'].setText(_('no data ...'))
                        self.downloading = False
            showlist(self.names, self['text'])
        except:
            self.downloading = False

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                print("url =", url)
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.zip'):
            fdest1 = "/tmp/unzipped"
            fdest2 = "/etc/enigma2"
            if os.path.exists(fdest1):
                cmd = "rm -rf '/tmp/unzipped'"
                os.system(cmd)
            os.makedirs('/tmp/unzipped')
            cmd2 = "unzip -o -q '/tmp/settings.zip' -d " + fdest1
            os.system(cmd2)
            if os.path.exists(fdest1):
                cmd = []
                cmd3 = "rm -rf /etc/enigma2/lamedb"
                cmd4 = "rm -rf /etc/enigma2/*.radio"
                cmd5 = "rm -rf /etc/enigma2/*.tv"
                cmd6 = "cp -rf /tmp/unzipped/* /etc/enigma2"
                cmd13 = "rm -rf /tmp/settings.zip"
                cmd14 = "rm -rf /tmp/unzipped"
                cmd.append(cmd3)
                cmd.append(cmd4)
                cmd.append(cmd5)
                cmd.append(cmd6)
                cmd.append(cmd13)
                cmd.append(cmd14)
                title = _("Installation Settings")
                self.session.open(Console, _(title),cmd)
                if not isDreamOS:
                    self.onShown.append(resettings)


class SettingVhan(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Vhannibal')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL3NhdC5hbGZhLXRlY2gubmV0L3VwbG9hZC9zZXR0aW5ncy92aGFubmliYWwv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            regex = '<a href="Vhannibal(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            for url in match:
                if 'zip' in url.lower():
                    if '.php' in url.lower():
                        continue
                    name = "Vhannibal" + url
                    name = name.replace(".zip", "")
                    name = name.replace("%20", " ")
                    url64b = base64.b64decode("aHR0cDovL3NhdC5hbGZhLXRlY2gubmV0L3VwbG9hZC9zZXR0aW5ncy92aGFubmliYWwvVmhhbm5pYmFs")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
                else:
                    self['info'].setText(_('no data ...'))
                    self.downloading = False
            showlist(self.names, self['text'])
        except:
            self.downloading = False

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                print("url =", url)
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.zip'):
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            fdest1 = "/tmp"
            fdest2 = "/etc/enigma2"
            cmd1 = "unzip -o -q '/tmp/settings.zip' -d " + fdest1
            cmd2 = "cp -rf  '/tmp/" + self.name + "'/* " + fdest2
            print("cmd2 =", cmd2)
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/settings.zip"
            cmd5 = "rm -rf /tmp/Vhannibal*"
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd2)
            cmd.append(cmd3)
            cmd.append(cmd4)
            cmd.append(cmd5)
            title = _("Installation Settings")
            self.session.open(Console, _(title),cmd)
            if not isDreamOS:
                self.onShown.append(resettings)


class SettingMilenka6121(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Milenka61')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvdGFyR3ov")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            regex = '<a href="Satvenus(.*?)".*?align="right">(.*?)-(.*?)-(.*?) '
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            for url, date1, date2, date3 in match:
                if url.find('.tar.gz') != -1 :
                    name = url.replace('Satvenus_EX-YU_Lista_za_milenka61_', '')
                    name = name + ' ' + date1 + '-' + date2 + '-' + date3
                    name = name.replace(".tar.gz", "")
                    name = name.replace("Satvenus", "").replace("milenka61 ", "")
                    name = name.replace("EX YU", "").replace("za", "")
                    name = name.replace("Lista", "").replace("%20", " ")
                    name = name.replace("-", " ").replace("_", " ")
                    url64b = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvdGFyR3ovU2F0dmVudXM=")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
                else:
                    self['info'].setText(_('no data ...'))
                    self.downloading = False
            showlist(self.names, self['text'])
        except:
            self.downloading = False

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                print("url =", url)
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.tar.gz'):
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            cmd1 = "tar -xvf /tmp/*.tar.gz -C /"
            print("cmd1 =", cmd1)
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/*.tar.gz"
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd3)
            cmd.append(cmd4)
            title = _("Installation Settings")
            self.session.open(Console, _(title),cmd)
            if not isDreamOS:
                self.onShown.append(resettings)

class SettingManutek(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Manutek')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL3d3dy5tYW51dGVrLml0L2lzZXR0aW5nLw==")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            match = re.compile('href=".*?file=(.+?)">', re.DOTALL).findall(self.xml)
            for url in match:
                if 'zip' in url.lower():
                    name = url
                    name = name.replace(".zip", "")
                    name = name.replace("%20", " ")
                    name = name.replace("NemoxyzRLS_", "")
                    name = name.replace("_", " ")
                    url64b = base64.b64decode("aHR0cDovL3d3dy5tYW51dGVrLml0L2lzZXR0aW5nL2VuaWdtYTIv")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
                else:
                    self['info'].setText(_('no data ...'))
                    self.downloading = False
            showlist(self.names, self['text'])
        except:
            self.downloading = False

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                print("url =", url)
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.zip'):
            fdest1 = "/tmp/unzipped"
            fdest2 = "/etc/enigma2"
            if os.path.exists("/tmp/unzipped"):
                cmd = "rm -rf '/tmp/unzipped'"
                os.system(cmd)
            os.makedirs('/tmp/unzipped')
            cmd2 = "unzip -o -q '/tmp/settings.zip' -d " + fdest1
            os.system(cmd2)

            for root, dirs, files in os.walk(fdest1):
                for name in dirs:
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    cmd3 = "cp -rf  '/tmp/unzipped/" + name + "'/* " + fdest2
                    cmd4 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
                    cmd5 = "rm -rf /tmp/settings.zip"
                    cmd6 = "rm -rf /tmp/unzipped"
                    cmd = []
                    cmd.append(cmd3)
                    cmd.append(cmd4)
                    cmd.append(cmd5)
                    cmd.append(cmd6)
                title = _("Installation Settings")
                self.session.open(Console, _(title),cmd)
            if not isDreamOS:
                self.onShown.append(resettings)

class SettingMorpheus2(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Morpheus')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL21vcnBoZXVzODgzLmFsdGVydmlzdGEub3JnL2Rvd25sb2FkL2luZGV4LnBocD9kaXI9")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            match = re.compile('href=".*?file=(.+?)">', re.DOTALL).findall(self.xml)
            for url in match:
                if 'zip' in url.lower():
                    if 'settings' in url.lower():
                        continue
                    name = url
                    name = name.replace(".zip", "")
                    name = name.replace("%20", " ")
                    name = name.replace("_", " ")
                    name = name.replace("Morph883", "Morpheus883")
                    name = name.replace("E2", "")
                    url64b = base64.b64decode("aHR0cDovL21vcnBoZXVzODgzLmFsdGVydmlzdGEub3JnL3NldHRpbmdzLw==")
                    url = url64b + url
                    # print('url 64b-url-', url)
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
                else:
                    self['info'].setText(_('no data ...'))
                    self.downloading = False
            showlist(self.names, self['text'])
        except:
            self.downloading = False

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                print("url =", url)
                url= str(url)
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.zip'):
            if os.path.exists("/tmp/unzipped"):
                os.system('rm -rf /tmp/unzipped')
            os.makedirs('/tmp/unzipped')
            os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
            path = '/tmp/unzipped'
            for root, dirs, files in os.walk(path):
                for pth in dirs:
                    cmd = []
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    cmd1 = "cp -rf /tmp/unzipped/" + pth + "/* '/etc/enigma2'"
                    cmd2 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
                    cmd.append(cmd1)
                    cmd.append(cmd2)
            title = _("Installation Settings")
            self.session.open(Console, _(title),cmd)
        # deletetmp()
        if not isDreamOS:
            self.onShown.append(resettings)

class SettingCiefp3(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Ciefp')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        # url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvQ2llZnA=")
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvQ2llZnAv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            regex = '<a href="ciefp(.*?)".*?align="right">(.*?)-(.*?)-(.*?) '
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            for url,date1, date2, date3 in match:
                if 'tar.gz' in url:
                    name = url
                    name = name.replace('-e2-settings-', 'Ciefp ')
                    name = name + ' ' + date1 + '-' + date2 + '-' + date3
                    name = name.replace(".tar.gz", "")
                    name = name.replace("%20", " ")
                    url64b = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvQ2llZnAvY2llZnA=")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
                else:
                    self['info'].setText(_('no data ...'))
                    self.downloading = False
            showlist(self.names, self['text'])
        except:
            pass

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                print("url =", url)
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.tar.gz'):
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            cmd1 = "tar -xvf /tmp/*.tar.gz -C /"
            print("cmd1 =", cmd1)
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/*.tar.gz"
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd3)
            cmd.append(cmd4)
            title = _("Installation Settings")
            self.session.open(Console, _(title),cmd)
            if not isDreamOS:
                self.onShown.append(resettings)

class tvSettingBi58(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Bi58')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvQmk1OC8=")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):

        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            regex = '<a href="bi58-e2(.*?)".*?align="right">(.*?)-(.*?)-(.*?) '
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            for url, date1, date2, date3 in match:
                if url.find('.tar.gz') != -1 :
                    name = url.replace('-settings-','bi58 ')
                    name = name + ' ' + date1 + '-' + date2 + '-' + date3
                    name = name.replace(".tar.gz", "")
                    name = name.replace("%20", " ")
                    url64b = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvQmk1OC9iaTU4LWUy")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
                else:
                    self['info'].setText(_('no data ...'))
                    self.downloading = False
            showlist(self.names, self['text'])
        except:
            pass

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                print("url =", url)
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.tar.gz'):
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            cmd1 = "tar -xvf /tmp/*.tar.gz -C /"
            print("cmd1 =", cmd1)
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/*.tar.gz"
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd3)
            cmd.append(cmd4)
            title = _("Installation Settings")
            self.session.open(Console, _(title),cmd)
            if not isDreamOS:
                self.onShown.append(resettings)

class SettingPredrag(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Predrag')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvUHJlZHJAZy8=")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):

        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            regex = '<a href="predrag(.*?)".*?align="right">(.*?)-(.*?)-(.*?) '
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            for url, date1, date2,date3 in match:
                if url.find('.tar.gz') != -1 :
                    name = url
                    name = name.replace('-settings-e2-','Predrag ')
                    name = name + date1 + '-' + date2 + '-' + date3
                    name = name.replace(".tar.gz", "")
                    url64b = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvUHJlZHJAZy9wcmVkcmFn")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
                else:
                    self['info'].setText(_('no data ...'))
                    self.downloading = False
            showlist(self.names, self['text'])
        except:
            pass

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                print("url =", url)
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.tar.gz'):
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            cmd1 = "tar -xvf /tmp/*.tar.gz -C /"
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/*.tar.gz"
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd3)
            cmd.append(cmd4)
            title = _("Installation Settings")
            self.session.open(Console, _(title),cmd)
            if not isDreamOS:
                self.onShown.append(resettings)
                
class CirusSetting(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Setting Cyrus')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['text'] = OneSetList([])
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL3d3dy5jeXJ1c3NldHRpbmdzLmNvbS9TZXRfMjlfMTFfMjAxMS9EcmVhbWJveC1JcEJveC9Db25maWcueG1s")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):

        self.xml = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            n1 = data.find('name="Sat">', 0)
            n2 = data.find("/ruleset>", n1)
            data1 = data[n1:n2]
        
            regex = 'Name="(.*?)".*?Link="(.*?)".*?Date="(.*?)"><'
            match = re.compile(regex,re.DOTALL).findall(data1)
            for name, url, date in match:
                if url.find('.zip') != -1 :
                    if 'ddt' in name.lower():
                        continue
                    if 'Sat' in name.lower():
                        continue
                    name = name + ' ' + date
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
                else:
                    self['info'].setText(_('no data ...'))
                    self.downloading = False
            showlist(self.names, self['text'])
        except:
            pass

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                if 'dtt' not in url.lower():
                    if not isDreamOS:
                        set = 1
                        terrestrial()
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close()

    def showError(self, error):
        print("download error =", error)
        self.close()

    def install(self, fplug):
        if os.path.exists('/tmp/settings.zip'):
            if os.path.exists("/tmp/unzipped"):
                os.system('rm -rf /tmp/unzipped')
            os.makedirs('/tmp/unzipped')
            os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
            path = '/tmp/unzipped'
            for root, dirs, files in os.walk(path):
                for pth in dirs:
                    cmd = []
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    cmd1 = "cp -rf /tmp/unzipped/" + pth + "/* '/etc/enigma2'"
                    cmd2 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
                    cmd.append(cmd1)
                    cmd.append(cmd2)
            title = _("Installation Settings")
            self.session.open(Console, _(title), cmd)
        # deletetmp()
            if not isDreamOS:
                self.onShown.append(resettings)                                                              

def main(session, **kwargs):
    if checkInternet():
        session.open(MainSetting)
    else:
        session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

def StartSetup(menuid):
    if menuid == 'scan':
        return [('TiVuStream Settings',
          main,
          'TiVuStream Settings',
          None)]
    else:
        return []

def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not isDreamOS:
        ico_path = plugin_path + '/res/pics/logo.png'
    return [PluginDescriptor(name=name_plug, description=_(title_plug), where=[PluginDescriptor.WHERE_PLUGINMENU], icon=ico_path, fnc=main),
     PluginDescriptor(name=_(name_plug), description=_(title_plug), where=PluginDescriptor.WHERE_MENU, fnc=StartSetup),
     PluginDescriptor(name=name_plug, description=_(title_plug), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]

def terrestrial():
    SavingProcessTerrestrialChannels = StartSavingTerrestrialChannels()
    # run a rescue reload
    import time
    now = time.time()
    ttime = time.localtime(now)
    tt = str('{0:02d}'.format(ttime[2])) + str('{0:02d}'.format(ttime[1])) + str(ttime[0])[2:] + '_' + str('{0:02d}'.format(ttime[3])) + str('{0:02d}'.format(ttime[4])) + str('{0:02d}'.format(ttime[5]))
    os.system('tar -czvf /tmp/' + tt + '_enigma2settingsbackup.tar.gz' + ' -C / /etc/enigma2/*.tv /etc/enigma2/*.radio /etc/enigma2/lamedb')

    if SavingProcessTerrestrialChannels:
        print('ok')
    return

def terrestrial_rest():
    if LamedbRestore():
        TransferBouquetTerrestrialFinal()
        icount = 0
        terrr = plugin_path + '/temp/TerrestrialChannelListArchive'
        if os.path.exists(terrr):
                os.system("cp -rf " + plugin_path + "/temp/TerrestrialChannelListArchive /etc/enigma2/userbouquet.terrestrial.tv")
        os.system('cp -rf /etc/enigma2/bouquets.tv /etc/enigma2/backup_bouquets.tv')
        with open('/etc/enigma2/bouquets.tv', 'r+') as f:
            bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial.tv" ORDER BY bouquet\n'
            if bouquetTvString not in f:
                new_bouquet = open('/etc/enigma2/new_bouquets.tv', 'w')
                new_bouquet.write('#NAME User - bouquets (TV)\n')
                new_bouquet.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial.tv" ORDER BY bouquet\n')
                file_read = open('/etc/enigma2/bouquets.tv').readlines()
                for line in file_read:
                    if line.startswith("#NAME"):
                        continue
                    new_bouquet.write(line)
                new_bouquet.close()
                os.system('cp -rf /etc/enigma2/bouquets.tv /etc/enigma2/backup_bouquets.tv')
                os.system('mv -f /etc/enigma2/new_bouquets.tv /etc/enigma2/bouquets.tv')
        lcnstart()

def lcnstart():
    print(' lcnstart ')
    if os.path.exists('/etc/enigma2/lcndb'):
    # if os.path.exists('/var/etc/enigma2/lamedb') :   
        lcn = LCN()
        lcn.read()
        if len(lcn.lcnlist) > 0:
            lcn.writeBouquet()
            # lcn.reloadBouquets()
            ReloadBouquet()
    return

def StartSavingTerrestrialChannels():
    def ForceSearchBouquetTerrestrial():
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            if 'tivustream' in file:
                continue
            f = open(file, "r").read()
            x = f.strip().lower()
            if x.find('http'):
                continue
            if x.find('eeee0000')!= -1:
                if x.find('82000') == -1 and x.find('c0000') == -1:
                    return file
                    break
        return

    def ResearchBouquetTerrestrial(search):
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            if 'tivustream' in file:
                continue
            f = open(file, "r").read()
            x = f.strip().lower()
            x1 = f.strip()
            if x1.find("#NAME") != -1:
                if x.lower().find((search.lower())) != -1:
                    if x.find('http'):
                        continue
                    if x.find('eeee0000')!= -1:
                        return file
                        break
        return


    def SaveTrasponderService():
        TrasponderListOldLamedb = open(plugin_path +'/temp/TrasponderListOldLamedb', 'w')
        ServiceListOldLamedb = open(plugin_path +'/temp/ServiceListOldLamedb', 'w')
        Trasponder = False
        inTransponder = False
        inService = False
        try:
          LamedbFile = open('/etc/enigma2/lamedb')
          while 1:
            line = LamedbFile.readline()
            if not line: break
            if not (inTransponder or inService):
              if line.find('transponders') == 0:
                inTransponder = True
              if line.find('services') == 0:
                inService = True
            if line.find('end') == 0:
              inTransponder = False
              inService = False
            line = line.lower()
            if line.find('eeee0000') != -1:
              Trasponder = True
              if inTransponder:
                TrasponderListOldLamedb.write(line)
                line = LamedbFile.readline()
                TrasponderListOldLamedb.write(line)
                line = LamedbFile.readline()
                TrasponderListOldLamedb.write(line)
              if inService:
                tmp = line.split(':')
                ServiceListOldLamedb.write(tmp[0] +":"+tmp[1]+":"+tmp[2]+":"+tmp[3]+":"+tmp[4]+":0\n")
                line = LamedbFile.readline()
                ServiceListOldLamedb.write(line)
                line = LamedbFile.readline()
                ServiceListOldLamedb.write(line)
          TrasponderListOldLamedb.close()
          ServiceListOldLamedb.close()
          if not Trasponder:
            os.system('rm -fr ' + plugin_path + '/temp/TrasponderListOldLamedb')
            os.system('rm -fr ' + plugin_path + '/temp/ServiceListOldLamedb')
        except:
            pass
        return Trasponder
        
       
    def CreateBouquetForce():
        WritingBouquetTemporary = open(plugin_path +'/temp/TerrestrialChannelListArchive','w')
        WritingBouquetTemporary.write('#NAME Terrestre\n')
        ReadingTempServicelist = open(plugin_path +'/temp/ServiceListOldLamedb').readlines()
        for jx in ReadingTempServicelist:
          if jx.find('eeee') != -1:
             String = jx.split(':')
             WritingBouquetTemporary.write('#SERVICE 1:0:%s:%s:%s:%s:%s:0:0:0:\n'% (hex(int(String[4]))[2:],String[0],String[2],String[3],String[1]))
        WritingBouquetTemporary.close()

   
    def SaveBouquetTerrestrial():
        NameDirectory = ResearchBouquetTerrestrial('terr')
        if not NameDirectory:
          NameDirectory = ForceSearchBouquetTerrestrial()
        try:
          shutil.copyfile(NameDirectory,plugin_path +'/temp/TerrestrialChannelListArchive')
          return True
        except :
          pass
        return

    Service = SaveTrasponderService()
    if Service:
      if not SaveBouquetTerrestrial():
        CreateBouquetForce()
      return True
    return

def LamedbRestore():
    try:

      TrasponderListNewLamedb = open(plugin_path +'/temp/TrasponderListNewLamedb', 'w')
      ServiceListNewLamedb = open(plugin_path +'/temp/ServiceListNewLamedb', 'w')
      inTransponder = False
      inService = False
      infile = open("/etc/enigma2/lamedb")
      while 1:
        line = infile.readline()
        if not line: break
        if not (inTransponder or inService):
          if line.find('transponders') == 0:
            inTransponder = True
          if line.find('services') == 0:
            inService = True
        if line.find('end') == 0:
          inTransponder = False
          inService = False
        if inTransponder:
          TrasponderListNewLamedb.write(line)
        if inService:
          ServiceListNewLamedb.write(line)
      TrasponderListNewLamedb.close()
      ServiceListNewLamedb.close()
      WritingLamedbFinal=open("/etc/enigma2/lamedb", "w")
      WritingLamedbFinal.write("eDVB services /4/\n")
      TrasponderListNewLamedb = open(plugin_path +'/temp/TrasponderListNewLamedb').readlines()
      for x in TrasponderListNewLamedb:
        WritingLamedbFinal.write(x)
      try:
        TrasponderListOldLamedb = open(plugin_path +'/temp/TrasponderListOldLamedb').readlines()
        for x in TrasponderListOldLamedb:
          WritingLamedbFinal.write(x)
      except:
        pass
      WritingLamedbFinal.write("end\n")
      ServiceListNewLamedb = open(plugin_path +'/temp/ServiceListNewLamedb').readlines()
      for x in ServiceListNewLamedb:
        WritingLamedbFinal.write(x)
      try:
        ServiceListOldLamedb = open(plugin_path +'/temp/ServiceListOldLamedb').readlines()
        for x in ServiceListOldLamedb:
          WritingLamedbFinal.write(x)
      except:
        pass
      WritingLamedbFinal.write("end\n")
      WritingLamedbFinal.close()
      return True
    except:
      return False



def TransferBouquetTerrestrialFinal():

        def RestoreTerrestrial():
          for file in os.listdir("/etc/enigma2/"):
            if re.search('^userbouquet.*.tv', file):
              f = open("/etc/enigma2/" + file, "r")
              x = f.read()
              if re.search("#NAME Digitale Terrestre",x, flags=re.IGNORECASE):
                return "/etc/enigma2/"+file
          # return

        try:
          TerrestrialChannelListArchive = open(plugin_path +'/temp/TerrestrialChannelListArchive').readlines()
          DirectoryUserBouquetTerrestrial = RestoreTerrestrial()
          if DirectoryUserBouquetTerrestrial:
            TrasfBouq = open(DirectoryUserBouquetTerrestrial,'w')
            for Line in TerrestrialChannelListArchive:
              if Line.lower().find('#name') != -1 :
                TrasfBouq.write('#NAME Digitale Terrestre\n')
              else:
                TrasfBouq.write(Line)
            TrasfBouq.close()
            return True
        except:
          return False    
#======================================================

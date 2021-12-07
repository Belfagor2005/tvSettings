#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------#
#  coded by Lululla  #
#   skin by MMark    #
#     21/09/2021     #
#--------------------#
#Info http://t.me/tivustream
from __future__ import print_function
from . import _
from Components.ActionMap import ActionMap
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
from .Lcn import *
global category
global pngx, pngl, pngs
currversion='1.7'
title_plug='..:: TiVuStream Settings V. %s ::..' % currversion
name_plug='TiVuStream Settings'
category = 'lululla.xml'
set = 0
from six.moves.urllib.parse import quote_plus
from six.moves.urllib.request import urlopen
from six.moves.urllib.request import Request
from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import quote
from six.moves.urllib.parse import urlencode
# from six.moves.urllib.error import HTTPError
# from six.moves.urllib.error import URLError
from six.moves.urllib.request import urlretrieve
# import six.moves.urllib.request
try:
    from Plugins.Extensions.tvSettings.Utils import *
except:
    from . import Utils

try:
    import zipfile
except:
    pass
    
if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext=ssl._create_unverified_context()
    except:
        sslContext=None

def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context= sslContext)
    else:
        return urlopen(url)

def ReloadBouquet():
    global set
    print('\n----Reloading bouquets----')
    if set == 1:
        set = 0
        terrestrial_rest()
    try:
        from enigma import eDVBDB
        eDVBDB.getInstance().reloadBouquets()
        print('bouquets reloaded...')        
    except ImportError:
        eDVBDB = None
        os.system('wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &')
        print('bouquets reloaded...')

os.system('rm -fr /usr/lib/enigma2/python/Plugins/Extensions/tvSettings/temp/*')# clean /temp
plugin_path=os.path.dirname(sys.modules[__name__].__file__)
ico_path=plugin_path + '/logo.png'
res_plugin_path=plugin_path + '/res/'
pngl=res_plugin_path + 'pics/plugin.png'
pngs=res_plugin_path + 'pics/setting.png'
pngx=res_plugin_path + 'pics/plugins.png'

if isFHD():
    skin_path=res_plugin_path + 'skins/fhd/'
else:
    skin_path=res_plugin_path + 'skins/hd/'
if DreamOS():
    skin_path=skin_path + 'dreamOs/'

Panel_Dlist=[
 ('SETTINGS BI58'),
 ('SETTINGS CIEFP'),
 ('SETTINGS CYRUS'),
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
        if isFHD():
            self.l.setItemHeight(50)
        else:
            self.l.setItemHeight(50)

class OneSetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if isFHD():
            self.l.setItemHeight(50)
            textfont=int(34)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont=int(22)
            self.l.setFont(0, gFont('Regular', textfont))

def DListEntry(name, idx):
    res=[name]
    if isFHD():

        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1900, 50), font=6, text=name, color= 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:

        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=0, text=name, color= 0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res

def OneSetListEntry(name):
    res= [name]
    if isFHD():

        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1900, 50), font=0, text=name, color= 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=0, text=name, color= 0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res

def showlist(data, list):
    icount= 0
    plist= []
    for line in data:
        name= data[icount]
        plist.append(OneSetListEntry(name))
        icount= icount+1
        list.setList(plist)


class MainSetting(Screen):
    def __init__(self, session):
        self.session= session
        skin= skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin= f.read()
        self.setup_title= ('MainSetting')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self['text']=SetList([])
        self['title']=Label(_(title_plug))
        self['info']=Label('')
        self['info'].setText(_('Getting the list, please wait ...'))
        self['key_green']=Button(_('Select'))
        self['key_red']=Button(_('Exit'))
        self['key_yellow']=Button(_('Lcn'))
        if DreamOS():
                self['key_yellow'].hide()
        self["key_blue"]=Button(_(''))
        self['key_blue'].hide()
        self['actions']=ActionMap(['SetupActions', 'ColorActions', ], {'ok': self.okRun,
         'green': self.okRun,
         'back': self.closerm,
         'red': self.closerm,
         'yellow': self.Lcn,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def Lcn(self):
        self.mbox=self.session.open(MessageBox, _('Reorder Terrestrial channels with Lcn rules'), MessageBox.TYPE_INFO, timeout=5)
        lcnstart()

    def closerm(self):
        self.close()

    def updateMenuList(self):
        self.menu_list=[]
        for x in self.menu_list:
            del self.menu_list[0]
        list=[]
        idx=0
        for x in Panel_Dlist:
            list.append(DListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)
        self['info'].setText(_('Please select ...'))

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel=self.menu_list[idx]
        if sel== _('UPDATE SATELLITES.XML'):
            self.okSATELLITE()
        elif sel== _('UPDATE TERRESTRIAL.XML'):
            self.okTERRESTRIAL()
        elif sel== ('SETTINGS CIEFP'):
            self.session.open(SettingCiefp)
        elif sel== ('SETTINGS CYRUS'):
            self.session.open(CirusSetting)
        elif sel== ('SETTINGS BI58'):
            self.session.open(tvSettingBi58)
        elif sel== ('SETTINGS MANUTEK'):
            self.session.open(SettingManutek)
        elif sel== ('SETTINGS MILENKA61'):
            self.session.open(SettingMilenka6121)
        elif sel== ('SETTINGS MORPHEUS'):
            self.session.open(SettingMorpheus2)
        elif sel== ('SETTINGS PREDRAG'):
            self.session.open(SettingPredrag)
        elif sel== ('SETTINGS VHANNIBAL'):
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
                self.mbox = self.session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

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
                self.mbox = self.session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

class SettingVhan(Screen):

    def __init__(self, session):
        self.session=session
        skin=skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin=f.read()
        self.setup_title=('Setting Vhannibal')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list=[]
        self['text']=OneSetList([])
        self.icount=0
        self['info']=Label(_('Getting the list, please wait ...'))
        self['key_green']=Button(_('Install'))
        self['key_red']=Button(_('Back'))
        self['key_yellow']=Button(_(''))
        self["key_blue"]=Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading=False
        self.timer=eTimer()
        self.timer.start(500, 1)
        if DreamOS():
            self.timer_conn=self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title']=Label(_(title_plug))
        self['actions']=ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url='http://sat.alfa-tech.net/upload/settings/vhannibal/'
        r=ReadUrl2(url)
        print('rrrrrrrr ', r)
        if six.PY3:
            r  = six.ensure_str(r)
        self.names=[]
        self.urls=[]
        try:
            regex   = '<a href="Vhannibal(.*?).zip"'
            match   = re.compile(regex).findall(r)
            for url in match:
                if '.php' in url.lower():
                    continue
                name = "Vhannibal" + url
                name = name.replace(".zip", "")
                name = name.replace("%20", " ")
                url = "http://sat.alfa-tech.net/upload/settings/vhannibal/Vhannibal" + url + '.zip'
                url = checkStr(url)
                name = checkStr(name)
                self.urls.append(url)
                self.names.append(name)
                self.downloading = True
                self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except Exception as e:
            print(('downxmlpage get failed: ', str(e)))

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
                self.dest = "/tmp/settings.zip"
                print("url =", url)
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                urlretrieve(url, self.dest)
                if os.path.exists(self.dest):
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["unzip -o -q '/tmp/settings.zip' -d /tmp; cp -rf '/tmp/" + str(self.name) + "'/* /etc/enigma2; wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess =False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquet()

class SettingMilenka6121(Screen):
    def __init__(self, session):
        self.session=session
        skin=skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin=f.read()
        self.setup_title=('Setting Milenka61')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list=[]
        self['text']=OneSetList([])
        self.icount=0
        self['info']=Label(_('Getting the list, please wait ...'))
        self['key_green']=Button(_('Install'))
        self['key_red']=Button(_('Back'))
        self['key_yellow']=Button(_(''))
        self["key_blue"]=Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading=False
        self.timer=eTimer()
        self.timer.start(500, True)
        if DreamOS():
            self.timer_conn=self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title']=Label(_(title_plug))
        self['actions']=ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://178.63.156.75/tarGz/'
        data = ReadUrl2(url)
        r = data
        print('rrrrrrrr ', r)
        self.names  = []
        self.urls   = []
        try:
            regex   = '<a href="Satvenus(.*?)".*?align="right">(.*?)-(.*?)-(.*?) '
            match   = re.compile(regex).findall(r)
            for url, date1, date2, date3 in match:
                if url.find('.tar.gz') != -1 :
                    name = url.replace('_EX-YU_Lista_za_milenka61_', '')
                    name = name + ' ' + date1 + '-' + date2 + '-' + date3
                    name = name.replace("_", " ").replace(".tar.gz", "")
                    url = "http://178.63.156.75/tarGz/Satvenus" + url
                    url = checkStr(url)
                    name = checkStr(name)
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except Exception as e:
            print(('downxmlpage get failed: ', str(e)))

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                self.dest = "/tmp/settings.tar.gz"
                print("url =", url)
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                urlretrieve(url, self.dest)
                if os.path.exists('/tmp/settings.tar.gz'):
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["tar -xvf /tmp/settings.tar.gz -C /; wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess =False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquet()

class SettingManutek(Screen):
    def __init__(self, session):
        self.session=session
        skin=skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin=f.read()
        self.setup_title=('Setting Manutek')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list=[]
        self['text']=OneSetList([])
        self.icount=0
        self['info']=Label(_('Getting the list, please wait ...'))
        self['key_green']=Button(_('Install'))
        self['key_red']=Button(_('Back'))
        self['key_yellow']=Button(_(''))
        self["key_blue"]=Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading=False
        self.timer=eTimer()
        self.timer.start(500, True)
        if DreamOS():
            self.timer_conn=self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title']=Label(_(title_plug))
        self['actions']=ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://www.manutek.it/isetting/'
        data = ReadUrl2(url)
        r = data
        print('rrrrrrrr ', r)
        self.names  = []
        self.urls   = []
        try:
            regex   = 'href=".*?file=(.+?).zip">'
            match   = re.compile(regex).findall(r)
            for url in match:
                name = url
                name = name.replace(".zip", "")
                name = name.replace("%20", " ")
                name = name.replace("NemoxyzRLS_", "")
                name = name.replace("_", " ")
                url = 'http://www.manutek.it/isetting/enigma2/' + url + '.zip'
                url = checkStr(url)
                name = checkStr(name)
                self.urls.append(url)
                self.names.append(name)
                self.downloading = True
                self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except Exception as e:
            print(('downxmlpage get failed: ', str(e)))

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                self.dest = "/tmp/settings.zip"
                print("url =", url)
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                urlretrieve(url, self.dest)
                if os.path.exists(self.dest):
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
                            os.system("cp -rf  '/tmp/unzipped/" + name + "'/* " + fdest2)
                        title = _("Installation Settings")
                        self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["tar -xvf /tmp/settings.tar.gz -C /; wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess =False)
                    self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquet()

class SettingMorpheus2(Screen):
    def __init__(self, session):
        self.session=session
        skin=skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin=f.read()
        self.setup_title=('Setting Morpheus')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list=[]
        self['text']=OneSetList([])
        self.icount=0
        self['info']=Label(_('Getting the list, please wait ...'))
        self['key_green']=Button(_('Install'))
        self['key_red']=Button(_('Back'))
        self['key_yellow']=Button(_(''))
        self["key_blue"]=Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading=False
        self.timer=eTimer()
        self.timer.start(500, True)
        if DreamOS():
            self.timer_conn=self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title']=Label(_(title_plug))
        self['actions']=ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = r'http://morpheus883.altervista.org/download/index.php'
        data = ReadUrl2(url)
        r = data
        print('rrrrrrrr ', r)
        self.names  = []
        self.urls   = []
        try:
            #href="/download/index.php?dir=&amp;file=
            regex   = 'href="/download/.*?file=(.*?)">'
            match   = re.compile(regex).findall(r)
            for url in match:
                if 'zip' in url.lower():
                    self.downloading = True
                    if 'settings' in url.lower():
                        continue
                    name = url
                    name = name.replace(".zip", "")
                    name = name.replace("%20", " ")
                    name = name.replace("_", " ")
                    name = name.replace("Morph883", "Morpheus883")
                    name = name.replace("E2", "")
                    url = "http://morpheus883.altervista.org/settings/" + url
                    url = checkStr(url)
                    name = checkStr(name)
                    self.urls.append(url)
                    self.names.append(name)
                    print("url =", url)
                    print("name =", name)
                    self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except Exception as e:
            print(('downxmlpage get failed: ', str(e)))

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        print("self.downloading is =", self.downloading)
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                self.dest = "/tmp/settings.zip"
                print("url =", url)
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                urlretrieve(url, self.dest)
                if os.path.exists(self.dest):
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
                    os.makedirs('/tmp/unzipped')
                    os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
                    path = '/tmp/unzipped'
                    # pth = ''
                    for root, dirs, files in os.walk(path):
                        for pth in dirs:
                            cmd = []
                            os.system('rm -rf /etc/enigma2/lamedb')
                            os.system('rm -rf /etc/enigma2/*.radio')
                            os.system('rm -rf /etc/enigma2/*.tv')
                            os.system("cp -rf /tmp/unzipped/" + pth + "/* '/etc/enigma2'")
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"],closeOnSuccess =False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquet()

class SettingCiefp(Screen):
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
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['pth'] = Label('')
        self['pform'] = Label('')
        # self['progress'] = ProgressBar()
        # self["progress"].hide()
        # self['progresstext'] = StaticText()
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(500, 1)
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

#https://github.com/ciefp/ciefpsettings-enigma2-zipped/raw/master/ciefp-E2-4satA-28E-19E-13E-30W-14.08.2021.zip
#/ciefp/ciefpsettings-enigma2-zipped/blob/master/ciefp-E2-9sat-28E-23E-19E-16E-13E-9E-1.9E-0.8W-5W-14.08.2021.zip
#https://github.com//ciefp/ciefpsettings-enigma2-zipped/raw/master/ciefp-E2-9sat-28E-23E-19E-16E-13E-9E-1.9E-0.8W-5W-14.08.2021.zip
#<span class="css-truncate css-truncate-target d-block width-fit"><a class="js-navigation-open Link--primary" title="ciefp-E2-10sat-39E-28E-23E-19E-16E-13E-9E-4.8E-1.9E-0.8W-14.08.2021.zip" data-pjax="#repo-content-pjax-container" href="/ciefp/ciefpsettings-enigma2-zipped/blob/master/ciefp-E2-10sat-39E-28E-23E-19E-16E-13E-9E-4.8E-1.9E-0.8W-14.08.2021.zip">ciefp-E2-10sat-39E-28E-23E-19E-16E-13E-9E-4.8E-1.9E-0.8W-14.08.2021.zip</a></span>
    def downxmlpage(self):
        url = 'https://github.com/ciefp/ciefpsettings-enigma2-zipped'
        data = ReadUrl2(url)
        r = data
        print('rrrrrrrr ', r)
        self.names  = []
        self.urls   = []
        try:
            n1 = r.find('Details">', 0)
            n2 = r.find('href="#readme">', n1)
            r = r[n1:n2]
            regex   = 'title="ciefp-E2-(.*?)".*?href="(.*?)"'
            match   = re.compile(regex).findall(r)
            for name, url in match:
                if url.find('.zip') != -1 :
                    if 'ddt' in name.lower():
                        continue
                    if 'Sat' in name.lower():
                        continue
                    # name = name + ' ' + date
                    name = checkStr(name)
                    url = url.replace('blob', 'raw')
                    url = 'https://github.com' + url
                    url = checkStr(url)
                    print('name ', name)
                    print('url ', url)
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except Exception as e:
            print(('downxmlpage get failed: ', str(e)))

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                self.dest = "/tmp/settings.zip"
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                urlretrieve(url, self.dest)
                if os.path.exists(self.dest):
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
                    os.makedirs('/tmp/unzipped')
                    os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
                    path = '/tmp/unzipped'
                    for root, dirs, files in os.walk(path):
                        for pth in dirs:
                            pth = pth
                            os.system('rm -rf /etc/enigma2/lamedb')
                            os.system('rm -rf /etc/enigma2/*.radio')
                            os.system('rm -rf /etc/enigma2/*.tv')
                            os.system("cp -rf /tmp/unzipped/" + pth + "/* '/etc/enigma2'")
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"] , closeOnSuccess =False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquet()

class tvSettingBi58(Screen):
    def __init__(self, session):
        self.session=session
        skin=skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin=f.read()
        self.setup_title=('Setting Bi58')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list=[]
        self['text']=OneSetList([])
        self.icount=0
        self['info']=Label(_('Getting the list, please wait ...'))
        self['key_green']=Button(_('Install'))
        self['key_red']=Button(_('Back'))
        self['key_yellow']=Button(_(''))
        self["key_blue"]=Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading=False
        self.timer=eTimer()
        self.timer.start(500, True)
        if DreamOS():
            self.timer_conn=self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title']=Label(_(title_plug))
        self['actions']=ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://178.63.156.75/paneladdons/Bi58/'
        data = ReadUrl2(url)
        r = data
        print('rrrrrrrr ', r)
        self.names  = []
        self.urls   = []
        try:
            regex   = '<a href="bi58-e2(.*?)".*?align="right">(.*?)-(.*?)-(.*?) '
            match   = re.compile(regex).findall(r)
            for url, date1, date2, date3 in match:
                if url.find('.tar.gz') != -1 :
                    name = url.replace('-settings-','bi58 ')
                    name = name + ' ' + date1 + '-' + date2 + '-' + date3
                    name = name.replace(".tar.gz", "")
                    name = name.replace("%20", " ")
                    url = "http://178.63.156.75/paneladdons/Bi58/bi58-e2" + url
                    url = checkStr(url)
                    name = checkStr(name)
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except Exception as e:
            print(('downxmlpage get failed: ', str(e)))

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                self.dest = "/tmp/settings.tar.gz"
                print("url =", url)
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                urlretrieve(url, self.dest)
                if os.path.exists('/tmp/settings.tar.gz'):
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["tar -xvf /tmp/settings.tar.gz -C /; wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess =False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquet()

class SettingPredrag(Screen):
    def __init__(self, session):
        self.session=session
        skin=skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin=f.read()
        self.setup_title=('Setting Predrag')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list=[]
        self['text']=OneSetList([])
        self.icount=0
        self['info']=Label(_('Getting the list, please wait ...'))
        self['key_green']=Button(_('Install'))
        self['key_red']=Button(_('Back'))
        self['key_yellow']=Button(_(''))
        self["key_blue"]=Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading=False
        self.timer=eTimer()
        self.timer.start(500, True)
        if DreamOS():
            self.timer_conn=self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title']=Label(_(title_plug))
        self['actions']=ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://178.63.156.75/paneladdons/Predr@g/'
        data = ReadUrl2(url)
        r = data
        print('rrrrrrrr ', r)
        self.names  = []
        self.urls   = []
        try:
            regex   = '<a href="predrag(.*?)".*?align="right">(.*?)-(.*?)-(.*?) '
            match   = re.compile(regex).findall(r)
            for url, date1, date2, date3 in match:
                if url.find('.tar.gz') != -1 :
                    name = url
                    name = name.replace('-settings-e2-','Predrag ')
                    name = name + date1 + '-' + date2 + '-' + date3
                    name = name.replace(".tar.gz", "")
                    url = "http://178.63.156.75/paneladdons/Predr@g/predrag" + url
                    url = checkStr(url)
                    name = checkStr(name)
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except Exception as e:
            print(('downxmlpage get failed: ', str(e)))

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
                self.dest = "/tmp/settings.tar.gz"
                print("url =", url)
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                urlretrieve(url, self.dest)
                if os.path.exists('/tmp/settings.tar.gz'):
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["tar -xvf /tmp/settings.tar.gz -C /; wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess =False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquet()

class CirusSetting(Screen):
    def __init__(self, session):
        self.session=session
        skin=skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin=f.read()
        self.setup_title=('Setting Cyrus')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list=[]
        self['text']=OneSetList([])
        self.icount=0
        self['info']=Label(_('Getting the list, please wait ...'))
        self['key_green']=Button(_('Install'))
        self['key_red']=Button(_('Back'))
        self['key_yellow']=Button(_(''))
        self["key_blue"]=Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading=False
        self.timer=eTimer()
        self.timer.start(500, True)
        if DreamOS():
            self.timer_conn=self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title']=Label(_(title_plug))
        self['actions']=ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://www.cyrussettings.com/Set_29_11_2011/Dreambox-IpBox/Config.xml'
        data = ReadUrl2(url)
        r = data
        print('rrrrrrrr ', r)
        self.names  = []
        self.urls   = []
        try:
            n1 = r.find('name="Sat">', 0)
            n2 = r.find("/ruleset>", n1)
            r = r[n1:n2]
            regex   = 'Name="(.*?)".*?Link="(.*?)".*?Date="(.*?)"><'
            match   = re.compile(regex).findall(r)
            for name, url, date in match:
                if url.find('.zip') != -1 :
                    if 'ddt' in name.lower():
                        continue
                    if 'Sat' in name.lower():
                        continue
                    name = name + ' ' + date
                    name = checkStr(name)
                    url = checkStr(url)
                    self.urls.append(url)
                    self.names.append(name)
                    self.downloading = True
                    self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except Exception as e:
            print(('downxmlpage get failed: ', str(e)))

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        global set
        set = 0
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                url = self.urls[idx]
                self.dest = "/tmp/settings.zip"
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                urlretrieve(url, self.dest)
                if os.path.exists(self.dest):
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
                    os.makedirs('/tmp/unzipped')
                    os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
                    path = '/tmp/unzipped'
                    for root, dirs, files in os.walk(path):
                        for pth in dirs:
                            pth = pth
                            os.system('rm -rf /etc/enigma2/lamedb')
                            os.system('rm -rf /etc/enigma2/*.radio')
                            os.system('rm -rf /etc/enigma2/*.tv')
                            os.system("cp -rf /tmp/unzipped/" + pth + "/* '/etc/enigma2'")
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"] , closeOnSuccess =False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquet()

class tvConsole(Screen):
# def __init__(self, session, title = 'Console', cmdlist = None, finishedCallback = None, closeOnSuccess = False, showStartStopText = True, skin = None):
    def __init__(self, session, title ="Console", cmdlist =None, finishedCallback =None, closeOnSuccess =False, endstr =''):
        self.session = session
        skin = skin_path + 'tvConsole.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Console')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.endstr = endstr
        self.errorOcurred = False
        self['title'] = Label(_(title_plug))
        self['text'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions', 'ColorActions'], {'ok': self.cancel,
         'back': self.cancel,
         'red': self.cancel,
         "blue": self.restartenigma,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown}, -1)
        self.cmdlist = cmdlist
        self.newtitle = _(title_plug)
        self.onShown.append(self.updateTitle)
        self.container = eConsoleAppContainer()
        self.run=0
        try:
            self.container.appClosed.append(self.runFinished)
            self.container.dataAvail.append(self.dataAvail)
        except:
            self.appClosed_conn = self.container.appClosed.connect(self.runFinished)
            self.dataAvail_conn = self.container.dataAvail.connect(self.dataAvail)
        self.onLayoutFinish.append(self.startRun)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        self['text'].setText(_('Execution Progress:') + '\n\n')
        print('Console: executing in run', self.run, ' the command:', self.cmdlist[self.run])
        if self.container.execute(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            self.show()
            self.finished = True
            str= self["text"].getText()
            if not retval and self.endstr.startswith("Swapping"):
               str += _("\n\n" + self.endstr)
            else:
               str += _("Execution finished!!\n")
            self["text"].setText(str)
            self["text"].lastPage()
            # if self.finishedCallback != None:
                    # self.finishedCallback(retval)
            # if not retval and self.closeOnSuccess:
            self.cancel()

    def cancel(self):
        if self.run == len(self.cmdlist):
            self.close()
            try:
                self.appClosed_conn = None
                self.dataAvail_conn = None
            except:
                self.container.appClosed.remove(self.runFinished)
                self.container.dataAvail.remove(self.dataAvail)

    def cancelCallback(self, ret = None):
        self.cancel_msg = None
        if ret:
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)
            self.container.kill()
            self.close()
        return
    def dataAvail(self, data):
        if six.PY3:
            data = data.decode("utf-8")
        try:
            self["text"].setText(self["text"].getText() + data)
        except:
            trace_error()
        return
        if self["text"].getText().endswith("Do you want to continue? [Y/n] "):
            msg= self.session.openWithCallback(self.processAnswer, MessageBox, _("Additional packages must be installed. Do you want to continue?"), MessageBox.TYPE_YESNO)

    def processAnswer(self, retval):
        if retval:
            self.container.write("Y",1)
        else:
            self.container.write("n",1)
        self.dataSent_conn = self.container.dataSent.connect(self.processInput)

    def processInput(self, retval):
        self.container.sendEOF()

    def restartenigma(self):
        self.session.open(TryQuitMainloop, 3)

    def closeConsole(self):
        if self.finished:
            try:
                self.container.appClosed.append(self.runFinished)
                self.container.dataAvail.append(self.dataAvail)
            except:
                self.appClosed_conn = self.container.appClosed.connect(self.runFinished)
                self.dataAvail_conn = self.container.dataAvail.connect(self.dataAvail)
                self.close()
            else:
                self.show()

def main(session, **kwargs):
    session.open(MainSetting)


def StartSetup(menuid):
    if menuid== 'scan':
        return [('TiVuStream Settings',
          main,
          'TiVuStream Settings',
          None)]
    else:
        return []

def Plugins(**kwargs):
    ico_path='logo.png'
    if not os.path.exists('/var/lib/dpkg/status'):
        ico_path=plugin_path + '/res/pics/logo.png'
    return [PluginDescriptor(name=name_plug, description=_(title_plug), where=[PluginDescriptor.WHERE_PLUGINMENU], icon=ico_path, fnc=main),
     PluginDescriptor(name=_(name_plug), description=_(title_plug), where=PluginDescriptor.WHERE_MENU, fnc=StartSetup),
     PluginDescriptor(name=name_plug, description=_(title_plug), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]

def terrestrial():
    SavingProcessTerrestrialChannels=StartSavingTerrestrialChannels()
    # run a rescue reload
    import time
    now=time.time()
    ttime=time.localtime(now)
    tt=str('{0:02d}'.format(ttime[2])) + str('{0:02d}'.format(ttime[1])) + str(ttime[0])[2:] + '_' + str('{0:02d}'.format(ttime[3])) + str('{0:02d}'.format(ttime[4])) + str('{0:02d}'.format(ttime[5]))
    os.system('tar -czvf /tmp/' + tt + '_enigma2settingsbackup.tar.gz' + ' -C / /etc/enigma2/*.tv /etc/enigma2/*.radio /etc/enigma2/lamedb')

    if SavingProcessTerrestrialChannels:
        print('ok')
    return

def terrestrial_rest():
    if LamedbRestore():
        TransferBouquetTerrestrialFinal()
        icount=0
        terrr=plugin_path + '/temp/TerrestrialChannelListArchive'
        if os.path.exists(terrr):
                os.system("cp -rf " + plugin_path + "/temp/TerrestrialChannelListArchive /etc/enigma2/userbouquet.terrestrial.tv")
        os.system('cp -rf /etc/enigma2/bouquets.tv /etc/enigma2/backup_bouquets.tv')
        with open('/etc/enigma2/bouquets.tv', 'r+') as f:
            bouquetTvString='#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial.tv" ORDER BY bouquet\n'
            if bouquetTvString not in f:
                new_bouquet=open('/etc/enigma2/new_bouquets.tv', 'w')
                new_bouquet.write('#NAME User - bouquets (TV)\n')
                new_bouquet.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial.tv" ORDER BY bouquet\n')
                file_read=open('/etc/enigma2/bouquets.tv').readlines()
                for line in file_read:
                    if line.startswith("#NAME"):
                        continue
                    new_bouquet.write(line)
                new_bouquet.close()
                os.system('cp -rf /etc/enigma2/bouquets.tv /etc/enigma2/backup_bouquets.tv')
                os.system('mv -f /etc/enigma2/new_bouquets.tv /etc/enigma2/bouquets.tv')
        # if not os.path.exists('/var/lib/dpkg/status'):
        lcnstart()

def lcnstart():
    print(' lcnstart ')
    if os.path.exists('/etc/enigma2/lcndb'):
        lcn=LCN()
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
            f=open(file, "r").read()
            x=f.strip().lower()
            if x.find('http'):
                continue
            if x.find('eeee0000')!= -1:
                if x.find('82000')== -1 and x.find('c0000')== -1:
                    return file
                    break
        return

    def ResearchBouquetTerrestrial(search):
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            if 'tivustream' in file:
                continue
            f=open(file, "r").read()
            x=f.strip().lower()
            x1=f.strip()
            if x1.find("#NAME") != -1:
                if x.lower().find((search.lower())) != -1:
                    if x.find('http'):
                        continue
                    if x.find('eeee0000')!= -1:
                        return file
                        break
        return

    def SaveTrasponderService():
        TrasponderListOldLamedb=open(plugin_path +'/temp/TrasponderListOldLamedb', 'w')
        ServiceListOldLamedb=open(plugin_path +'/temp/ServiceListOldLamedb', 'w')
        Trasponder=False
        inTransponder=False
        inService=False
        try:
          LamedbFile=open('/etc/enigma2/lamedb')
          while 1:
            line=LamedbFile.readline()
            if not line: break
            if not (inTransponder or inService):
              if line.find('transponders')== 0:
                inTransponder=True
              if line.find('services')== 0:
                inService=True
            if line.find('end')== 0:
              inTransponder=False
              inService=False
            line=line.lower()
            if line.find('eeee0000') != -1:
              Trasponder=True
              if inTransponder:
                TrasponderListOldLamedb.write(line)
                line=LamedbFile.readline()
                TrasponderListOldLamedb.write(line)
                line=LamedbFile.readline()
                TrasponderListOldLamedb.write(line)
              if inService:
                tmp=line.split(':')
                ServiceListOldLamedb.write(tmp[0] +":"+tmp[1]+":"+tmp[2]+":"+tmp[3]+":"+tmp[4]+":0\n")
                line=LamedbFile.readline()
                ServiceListOldLamedb.write(line)
                line=LamedbFile.readline()
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
        WritingBouquetTemporary=open(plugin_path +'/temp/TerrestrialChannelListArchive','w')
        WritingBouquetTemporary.write('#NAME Terrestre\n')
        ReadingTempServicelist=open(plugin_path +'/temp/ServiceListOldLamedb').readlines()
        for jx in ReadingTempServicelist:
          if jx.find('eeee') != -1:
             String=jx.split(':')
             WritingBouquetTemporary.write('#SERVICE 1:0:%s:%s:%s:%s:%s:0:0:0:\n'% (hex(int(String[4]))[2:],String[0],String[2],String[3],String[1]))
        WritingBouquetTemporary.close()

    def SaveBouquetTerrestrial():
        NameDirectory=ResearchBouquetTerrestrial('terr')
        if not NameDirectory:
          NameDirectory=ForceSearchBouquetTerrestrial()
        try:
          shutil.copyfile(NameDirectory,plugin_path +'/temp/TerrestrialChannelListArchive')
          return True
        except :
          pass
        return

    Service=SaveTrasponderService()
    if Service:
      if not SaveBouquetTerrestrial():
        CreateBouquetForce()
      return True
    return

def LamedbRestore():
    try:

      TrasponderListNewLamedb=open(plugin_path +'/temp/TrasponderListNewLamedb', 'w')
      ServiceListNewLamedb=open(plugin_path +'/temp/ServiceListNewLamedb', 'w')
      inTransponder=False
      inService=False
      infile=open("/etc/enigma2/lamedb")
      while 1:
        line=infile.readline()
        if not line: break
        if not (inTransponder or inService):
          if line.find('transponders')== 0:
            inTransponder=True
          if line.find('services')== 0:
            inService=True
        if line.find('end')== 0:
          inTransponder=False
          inService=False
        if inTransponder:
          TrasponderListNewLamedb.write(line)
        if inService:
          ServiceListNewLamedb.write(line)
      TrasponderListNewLamedb.close()
      ServiceListNewLamedb.close()
      WritingLamedbFinal=open("/etc/enigma2/lamedb", "w")
      WritingLamedbFinal.write("eDVB services /4/\n")
      TrasponderListNewLamedb=open(plugin_path +'/temp/TrasponderListNewLamedb').readlines()
      for x in TrasponderListNewLamedb:
        WritingLamedbFinal.write(x)
      try:
        TrasponderListOldLamedb=open(plugin_path +'/temp/TrasponderListOldLamedb').readlines()
        for x in TrasponderListOldLamedb:
          WritingLamedbFinal.write(x)
      except:
        pass
      WritingLamedbFinal.write("end\n")
      ServiceListNewLamedb=open(plugin_path +'/temp/ServiceListNewLamedb').readlines()
      for x in ServiceListNewLamedb:
        WritingLamedbFinal.write(x)
      try:
        ServiceListOldLamedb=open(plugin_path +'/temp/ServiceListOldLamedb').readlines()
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
              f=open("/etc/enigma2/" + file, "r")
              x=f.read()
              if re.search("#NAME Digitale Terrestre",x, flags=re.IGNORECASE):
                return "/etc/enigma2/"+file
          # return
        try:
          TerrestrialChannelListArchive=open(plugin_path +'/temp/TerrestrialChannelListArchive').readlines()
          DirectoryUserBouquetTerrestrial=RestoreTerrestrial()
          if DirectoryUserBouquetTerrestrial:
            TrasfBouq=open(DirectoryUserBouquetTerrestrial,'w')
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

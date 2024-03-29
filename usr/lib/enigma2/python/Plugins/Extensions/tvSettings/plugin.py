#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------#
#  coded by Lululla  #
#   skin by MMark    #
#     04/07/2023     #
# --------------------#
# Info http://t.me/tivustream

from __future__ import print_function
from . import _
from . import Utils
from .Lcn import LCN
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.MultiContent import MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.ScrollLabel import ScrollLabel
from Screens.Standby import TryQuitMainloop
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS, fileExists, resolveFilename
from enigma import RT_HALIGN_LEFT, RT_VALIGN_CENTER, loadPNG
from enigma import eTimer, eListboxPythonMultiContent
from enigma import eConsoleAppContainer, gFont
from twisted.web.client import downloadPage
from enigma import getDesktop
import codecs
import os
import re
import sys
import shutil
import ssl
import glob
import six

global category
global set
set = 0

PY3 = sys.version_info.major >= 3
if PY3:
    from urllib.error import URLError
    from urllib.request import urlopen, Request
    from urllib.parse import urlparse
    unicode = str
    unichr = chr
    long = int
    PY3 = True
else:
    from urllib2 import urlopen, Request, URLError
    from urlparse import urlparse


if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None


def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)


try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False

if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx


def make_request(url):
    try:
        import requests
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            link = requests.get(url, headers={'User-Agent': Utils.RequestAgent()}, timeout=15, verify=False, stream=True).text
        return link
    except ImportError:
        req = Request(url)
        req.add_header('User-Agent', 'E2 Plugin TVaddon Panel')
        response = urlopen(req, None, 10)
        link = response.read().decode('utf-8')
        response.close()
        return link
    return


def ReloadBouquets():
    from enigma import eDVBDB
    print("\n----Reloading bouquets----")
    global set
    if set == 1:
        set = 0
        print("\n----Reloading Terrestrial----")
        terrestrial_rest()
    if eDVBDB:
        eDVBDB.getInstance().reloadServicelist()
        eDVBDB.getInstance().reloadBouquets()
        print("eDVBDB: bouquets reloaded...")
    else:
        os.system("wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &")
        os.system("wget -qO - http://127.0.0.1/web/servicelistreload?mode=4 > /dev/null 2>&1 &")
        print("wGET: bouquets reloaded...")


os.system('rm -fr /usr/lib/enigma2/python/Plugins/Extensions/tvSettings/temp/*')  # clean /temp
currversion = '1.7'
title_plug = '..:: TiVuStream Settings V. %s ::..' % currversion
name_plug = 'TiVuStream Settings'
category = 'lululla.xml'
# plugin_path = os.path.dirname(sys.modules[__name__].__file__)
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/tvSettings'
ico_path = os.path.join(plugin_path, 'logo.png')
no_cover = os.path.join(plugin_path, 'no_coverArt.png')
res_plugin_path = os.path.join(plugin_path, 'res/')
_firstStarttvsset = True
ee2ldb = '/etc/enigma2/lamedb'
ServOldLamedb = plugin_path + '/temp/ServiceListOldLamedb'
TransOldLamedb = plugin_path + '/temp/TrasponderListOldLamedb'
TerChArch = plugin_path + '/temp/TerrestrialChannelListArchive'
# SelBack = plugin_path + '/SelectBack'
# SSelect = plugin_path + '/Select'
# DIGTV = 'eeee0000'

screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    skin_path = plugin_path + '/res/skins/uhd/'
elif screenwidth.width() == 1920:
    skin_path = plugin_path + '/res/skins/fhd/'
else:
    skin_path = plugin_path + '/res/skins/hd/'

if os.path.exists('/var/lib/dpkg/info'):
    skin_path = skin_path + 'dreamOs/'

Panel_Dlist = [
               ('SAVE DTT BOUQUET'),
               ('RESTORE DTT BOUQUET'),
               ('SETTINGS BI58'),
               ('SETTINGS CIEFP'),
               ('SETTINGS CYRUS'),
               ('SETTINGS MANUTEK'),
               ('SETTINGS MILENKA61'),
               ('SETTINGS MORPHEUS'),
               ('SETTINGS PREDRAG'),
               ('SETTINGS VHANNIBAL'),
               ('SETTINGS VHANNIBAL 2'),
               ('UPDATE SATELLITES.XML'),
               ('UPDATE TERRESTRIAL.XML'),
               ]


class OneSetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if screenwidth.width() == 2560:
            self.l.setItemHeight(60)
            textfont = int(44)
            self.l.setFont(0, gFont('Regular', textfont))
        elif screenwidth.width() == 1920:
            self.l.setItemHeight(50)
            textfont = int(32)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


def DListEntry(name, idx):
    res = [name]
    pngs = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('tvSettings'))
    if screenwidth.width() == 2560:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(50, 50), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1200, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 10), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(50, 0), size=(500, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(DListEntry(name, icount))
        icount += 1
        list.setList(plist)


class MainSetting(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('MainSetting')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self['list'] = OneSetList([])
        self['title'] = Label(_(title_plug))
        self['info'] = Label('')
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self['key_yellow'] = Button('')
        self['key_yellow'].hide()
        self['key_green'].hide()
        self.LcnOn = False
        if os.path.exists('/etc/enigma2/lcndb'):
            self['key_yellow'].show()
            self['key_yellow'] = Button('Lcn')
            self.LcnOn = True
        self["key_blue"] = Button('')
        self['key_blue'].hide()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'back': self.cancel,
                                                       'red': self.cancel,
                                                       'yellow': self.Lcn,
                                                       'cancel': self.cancel}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def Lcn(self):
        if self.LcnOn:
            lcn = LCN()
            lcn.read()
            if len(lcn.lcnlist) > 0:
                lcn.writeBouquet()
                lcn.ReloadBouquets()
                self.session.open(MessageBox, _('Sorting Terrestrial channels with Lcn rules Completed'), MessageBox.TYPE_INFO, timeout=5)

    def cancel(self):
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
        self['list'].setList(list)
        self['key_green'].show()
        self['info'].setText(_('Please select ...'))

    def okRun(self):
        self.keyNumberGlobalCB(self['list'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        if sel == ('SAVE DTT BOUQUET'):
            self.terrestrialsave()
        elif sel == ('RESTORE DTT BOUQUET'):
            self.terrestrial_restore()
        elif sel == ('SETTINGS CIEFP'):
            self.session.open(SettingCiefp)
        elif sel == ('SETTINGS CYRUS'):
            self.session.open(SettingCyrus)
        elif sel == ('SETTINGS BI58'):
            self.session.open(SettingBi58)
        elif sel == ('SETTINGS MANUTEK'):
            self.session.open(SettingManutek)
        elif sel == ('SETTINGS MILENKA61'):
            self.session.open(SettingMilenka61)
        elif sel == ('SETTINGS MORPHEUS'):
            self.session.open(SettingMorpheus)
        elif sel == ('SETTINGS PREDRAG'):
            self.session.open(SettingPredrag)
        elif sel == ('SETTINGS VHANNIBAL'):
            self.session.open(SettingVhan)
        elif sel == ('SETTINGS VHANNIBAL 2'):
            self.session.open(SettingVhan2)
        elif sel == _('UPDATE SATELLITES.XML'):
            self.okSATELLITE()
        elif sel == _('UPDATE TERRESTRIAL.XML'):
            self.okTERRESTRIAL()
        else:
            return

    def terrestrial_restore(self):
        self.session.openWithCallback(self.terrestrial_restore2, MessageBox, _("This operation restore your Favorite channel Dtt\nfrom =>>THISPLUGIN/temp/TerrestrialChannelListArchive\nDo you really want to continue?"), MessageBox.TYPE_YESNO)

    def terrestrial_restore2(self, answer):
        if answer:
            terrestrial_rest()

    def terrestrialsave(self):
        self.session.openWithCallback(self.terrestrialsave2, MessageBox, _("This operation save your Favorite channel Dtt\nto =>>/tmp/*_enigma2settingsbackup.tar.gz\nDo you really want to continue?"), MessageBox.TYPE_YESNO)

    def terrestrialsave2(self, answer):
        if answer:
            terrestrial()

    def okSATELLITE(self):
        self.session.openWithCallback(self.okSATELLITE2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okSATELLITE2(self, answer):
        if answer:
            if Utils.checkInternet():
                try:
                    url_sat_oealliance = 'http://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/satellites.xml'
                    link_sat = ssl_urlopen(url_sat_oealliance)
                    dirCopy = '/etc/tuxbox/satellites.xml'
                    import requests
                    r = requests.get(link_sat)
                    with open(dirCopy, 'wb') as f:
                        f.write(r.content)
                    self.session.open(MessageBox, _('Satellites.xml Updated!'), MessageBox.TYPE_INFO, timeout=5)
                    self['info'].setText(_('Installation done !!!'))
                except Exception as e:
                    print('error: ', str(e))
            else:
                self.session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

    def okTERRESTRIAL(self):
        self.session.openWithCallback(self.okTERRESTRIAL2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okTERRESTRIAL2(self, answer):
        if answer:
            if Utils.checkInternet():
                try:
                    url_sat_oealliance = 'https://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/terrestrial.xml'
                    link_ter = ssl_urlopen(url_sat_oealliance)
                    dirCopy = '/etc/tuxbox/terrestrial.xml'
                    import requests
                    r = requests.get(link_ter)
                    with open(dirCopy, 'wb') as f:
                        f.write(r.content)
                    self.session.open(MessageBox, _('Terrestrial.xml Updated!'), MessageBox.TYPE_INFO, timeout=5)
                    self['info'].setText(_('Installation done !!!'))
                except Exception as e:
                    print('error: ', str(e))
            else:
                self.session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)


class SettingVhan(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Vhannibal')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        self.names = []
        self.urls = []
        try:
            urlsat = 'https://www.vhannibal.net/asd.php'
            r = make_request(urlsat)
            if PY3:
                r = six.ensure_str(r)
            match = re.compile('<td><a href="(.+?)">(.+?)</a></td>.*?<td>(.+?)</td>', re.DOTALL).findall(r)
            for url, name, date in match:
                name = name.replace('&#127381;', '') + ' ' + date
                url = "https://www.vhannibal.net/" + url
                self.urls.append(Utils.checkStr(url.strip()))
                self.names.append(Utils.checkStr(name.strip()))
            self.downloading = True
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                import requests
                r = requests.get(url)
                with open(dest, 'wb') as f:
                    f.write(r.content)

                if 'dtt' not in self.name.lower():
                    set = 1
                    terrestrial()
                if os.path.exists(dest):
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
                            self.namel = name
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    os.system("cp -rf  '/tmp/unzipped/" + str(self.namel) + "/'* " + fdest2)
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &; sleep 3"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
                else:
                    self['info'].setText(_('Settings Not Installed ...'))
            else:
                self['info'].setText(_('No Downloading ...'))

    def yes(self):
        ReloadBouquets()


class SettingVhan2(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Vhannibal')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://sat.alfa-tech.net/upload/settings/vhannibal/'
        r = make_request(url)
        if PY3:
            r = six.ensure_str(r)
        self.names = []
        self.urls = []
        try:
            regex = '<a href="Vhannibal(.*?).zip"'
            match = re.compile(regex).findall(r)
            for url in match:
                if '.php' in url.lower():
                    continue
                name = "Vhannibal" + url
                name = name.replace('&#127381;', '').replace("%20", " ")
                url = "http://sat.alfa-tech.net/upload/settings/vhannibal/Vhannibal" + url + '.zip'
                self.urls.append(Utils.checkStr(url.strip()))
                self.names.append(Utils.checkStr(name.strip()))
                self.downloading = True
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                try:
                    idx = self["list"].getSelectionIndex()
                    self.name = self.names[idx]
                    url = self.urls[idx]
                    dest = "/tmp/settings.zip"
                    if 'dtt' not in url.lower():
                        # if not os.path.exists('/var/lib/dpkg/status'):
                        set = 1
                        terrestrial()
                    if PY3:
                        url = six.ensure_binary(url)
                    if url.startswith(b"https") and sslverify:
                        parsed_uri = urlparse(url)
                        domain = parsed_uri.hostname
                        sniFactory = SNIFactory(domain)
                        downloadPage(url, dest, sniFactory, timeout=5).addCallback(self.download, dest).addErrback(self.downloadError)
                    else:
                        downloadPage(url, dest).addCallback(self.download, dest).addErrback(self.downloadError)
                except Exception as e:
                    print('error: ', str(e))

    def download(self, data, dest):
        try:
            if os.path.exists(dest):
                self.namel = ''
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
                        self.namel = name
                os.system('rm -rf /etc/enigma2/lamedb')
                os.system('rm -rf /etc/enigma2/*.radio')
                os.system('rm -rf /etc/enigma2/*.tv')
                os.system('rm -rf /etc/enigma2/*.del')
                os.system("cp -rf  '/tmp/unzipped/" + str(self.namel) + "/'* " + fdest2)
                title = _("Installation Settings")
                self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &; sleep 3"], closeOnSuccess=False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

        except Exception as e:
            print('error: ', str(e))
            self['info'].setText(_('Not Installed ...'))

    def downloadError(self, png):
        try:
            if not fileExists(png):
                self.poster_resize(no_cover)
        except Exception as e:
            print('error: ', str(e))

    def yes(self):
        ReloadBouquets()


class SettingMilenka61(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Milenka61')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://178.63.156.75/tarGz/'
        data = make_request(url)
        if PY3:
            data = six.ensure_str(data)
        r = data
        self.names = []
        self.urls = []
        try:
            regex = '<a href="Satvenus(.+?)".*?align="right">(.*?) </td>'
            # regex = '<a href="Satvenus(.+?)".+?align="right">(.*?)-(.*?)-(.*?) .+?</td'
            match = re.compile(regex).findall(r)
            for url, txt in match:
                if url.find('.tar.gz') != -1:
                    name = url.replace('_EX-YU_Lista_za_milenka61_', '')
                    date = re.search("(.+?)-(.+?)-(.+?) ", txt).group()
                    name = name + ' ' + date
                    name = name.replace("_", " ").replace(".tar.gz", "")
                    url = "http://178.63.156.75/tarGz/Satvenus" + url
                    self.urls.append(Utils.checkStr(url.strip()))
                    self.names.append(Utils.checkStr(name.strip()))
                self.downloading = True
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                if 'dtt' not in url.lower():
                    set = 1
                    terrestrial()
                import requests
                r = requests.get(url)
                with open(dest, 'wb') as f:
                    f.write(r.content)
                if os.path.exists('/tmp/settings.tar.gz'):
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["tar -xvf /tmp/settings.tar.gz -C /; wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquets()


class SettingManutek(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Manutek')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://www.manutek.it/isetting/index.php'
        data = make_request(url)
        if PY3:
            data = six.ensure_str(data)
        r = data
        self.names = []
        self.urls = []
        try:
            regex = 'href="/isetting/.*?file=(.+?).zip">'
            match = re.compile(regex).findall(r)
            for url in match:
                name = url
                url = 'http://www.manutek.it/isetting/enigma2/' + url + '.zip'
                name = name.replace("NemoxyzRLS_Manutek_", "").replace("_", " ").replace("%20", " ")
                self.urls.append(Utils.checkStr(url.strip()))
                self.names.append(Utils.checkStr(name.strip()))
                self.downloading = True
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                if 'dtt' not in url.lower():
                    set = 1
                    terrestrial()
                import requests
                r = requests.get(url)
                with open(dest, 'wb') as f:
                    f.write(r.content)
                if os.path.exists(dest):
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
                            self.namel = name
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    os.system("cp -rf  '/tmp/unzipped/" + str(self.namel) + "/'* " + fdest2)
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &; sleep 3"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquets()


class SettingMorpheus(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Morpheus')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'https://github.com/morpheus883/enigma2-zipped'
        data = make_request(url)
        if PY3:
            data = six.ensure_str(data)
        r = data
        self.names = []
        self.urls = []
        try:
            regex = 'title="E2_Morph883_(.*?).zip".*?href="(.*?)"'
            match = re.compile(regex).findall(r)
            for name, url in match:
                if url.find('.zip') != -1:
                    url = url.replace('blob', 'raw')
                    url = 'https://github.com' + url
                    name = 'Morph883 ' + name
                    self.urls.append(Utils.checkStr(url.strip()))
                    self.names.append(Utils.checkStr(name.strip()))
                    self.downloading = True
            self['key_green'].show()
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                if 'dtt' not in url.lower():
                    # if not os.path.exists('/var/lib/dpkg/status'):
                    set = 1
                    terrestrial()
                import requests
                r = requests.get(url)
                with open(dest, 'wb') as f:
                    f.write(r.content)
                if os.path.exists(dest):
                    # fdest1 = "/tmp/unzipped"
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
                    os.makedirs('/tmp/unzipped')
                    os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
                    path = '/tmp/unzipped'
                    # pth = ''
                    for root, dirs, files in os.walk(path):
                        for name in dirs:
                            self.namel = name
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    os.system("cp -rf  '/tmp/unzipped/" + str(self.namel) + "/'* " + fdest2)
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquets()


class SettingCiefp(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Ciefp')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['pth'] = Label('')
        self['pform'] = Label('')
        # self['progress'] = ProgressBar()
        # self["progress"].hide()
        # self['progresstext'] = StaticText()
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'https://github.com/ciefp/ciefpsettings-enigma2-zipped'
        data = make_request(url)
        if PY3:
            data = six.ensure_str(data)
        r = data
        self.names = []
        self.urls = []
        try:
            n1 = r.find('title="README.txt', 0)
            n2 = r.find('href="#readme">', n1)
            r = r[n1:n2]
            regex = 'title="ciefp-E2-(.*?).zip".*?href="(.*?)"'
            match = re.compile(regex).findall(r)
            for name, url in match:
                if url.find('.zip') != -1:
                    url = url.replace('blob', 'raw')
                    url = 'https://github.com' + url
                    self.urls.append(Utils.checkStr(url.strip()))
                    self.names.append(Utils.checkStr(name.strip()))
                    self.downloading = True
            self['key_green'].show()
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                if 'dtt' not in url.lower():
                    set = 1
                    terrestrial()
                import requests
                r = requests.get(url)
                with open(dest, 'wb') as f:
                    f.write(r.content)
                if os.path.exists(dest):
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
                    os.makedirs('/tmp/unzipped')
                    os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
                    path = '/tmp/unzipped'
                    for root, dirs, files in os.walk(path):
                        for name in dirs:
                            self.namel = name
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    os.system("cp -rf  '/tmp/unzipped/" + str(self.namel) + "/'* " + fdest2)
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquets()


class SettingBi58(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Bi58')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://178.63.156.75/paneladdons/Bi58/'
        data = make_request(url)
        if PY3:
            data = six.ensure_str(data)
        r = data
        self.names = []
        self.urls = []
        try:
            regex = '<a href="bi58-e2(.*?)".*?align="right">(.*?) </td>'
            match = re.compile(regex).findall(r)
            for url, txt in match:
                if url.find('.tar.gz') != -1:
                    name = url.replace('-settings-', 'bi58 ')
                    date = re.search("(.+?)-(.+?)-(.+?) ", txt).group()
                    name = name + ' ' + date
                    name = name.replace(".tar.gz", "").replace("%20", " ")
                    url = "http://178.63.156.75/paneladdons/Bi58/bi58-e2" + url
                    self.urls.append(Utils.checkStr(url.strip()))
                    self.names.append(Utils.checkStr(name.strip()))
                    self.downloading = True
            self['key_green'].show()
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                if 'dtt' not in url.lower():
                    set = 1
                    terrestrial()
                import requests
                r = requests.get(url)
                with open(dest, 'wb') as f:
                    f.write(r.content)
                if os.path.exists('/tmp/settings.tar.gz'):
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["tar -xvf /tmp/settings.tar.gz -C /; wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquets()


class SettingPredrag(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Predrag')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://178.63.156.75/paneladdons/Predr@g/'
        data = make_request(url)
        if PY3:
            data = six.ensure_str(data)
        r = data
        self.names = []
        self.urls = []
        try:
            regex = '<a href="predrag(.*?)".*?align="right">(.*?) </td>'
            match = re.compile(regex).findall(r)
            for url, txt in match:
                if url.find('.tar.gz') != -1:
                    name = url.replace('-settings-e2-', 'Predrag ')
                    date = re.search("(.+?)-(.+?)-(.+?) ", txt).group()
                    name = name + ' ' + date
                    name = name.replace(".tar.gz", "").replace("%20", " ")
                    url = "http://178.63.156.75/paneladdons/Predr@g/predrag" + url
                    self.urls.append(Utils.checkStr(url.strip()))
                    self.names.append(Utils.checkStr(name.strip()))
                    self.downloading = True
            self['key_green'].show()
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                if 'dtt' not in url.lower():
                    set = 1
                    terrestrial()
                import requests
                r = requests.get(url)
                with open(dest, 'wb') as f:
                    f.write(r.content)
                if os.path.exists('/tmp/settings.tar.gz'):
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["tar -xvf /tmp/settings.tar.gz -C /; wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquets()


class SettingCyrus(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Cyrus')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(_(title_plug))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://www.cyrussettings.com/Set_29_11_2011/Dreambox-IpBox/Config.xml'
        data = make_request(url)
        if PY3:
            data = six.ensure_str(data)
        r = data
        self.names = []
        self.urls = []
        try:
            n1 = r.find('name="Sat">', 0)
            n2 = r.find("/ruleset>", n1)
            r = r[n1:n2]
            regex = 'Name="(.*?)".*?Link="(.*?)".*?Date="(.*?)"><'
            match = re.compile(regex).findall(r)
            for name, url, date in match:
                if url.find('.zip') != -1:
                    if 'ddt' in name.lower():
                        continue
                    if 'Sat' in name.lower():
                        continue
                    name = name + ' ' + date
                    self.urls.append(Utils.checkStr(url.strip()))
                    self.names.append(Utils.checkStr(name.strip()))
                    self.downloading = True
            self['key_green'].show()
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['list'])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def okRun(self):
        self.session.openWithCallback(self.okRun2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun2(self, answer):
        if answer:
            global set
            set = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                if 'dtt' not in url.lower():
                    set = 1
                    terrestrial()
                import requests
                r = requests.get(url)
                with open(dest, 'wb') as f:
                    f.write(r.content)
                if os.path.exists(dest):
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
                    os.makedirs('/tmp/unzipped')
                    os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
                    path = '/tmp/unzipped'
                    for root, dirs, files in os.walk(path):
                        for name in dirs:
                            self.namel = name
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    os.system("cp -rf  '/tmp/unzipped/" + str(self.namel) + "/'* " + fdest2)
                    title = _("Installation Settings")
                    self.session.openWithCallback(self.yes, tvConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquets()


class tvConsole(Screen):
    def __init__(self, session, title="Console", cmdlist=None, finishedCallback=None, closeOnSuccess=False, endstr=''):
        self.session = session
        skin = os.path.join(skin_path, 'tvConsole.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Console')
        Screen.__init__(self, session)
        self.setTitle(_(title_plug))
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.endstr = endstr
        self.errorOcurred = False
        self['title'] = Label(_(title_plug))
        self['list'] = ScrollLabel('')
        self['actions'] = ActionMap(['DirectionActions',
                                     'ColorActions'], {'ok': self.cancel,
                                                       'back': self.cancel,
                                                       'red': self.cancel,
                                                       'blue': self.restartenigma,
                                                       'up': self['list'].pageUp,
                                                       'down': self['list'].pageDown}, -1)
        self.cmdlist = cmdlist
        self.newtitle = _(title_plug)
        self.onShown.append(self.updateTitle)
        self.container = eConsoleAppContainer()
        self.run = 0
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
        self['list'].setText(_('Execution Progress:') + '\n\n')
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
            str = self["list"].getText()
            if not retval and self.endstr.startswith("Swapping"):
                str += _("\n\n" + self.endstr)
            else:
                str += _("Execution finished!!\n")
            self["list"].setText(str)
            self["list"].lastPage()
            # if self.finishedCallback is not None:
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

    def cancelCallback(self, ret=None):
        self.cancel_msg = None
        if ret:
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)
            self.container.kill()
            self.close()
        return

    def dataAvail(self, data):
        if PY3:
            data = data.decode("utf-8")
        try:
            self["list"].setText(self["list"].getText() + data)
        except Exception as e:
            # trace_error()
            print(e)
            
        return
        if self["list"].getText().endswith("Do you want to continue? [Y/n] "):
            self.session.openWithCallback(self.processAnswer, MessageBox, _("Additional packages must be installed. Do you want to continue?"), MessageBox.TYPE_YESNO)

    def processAnswer(self, retval):
        if retval:
            self.container.write("Y", 1)
        else:
            self.container.write("n", 1)
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


class AutoStartTimertvsset:

    def __init__(self, session):
        self.session = session
        global _firstStarttvsset
        print("*** running AutoStartTimertvsset ***")
        if _firstStarttvsset:
            self.runUpdate()

    def runUpdate(self):
        print("*** running update ***")
        try:
            from . import Update
            Update.upd_done()
            _firstStarttvsset = False
        except Exception as e:
            print('error tvsetting', str(e))


def autostart(reason, session=None, **kwargs):
    print("*** running autostart ***")
    global autoStartTimertvsset
    global _firstStarttvsset
    if reason == 0:
        if session is not None:
            _firstStarttvsset = True
            autoStartTimertvsset = AutoStartTimertvsset(session)
    return


def main(session, **kwargs):
    try:
        session.open(MainSetting)
    except:
        import traceback
        traceback.print_exc()
        pass


def StartSetup(menuid, **kwargs):
    if menuid == 'scan':
        return [('TiVuStream Settings',
                 main,
                 'TiVuStream',
                 None)]
    else:
        return []


def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not os.path.exists('/var/lib/dpkg/status'):
        ico_path = os.path.join(plugin_path, 'res/pics/logo.png')
    return [PluginDescriptor(name=name_plug, description=title_plug, where=[PluginDescriptor.WHERE_PLUGINMENU], icon=ico_path, fnc=main),
            PluginDescriptor(name=name_plug, description=title_plug, where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=autostart),
            PluginDescriptor(name=name_plug, description=title_plug, where=PluginDescriptor.WHERE_MENU, fnc=StartSetup),
            PluginDescriptor(name=name_plug, description=title_plug, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]


def terrestrial():
    SavingProcessTerrestrialChannels = StartSavingTerrestrialChannels()
    import time
    now = time.time()
    ttime = time.localtime(now)
    tt = str('{0:02d}'.format(ttime[2])) + str('{0:02d}'.format(ttime[1])) + str(ttime[0])[2:] + '_' + str('{0:02d}'.format(ttime[3])) + str('{0:02d}'.format(ttime[4])) + str('{0:02d}'.format(ttime[5]))
    os.system('tar -czvf /tmp/' + tt + '_enigma2settingsbackup.tar.gz' + ' -C / /etc/enigma2/*.tv /etc/enigma2/*.radio /etc/enigma2/lamedb')
    if SavingProcessTerrestrialChannels:
        print('SavingProcessTerrestrialChannels')
    return


def terrestrial_rest():
    if LamedbRestore():
        TransferBouquetTerrestrialFinal()
        # terrr = os.path.join(plugin_path, 'temp/TerrestrialChannelListArchive')
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
        if os.path.exists('/etc/enigma2/lcndb'):
            lcnstart()


def lcnstart():
    print(' lcnstart ')
    if os.path.exists('/etc/enigma2/lcndb'):
        lcn = LCN()
        lcn.read()
        if len(lcn.lcnlist) > 0:
            lcn.writeBouquet()
            ReloadBouquets()
    return


def StartSavingTerrestrialChannels():

    def ForceSearchBouquetTerrestrial():
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            f = open(file, "r").read()
            x = f.strip().lower()
            if x.find('eeee') != -1:
                return file
                break
            # if x.find('eeee0000') != -1:
                # if x.find('82000') == -1 or x.find('c0000') == -1:
                    # return file
                    # break
        return

    def ResearchBouquetTerrestrial(search):
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            f = open(file, "r").read()
            x = f.strip().lower()
            x1 = f.strip()
            if x1.find("#NAME") != -1:
                if x.lower().find(search.lower()) != -1:
                    if x.find('eeee') != -1:
                        return file
                        break
        return

    def SaveTrasponderService():
        TrasponderListOldLamedb = open(TransOldLamedb, 'w')
        ServiceListOldLamedb = open(ServOldLamedb, 'w')
        Trasponder = False
        inTransponder = False
        inService = False
        try:
            LamedbFile = open(ee2ldb, 'r')
            while 1:
                line = LamedbFile.readline()
                if not line:
                    break
                if not (inTransponder or inService):
                    if line.find('transponders') == 0:
                        inTransponder = True
                    if line.find('services') == 0:
                        inService = True
                if line.find('end') == 0:
                    inTransponder = False
                    inService = False
                line = line.lower()
                if line.find('eeee') != -1:
                    Trasponder = True
                    if inTransponder:
                        TrasponderListOldLamedb.write(line)
                        line = LamedbFile.readline()
                        TrasponderListOldLamedb.write(line)
                        line = LamedbFile.readline()
                        TrasponderListOldLamedb.write(line)
                    if inService:
                        tmp = line.split(':')
                        ServiceListOldLamedb.write(tmp[0] + ":" + tmp[1] + ":" + tmp[2] + ":" + tmp[3] + ":" + tmp[4] + ":0\n")
                        line = LamedbFile.readline()
                        ServiceListOldLamedb.write(line)
                        line = LamedbFile.readline()
                        ServiceListOldLamedb.write(line)
            TrasponderListOldLamedb.close()
            ServiceListOldLamedb.close()
            if not Trasponder:
                os.system('rm -fr ' + TransOldLamedb)
                os.system('rm -fr ' + ServOldLamedb)
        except:
            pass
        return Trasponder

    def CreateBouquetForce():
        WritingBouquetTemporary = open(TerChArch, 'w')
        WritingBouquetTemporary.write('#NAME terrestre\n')
        ReadingTempServicelist = open(ServOldLamedb, 'r').readlines()
        for jx in ReadingTempServicelist:
            if jx.find('eeee') != -1:
                String = jx.split(':')
                WritingBouquetTemporary.write('#SERVICE 1:0:%s:%s:%s:%s:%s:0:0:0:\n' % (hex(int(String[4]))[2:], String[0], String[2], String[3], String[1]))
        WritingBouquetTemporary.close()

    def SaveBouquetTerrestrial():
        NameDirectory = ResearchBouquetTerrestrial('terr')
        if not NameDirectory:
            NameDirectory = ForceSearchBouquetTerrestrial()
        try:
            shutil.copyfile(NameDirectory, TerChArch)
            return True
        except:
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
        TrasponderListNewLamedb = open(plugin_path + '/temp/TrasponderListNewLamedb', 'w')
        ServiceListNewLamedb = open(plugin_path + '/temp/ServiceListNewLamedb', 'w')
        inTransponder = False
        inService = False
        infile = open(ee2ldb, 'r')
        while 1:
            line = infile.readline()
            if not line:
                break
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
        WritingLamedbFinal = open(ee2ldb, "w")
        WritingLamedbFinal.write("eDVB services /4/\n")
        TrasponderListNewLamedb = open(plugin_path + '/temp/TrasponderListNewLamedb', 'r').readlines()
        for x in TrasponderListNewLamedb:
            WritingLamedbFinal.write(x)
        try:
            TrasponderListOldLamedb = open(TransOldLamedb, 'r').readlines()
            for x in TrasponderListOldLamedb:
                WritingLamedbFinal.write(x)
        except:
            pass
        WritingLamedbFinal.write("end\n")
        ServiceListNewLamedb = open(plugin_path + '/temp/ServiceListNewLamedb', 'r').readlines()
        for x in ServiceListNewLamedb:
            WritingLamedbFinal.write(x)
        try:
            ServiceListOldLamedb = open(ServOldLamedb, 'r').readlines()
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
                if re.search('#NAME Digitale Terrestre', x, flags=re.IGNORECASE) or re.search('#NAME DTT', x, flags=re.IGNORECASE):  # for disa51
                    return "/etc/enigma2/" + file
        return

    try:
        TerrestrialChannelListArchive = open(TerChArch, 'r').readlines()
        DirectoryUserBouquetTerrestrial = RestoreTerrestrial()
        if DirectoryUserBouquetTerrestrial:
            TrasfBouq = open(DirectoryUserBouquetTerrestrial, 'w')
            for Line in TerrestrialChannelListArchive:
                if Line.lower().find('#name') != -1:
                    TrasfBouq.write('#NAME Digitale Terrestre\n')
                else:
                    TrasfBouq.write(Line)
            TrasfBouq.close()
            return True
    except:
        return False
    return
# ===== by lululla

#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------#
#  coded by Lululla  #
#   skin by MMark    #
#     30/07/2023     #
# --------------------#
# Info http://t.me/tivustream

from __future__ import print_function
from . import _, wgetsts
from . import Utils
from .Console import Console as xConsole
from .Utils import RequestAgent
from . Lcn import (
    LCN,
    terrestrial,
    terrestrial_rest,
    ReloadBouquets,
    keepiptv,
)
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import (MultiContentEntryText, MultiContentEntryPixmapAlphaTest)
# from Components.Pixmap import Pixmap
# from Components.ScrollLabel import ScrollLabel
# from Screens.Standby import TryQuitMainloop
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import (SCOPE_PLUGINS, fileExists, resolveFilename)

from enigma import (
    RT_HALIGN_LEFT,
    RT_VALIGN_CENTER,
    eListboxPythonMultiContent,
    # ePicLoad,
    # eServiceReference,
    eTimer,
    gFont,
    # gPixmapPtr,
    getDesktop,
    # iPlayableService,
    # iServiceInformation,
    loadPNG,
    # eConsoleAppContainer,
)
from twisted.web.client import downloadPage
from datetime import datetime
import codecs
# import glob
import json
import os
import re
# import shutil
import six
import ssl
import sys

global category
global setx
setx = 0

PY3 = sys.version_info.major >= 3
if PY3:
    from urllib.request import (urlopen, Request)
    from urllib.parse import urlparse
    unicode = str
    unichr = chr
    long = int
    PY3 = True
else:
    from urllib2 import (urlopen, Request)
    from urlparse import urlparse


if sys.version_info >= (2, 7, 9):
    try:
        # import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

try:
    wgetsts()
except:
    pass


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
        response = requests.get(url, verify=False, timeout=5)
        if response.status_code == 200:
            link = requests.get(url, headers={'User-Agent': Utils.RequestAgent()}, timeout=10, verify=False, stream=True).text
        return link
    except ImportError:
        req = Request(url)
        req.add_header('User-Agent', 'E2 Plugin Lululla')
        response = urlopen(req, None, 10)
        link = response.read().decode('utf-8')
        response.close()
        return link
    return


def checkGZIP(url):
    from io import StringIO
    import gzip
    hdr = {"User-Agent": RequestAgent()}
    response = None
    request = Request(url, headers=hdr)
    try:
        response = urlopen(request, timeout=10)
        if response.info().get('Content-Encoding') == 'gzip':
            buffer = StringIO(response.read())
            deflatedContent = gzip.GzipFile(fileobj=buffer)
            if PY3:
                return deflatedContent.read().decode('utf-8')
            else:
                return deflatedContent.read()
        else:
            if PY3:
                return response.read().decode('utf-8')
            else:
                return response.read()
    except Exception as e:
        print(e)
        return None


os.system('rm -fr /usr/lib/enigma2/python/Plugins/Extensions/tvSettings/temp/*')  # clean /temp
currversion = '1.9'
title_plug = '..:: TiVuStream Settings V. %s ::..' % currversion
name_plug = 'TiVuStream Settings'
category = 'lululla.xml'
# plugin_path = os.path.dirname(sys.modules[__name__].__file__)
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/tvSettings'
ico_path = os.path.join(plugin_path, 'logo.png')
no_cover = os.path.join(plugin_path, 'no_coverArt.png')
res_plugin_path = os.path.join(plugin_path, 'res/')
ee2ldb = '/etc/enigma2/lamedb'
plugin_temp = os.path.join(plugin_path, 'temp')
if not os.path.exists(plugin_temp):
    try:
        os.makedirs(plugin_temp)
    except OSError as e:
        print(('Error creating directory %s:\n%s') % (plugin_temp, str(e)))
ServOldLamedb = plugin_path + '/temp/ServiceListOldLamedb'
TransOldLamedb = plugin_path + '/temp/TrasponderListOldLamedb'
TerChArch = plugin_path + '/temp/TerrestrialChannelListArchive'
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS90dlNldHRpbmdzL21haW4vaW5zdGFsbGVyLnNo'
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvdHZTZXR0aW5ncw=='
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
    ('UPDATE SATELLITES.XML'),
    ('UPDATE TERRESTRIAL.XML'),
    ('SETTINGS CIEFP'),
    ('SETTINGS CYRUS'),
    ('SETTINGS MANUTEK'),
    ('SETTINGS MORPHEUS'),
    ('SETTINGS VHANNIBAL'),
    ('SETTINGS VHANNIBAL 2')]


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
            self.l.setItemHeight(40)
            textfont = int(22)
            self.l.setFont(0, gFont('Regular', textfont))


def DListEntry(name, idx):
    res = [name]
    pngs = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/settingon.png".format('tvSettings'))
    pngs = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/settingoff.png".format('tvSettings'))
    if screenwidth.width() == 2560:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 10), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(80, 0), size=(1200, 50), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 50), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 0), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(50, 0), size=(500, 40), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
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
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('MainSetting')
        self.setTitle(_(title_plug))
        self['list'] = OneSetList([])
        self['title'] = Label(title_plug)
        self['info'] = Label('')
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self['key_yellow'] = Button()
        self['key_yellow'].hide()
        self['key_green'].hide()
        self.LcnOn = False
        if os.path.exists('/etc/enigma2/lcndb'):
            self['key_yellow'].show()
            self['key_yellow'] = Button('Lcn')
            self.LcnOn = True
        self["key_blue"] = Button()
        self['key_blue'].hide()
        self.Update = False
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'HotkeyActions',
                                     'InfobarEPGActions',
                                     'MenuActions',
                                     'ChannelSelectBaseActions',
                                     'DirectionActions'], {'ok': self.okRun,
                                                           # 'yellow': self.update_me,  # update_me,
                                                           'yellow_long': self.update_dev,
                                                           'info_long': self.update_dev,
                                                           'infolong': self.update_dev,
                                                           'showEventInfoPlugin': self.update_dev,
                                                           'green': self.okRun,
                                                           'back': self.cancel,
                                                           'cancel': self.cancel,
                                                           'red': self.cancel}, -1)
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.check_vers)
        else:
            self.timer.callback.append(self.check_vers)
        self.timer.start(500, 1)
        self.onLayoutFinish.append(self.updateMenuList)

    def check_vers(self):
        try:
            remote_version = '0.0'
            remote_changelog = ''
            req = Utils.Request(Utils.b64decoder(installer_url), headers={'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            if PY3:
                data = page.decode("utf-8")
            else:
                data = page.encode("utf-8")
            if data:
                lines = data.split("\n")
                for line in lines:
                    if line.startswith("version"):
                        remote_version = line.split("=")
                        remote_version = line.split("'")[1]
                    if line.startswith("changelog"):
                        remote_changelog = line.split("=")
                        remote_changelog = line.split("'")[1]
                        break
            self.new_version = remote_version
            self.new_changelog = remote_changelog
            if currversion < remote_version:
                self.Update = True
                # self['key_yellow'].show()
                # self['key_green'].show()
                self.session.open(MessageBox, _('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') % (self.new_version, self.new_changelog), MessageBox.TYPE_INFO, timeout=5)
            # self.update_me()
        except Exception as e:
            print('error check_vers:', e)

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") % (self.new_version, self.new_changelog), MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _("Congrats! You already have the latest version..."),  MessageBox.TYPE_INFO, timeout=4)

    def update_dev(self):
        try:
            req = Utils.Request(Utils.b64decoder(developer_url), headers={'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            data = json.loads(page)
            remote_date = data['pushed_at']
            strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
            remote_date = strp_remote_date.strftime('%Y-%m-%d')
            self.session.openWithCallback(self.install_update, MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date), MessageBox.TYPE_YESNO)
        except Exception as e:
            print('error xcons:', e)

    def install_update(self, answer=False):
        if answer:
            cmd1 = 'wget -q "--no-check-certificate" ' + Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
            self.session.open(xConsole, 'Upgrading...', cmdlist=[cmd1], finishedCallback=self.myCallback, closeOnSuccess=False)
        else:
            self.session.open(MessageBox, _("Update Aborted!"),  MessageBox.TYPE_INFO, timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

    def Lcn(self):
        setx = 0
        if self.LcnOn:
            lcn = LCN()
            lcn.read()
            if len(lcn.lcnlist) >= 1:
                lcn.writeBouquet()
                lcn.ReloadBouquets(setx)
                self.session.open(MessageBox, _('Sorting Terrestrial channels with Lcn rules Completed'),
                                  MessageBox.TYPE_INFO,
                                  timeout=5)

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
        elif sel == ('SETTINGS MANUTEK'):
            self.session.open(SettingManutek)
        elif sel == ('SETTINGS MORPHEUS'):
            self.session.open(SettingMorpheus)
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

    def terrestrial_restore2(self, answer=False):
        if answer:
            terrestrial_rest()

    def terrestrialsave(self):
        self.session.openWithCallback(self.terrestrialsave2, MessageBox, _("This operation save your Favorite channel Dtt\nto =>>/tmp/*_enigma2settingsbackup.tar.gz\nDo you really want to continue?"), MessageBox.TYPE_YESNO)

    def terrestrialsave2(self, answer=False):
        if answer:
            terrestrial()

    def okSATELLITE(self):
        self.session.openWithCallback(self.okSATELLITE2, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okSATELLITE2(self, answer=False):
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

    def okTERRESTRIAL2(self, answer=False):
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


class SettingCiefp(Screen):
    def __init__(self, session):

        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Ciefp')
        self.setTitle(self.setup_title)
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
        self['key_yellow'] = Button()
        self["key_blue"] = Button()
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
        self['title'] = Label(title_plug)
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
                    if name in self.names:
                        continue

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
        self.session.openWithCallback(self.okRun1, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun1(self, answer=False):
        if answer:
            global setx
            setx = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                if 'dtt' not in url.lower():
                    setx = 1
                    terrestrial()
                if keepiptv():
                    print('-----save iptv channels-----')

                # import requests
                # r = requests.get(url)
                # with open(dest, 'wb') as f:
                    # f.write(r.content)

                from six.moves.urllib.request import urlretrieve
                urlretrieve(url, dest)

                if os.path.exists(dest)  and '.zip' in dest:
                    fdest1 = "/tmp/unzipped"
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
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
                    self.session.openWithCallback(self.yes, xConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
                else:
                    self['info'].setText(_('Settings Not Installed (dest)...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self, call=None):
        copy_files_to_enigma2()
        ReloadBouquets(setx)


class SettingCyrus(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Cyrus')
        self.setTitle(self.setup_title)
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button()
        self["key_blue"] = Button()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.downloading = False
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['title'] = Label(title_plug)
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

                    if name in self.names:
                        continue

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
        self.session.openWithCallback(self.okRun1, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun1(self, answer=False):
        if answer:
            global setx
            setx = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                if 'dtt' not in url.lower():
                    setx = 1
                    terrestrial()
                if keepiptv():
                    print('-----save iptv channels-----')

                # import requests
                # r = requests.get(url)
                # with open(dest, 'wb') as f:
                    # f.write(r.content)

                from six.moves.urllib.request import urlretrieve
                urlretrieve(url, dest)

                if os.path.exists(dest)  and '.zip' in dest:
                    fdest1 = "/tmp/unzipped"
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
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
                    self.session.openWithCallback(self.yes, xConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
                else:
                    self['info'].setText(_('Settings Not Installed (dest)...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self, call=None):
        copy_files_to_enigma2()
        ReloadBouquets(setx)


class SettingManutek(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Manutek')
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button()
        self["key_blue"] = Button()
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
        self['title'] = Label(title_plug)
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
                name = url.replace("NemoxyzRLS_Manutek_", "").replace("_", " ").replace("%20", " ")  
                if name in self.names:
                    continue
                url = 'http://www.manutek.it/isetting/enigma2/' + url + '.zip'
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
        self.session.openWithCallback(self.okRun1, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun1(self, answer=False):
        if answer:
            global setx
            setx = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                if 'dtt' not in url.lower():
                    setx = 1
                    terrestrial()
                if keepiptv():
                    print('-----save iptv channels-----')

                # import requests
                # r = requests.get(url)
                # with open(dest, 'wb') as f:
                    # f.write(r.content)

                from six.moves.urllib.request import urlretrieve
                urlretrieve(url, dest)

                if os.path.exists(dest)  and '.zip' in dest:
                    fdest1 = "/tmp/unzipped"
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
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
                    self.session.openWithCallback(self.yes, xConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &; sleep 3"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
                else:
                    self['info'].setText(_('Settings Not Installed (dest)...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self, answer=None):
        ReloadBouquets(setx)


class SettingMorpheus(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Morpheus')
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button()
        self["key_blue"] = Button()
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
        self['title'] = Label(title_plug)
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
                    if name in self.names:
                        continue
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
        self.session.openWithCallback(self.okRun1, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun1(self, answer=False):
        if answer:
            global setx
            setx = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''
                if 'dtt' not in url.lower():
                    setx = 1
                    terrestrial()
                if keepiptv():
                    print('-----save iptv channels-----')

                # import requests
                # r = requests.get(url)
                # with open(dest, 'wb') as f:
                    # f.write(r.content)

                from six.moves.urllib.request import urlretrieve
                urlretrieve(url, dest)

                if os.path.exists(dest) and '.zip' in dest:
                    fdest1 = "/tmp/unzipped"
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
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
                    self.session.openWithCallback(self.yes, xConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
                else:
                    self['info'].setText(_('Settings Not Installed (dest)...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self, call=None):
        copy_files_to_enigma2()
        ReloadBouquets(setx)


class SettingVhan(Screen):
    def __init__(self, session):

        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Vhannibal')

        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button()
        self["key_blue"] = Button()
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
        self['title'] = Label(title_plug)
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
            data = make_request(urlsat)
            if PY3:
                data = six.ensure_str(data)
            match = re.compile('<td><a href="(.+?)">(.+?)</a></td>.*?<td>(.+?)</td>', re.DOTALL).findall(data)
            for url, name, date in match:
                name = str(name) + ' ' + date
                url = "https://www.vhannibal.net/" + url
                if name in self.names:
                    continue
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
        self.session.openWithCallback(self.okRun1, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun1(self, answer=False):
        if answer:
            global setx
            setx = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                self.namel = ''

                # import requests
                # r = requests.get(url)
                # with open(dest, 'wb') as f:
                    # f.write(r.content)

                if 'dtt' not in self.name.lower():
                    setx = 1
                    terrestrial()
                if keepiptv():
                    print('-----save iptv channels-----')
                from six.moves.urllib.request import urlretrieve
                urlretrieve(url, dest)

                if os.path.exists(dest)  and '.zip' in dest:
                    fdest1 = "/tmp/unzipped"
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
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
                    self.session.openWithCallback(self.yes, xConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &; sleep 3"], closeOnSuccess=False)
                    self['info'].setText(_('Settings Installed ...'))
                else:
                    self['info'].setText(_('Settings Not Installed (dest)...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self, call=None):
        copy_files_to_enigma2()
        ReloadBouquets(setx)


class SettingVhan2(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Setting Vhannibal')
        self.setTitle(_(title_plug))
        self.list = []
        self['list'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button()
        self["key_blue"] = Button()
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
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def downxmlpage(self):
        url = 'http://sat.alfa-tech.net/upload/settings/vhannibal/'
        data = make_request(url)
        if PY3:
            data = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            regex = '<a href="Vhannibal(.*?).zip"'
            match = re.compile(regex).findall(data)
            for url in match:
                if '.php' in url.lower():
                    continue
                name = "Vhannibal" + url
                name = name.replace('&#127381;', '').replace("%20", " ")
                if name in self.names:
                    continue
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
        self.session.openWithCallback(self.okRun1, MessageBox, _("Do you want to install?"), MessageBox.TYPE_YESNO)

    def okRun1(self, answer=False):
        if answer:
            global setx
            setx = 0
            if self.downloading is True:
                try:
                    idx = self["list"].getSelectionIndex()
                    self.name = self.names[idx]
                    url = self.urls[idx]
                    dest = "/tmp/settings.zip"

                    if 'dtt' not in url.lower():
                        setx = 1
                        terrestrial()
                    if keepiptv():
                        print('-----save iptv channels-----')

                    if url.startswith(b"https") and sslverify:
                        parsed_uri = urlparse(url)
                        domain = parsed_uri.hostname
                        sniFactory = SNIFactory(domain)
                        downloadPage(url, dest, sniFactory, timeout=5).addCallback(self.download, dest).addErrback(self.downloadError)
                    else:
                        downloadPage(url, dest).addCallback(self.download, dest).addErrback(self.downloadError)
                except Exception as e:
                    print('error: ', str(e))

    def downloadError(self, png):
        try:
            if not fileExists(png):
                self.poster_resize(no_cover)
        except Exception as e:
            print('error: ', str(e))

    def download(self, data, dest):
        try:
            if os.path.exists(dest)  and '.zip' in dest:
                self.namel = ''
                fdest1 = "/tmp/unzipped"
                fdest2 = "/etc/enigma2"
                if os.path.exists("/tmp/unzipped"):
                    os.system('rm -rf /tmp/unzipped')
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
                self.session.openWithCallback(self.yes, xConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &; sleep 3"], closeOnSuccess=False)
                self['info'].setText(_('Settings Installed ...'))
            else:
                self['info'].setText(_('Settings Not Installed ...'))

        except Exception as e:
            print('error: ', str(e))
            self['info'].setText(_('Not Installed ...'))

    def yes(self, call=None):
        copy_files_to_enigma2()
        ReloadBouquets(setx)


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
            # PluginDescriptor(name=name_plug, description=title_plug, where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=autostart),
            PluginDescriptor(name=name_plug, description=title_plug, where=PluginDescriptor.WHERE_MENU, fnc=StartSetup),
            PluginDescriptor(name=name_plug, description=title_plug, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]


def copy_files_to_enigma2():
    import shutil
    IptvChArch = plugin_path + '/temp'
    enigma2_folder = "/etc/enigma2"
    bouquet_file = os.path.join(enigma2_folder, "bouquets.tv")

    # Copia i file dalla cartella temporanea a /etc/enigma2
    for filename in os.listdir(IptvChArch):
        if filename.endswith(".tv"):
            src_path = os.path.join(IptvChArch, filename)
            dst_path = os.path.join(enigma2_folder, filename)
            shutil.copy(src_path, dst_path)

            # Aggiungi il nome del file al file bouquet.tv
            with open(bouquet_file, "r+") as f:
                line = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "{}" ORDER BY bouquet\n'.format(filename)
                if line not in f:
                    f.write(line)
    print("Operazione completata!")


# ===== by lululla

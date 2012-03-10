#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 02.03.2011 
@author: anon <index4376867067@yandex.ru>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
   
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
   
    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    MA 02110-1301, USA.
'''

'''
Create pyrc: pyrcc4 -o res_.py res_.qrc
TODO: блокирование через контенстное меню, правая кнопка на постид -> меню-блоикровать
TODO: Каждый плагин заботится сам о сохранении своих настроек

TODO: Проверка новых версий svn на гугле файл
Подсветка сових постов.
Реконнект py-chat.tk

 >>32056 Вордфильтр, удобный, с возможностью выделить слово и внести его туда. 
 Блок одним кликом, функция обрезания постов больше n длинны. 
 Возможность игнора всех символов кроме латиницы и кириллицы.
 Всплывающие окна, оповещение о смене онлайна.
 Ах да, ещё хоткеи.
 Игнор капса.
 
 Сохранить буфер сообщений чята в файл
ПРИ СБОРКЕ ПОД ВЕНДУ ЧЕРЕЗ PY2EXE заменить в ui файлах <header>QtWebKit/QWebView</header> на
<header>PyQt4.QtWebKit</header>
'''

import gc
gc.enable()

from lib.class_Config import Config

Config()

from __builtin__ import qset #@UnresolvedImport
from __builtin__ import G #@UnresolvedImport
from __builtin__ import CFG #@UnresolvedImport

import sys
import os


from lib.debug import Debug

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4 import Qt
from lib.class_plugin_core import PluginHandler
from lib.gui.class_tab_connection import TAB_Connection
from lib.gui import class_tab_connection
import res_




class Chat(QtGui.QMainWindow):
    
    tabs = []
    icon_new_message = QtGui.QIcon()
    icon_main = QtGui.QIcon()
    icon_main_message = QtGui.QIcon()
    icons_conn = []
    defTitle = None
    
    def init_vars(self):        
        if G['version'][2]:
            self.defTitle = 'PyChat %s %s DEBUG' % (G['version'][0],
                                                    G['version'][1])
        else:
            self.defTitle = 'PyChat %s %s' % (G['version'][0],
                                                    G['version'][1])
        self.originalPalette = QtGui.QApplication.palette()
		
    def __init__(self):
        if False:
            self.chat_tabs = QtGui.QTabBar
        G['chat_win'] = self
        super(Chat,self).__init__()        
        self.init_vars()    
        self.SetupUI()
        
        G['config'].Load()
        self.changeStyleByName(G['config'].valueStr('View/StyleName','Plastique'))
        self.action_ShowPopup.setVisible(False)
        self.action_ShowPopup.setChecked(bool(G['config'].settings['showpopupmsg']))
        G['plugin_o'].LoadPlugins(self)
 
        self.test_timer = QtCore.QTimer()
        self.test_timer.setInterval(1000)
        QtCore.QObject.connect(self.test_timer, QtCore.SIGNAL("timeout()"), 
                               self.titleUpdate)
        self.test_timer.start()
        G['QAPP'].installEventFilter(self)

        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        QtCore.QObject.connect(self.trayIcon, QtCore.SIGNAL(traySignal), 
                               self.traySignal)
        
        self.show()
        self.CreateTab(1)
    
    def titleUpdate(self):            
        title = self.defTitle
        tabTitle = self.chat_tabs.tabText(self.chat_tabs.currentIndex())
        title += ' - ' + tabTitle
        
        def draw_icon(count):
            pix = QtGui.QPixmap(16,16)
            pix.fill(QtCore.Qt.transparent)
            
            painter = QtGui.QPainter(pix)

            textOption = QtGui.QTextOption()
            textOption.setAlignment(QtCore.Qt.AlignHCenter)
            
            f = QtGui.QFont("System", 3,  QtCore.Qt.SolidLine)
            #f.setWeight(QtGui.QFont.Bold)
            f.setBold(True)
            painter.setFont(f);
            
            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.blue)
            painter.setPen(pen)
            painter.drawText(QtCore.QRectF( pix.rect() ), 
                             QtCore.QString(str(count)) , textOption)
            
            self.setWindowIcon(QtGui.QIcon(pix))
            G['TRAY'].setIcon(QtGui.QIcon(pix))
            G['QAPP'].setWindowIcon(QtGui.QIcon(pix))
            
            painter.end()

        if G['msg_counter'][0] != 0:
            title = 'MSG: '+str(G['msg_counter'][0]) + ' ' + title
            draw_icon(G['msg_counter'][0])

        else:
            self.setWindowIcon(self.icon_main)
            G['TRAY'].setIcon(self.icon_main)
            G['QAPP'].setWindowIcon(self.icon_main)
            
        self.setWindowTitle(title)
    
    
    def traySignal(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:   
            self.action_HideToTray.toggle()
        
    def eventFilter(self, ob, ev):        
            
        t = ev.type()
            
        if t > 100 and t < 200:
            if t in (121,):
                G['msg_counter'][0] = 0
                self.titleUpdate()
                #self.setWindowModified(False)
        return False  
      
    def SetupUI(self):
        uic.loadUi('res/main.ui',self)
        self.setToolTip("")

        self.menubar.hide()
        self.chat_tabs.tabBar().hide()
        self.icon_new_message.addPixmap(QtGui.QPixmap(':/res/Images/mail-unread-new.png'), 
                                        QtGui.QIcon.Normal, 
                                        QtGui.QIcon.Off)
        
        self.icon_main.addPixmap(QtGui.QPixmap(':/res/Images/icon_16.png'), 
                                 QtGui.QIcon.Normal, 
                                 QtGui.QIcon.Off)
        
        self.icon_main_message.addPixmap(QtGui.QPixmap(':/res/Images/icon_128_ED_message.png'), 
                                         QtGui.QIcon.Normal, 
                                         QtGui.QIcon.Off)

        self.setWindowIcon(self.icon_main)
        G['QAPP'].setWindowIcon(self.icon_main)
        #qapp.setStyleSheet(WebKitStyle.getAppStyle())
        
        self.CreateTrayIcon()
        QtGui.QApplication.setApplicationName(self.defTitle)
        self.titleUpdate()
        self.SetUpSignals()
        self.widget_Top.hide()
        
        self.action_GetGetter = QtGui.QAction(self)
        self.action_GetGetter.setText('Get...')
        self.action_GetGetter.setShortcut("Ctrl+`")
        
        def CurrentTabGet_exec():
            tab_w = self.chat_tabs.currentWidget()
            if hasattr(tab_w, 'GET'):
                tab_w.GET()

        self.action_GetGetter.triggered.connect(lambda: self.chat_tabs.currentWidget().GET())
        
        self.restoreGeometry(qset.value('View/WindowGeometry').toByteArray())
        self.action_SwitchMiniStyle.triggered.connect(lambda b: self.emit(
                                                                          QtCore.SIGNAL("SwitchMiniStyle(bool)"),b))

        self.action_App_quit.triggered.connect(self.close)

        self.addAction(self.action_App_quit)
        self.addAction(self.action_GetGetter)
        self.addAction(self.action_SwitchMiniStyle)
        
        def hide_to_tray(b):
            if b:
                self.hide()
            else:
                self.show()
                self.setFocus()
                
        self.action_HideToTray.toggled.connect(hide_to_tray)
        
        self.action_ShowPopup.setCheckable(True)
        def update_showpopupmsg(b):
            G['config'].settings['showpopupmsg'] = b
        self.action_ShowPopup.triggered.connect(update_showpopupmsg)
        self.addAction(self.action_ShowPopup)
        
        # Add to tray
        self.trayIconMenu.addAction(self.action_SwitchMiniStyle)
        self.trayIconMenu.addAction(self.action_ShowPopup)
        self.trayIconMenu.addAction(self.action_HideToTray)
        self.addAction(self.action_HideToTray)
        
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.action_App_quit)
        
        
    def CreateTrayIcon(self):
        self.trayIcon = QtGui.QSystemTrayIcon(self.icon_main, self)
        self.trayIcon.show()
        G['TRAY'] = self.trayIcon
        
        self.trayIconMenu = QtGui.QMenu(self)
                
        G['TRAY'].setContextMenu(self.trayIconMenu)
         
        
    def closeEvent(self, event):
        self.hide()
         
        c = self.chat_tabs.count()
        for x in range(0,c):
            self.chat_tabs.widget(x).OnClose(x)
        
        G['config'].Save()
        self.trayIcon.hide()
        G['QAPP'].quit()

    def GET_icons(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtCore.QUrl('http://py-chat.tk/favicon.ico')), 
                       QtGui.QIcon.Normal, 
                       QtGui.QIcon.Off)
        self.icons_conn.append(icon)
        self.setWindowIcon(icon)
                
    def changeStyleByName(self, styleName):
        
        style = QtGui.QStyleFactory.create(styleName)
        G['QAPP'].setStyle(style)
        G['config'].settings['view']['style'] = styleName
        G['config'].setValue('View/StyleName',styleName)
        #QtGui.QApplication.setPalette(self.originalPalette)
        #!QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        QtGui.QApplication.setPalette(self.originalPalette)
        #self.changePalette()  
    
    def changePalette(self):
        QtGui.QApplication.setPalette(self.originalPalette)
        
                
    def setWindowTitle(self,title):
        QtGui.QMainWindow.setWindowTitle(self,title+' [*]')

    def SetUpSignals(self): 
        self.connect(self.Button_NewTab, QtCore.SIGNAL("clicked()"), 
                     lambda: self.CreateTab() )
        self.connect(self.chat_tabs, 
                     QtCore.SIGNAL("currentChanged(int)"), 
                     self.titleUpdate )
        
        self.connect(self.chat_tabs, 
                     QtCore.SIGNAL("tabCloseRequested(int)"), 
                     self.CloseTAB )

    def CloseTAB(self,i):
        self.chat_tabs.widget(i).OnClose(i)
        self.chat_tabs.removeTab(i)
                    
    def CreateTab(self,connIndex=None,TabName='',
                  conn_par=None,
                  IsAutoConn=False):
        
        Debug().info('#open tab index %s' % (connIndex))
        tab = TAB_Connection()
        self.chat_tabs.addTab(tab, TabName)
        tab.init_TWO(connIndex,conn_par, IsAutoConn)
        #thread.start_new_thread(tab.init_TWO,(connIndex,conn_par, self, IsAutoConn))
        
        #self.tabs.append(tab)
        return tab
    
    def AddCustomTab(self,tabwidget,name=''):
        self.chat_tabs.addTab(tabwidget, name)
        tabwidget.init_TWO(self)
    

if __name__ == '__main__':
    #os.system('clear')
    #G['script_dir'] = os.path.dirname(__file__) # __file__ не работает в скомпилированном exe
    G['script_dir'] = os.path.abspath(os.path.dirname(sys.argv[0]))
    Debug().info("Change working directory to: "+G['script_dir'])
    os.chdir(G['script_dir'])
    
    G['QAPP'] =  QtGui.QApplication(sys.argv)
    
    G['QAPP'].setOrganizationName('Sakurada Software Inc.') 
    G['plugin_o'] = PluginHandler()
    G['chat_win'] = Chat()

    sys.exit(G['QAPP'].exec_())

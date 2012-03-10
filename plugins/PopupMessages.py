#-*-coding: utf-8 -*-
'''
Created on 12.03.2011
@author: anon


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
from __builtin__ import G #@UnresolvedImport
USE_PYNOTIFY = True
BuildTrayTheme = object()
import sys
import os
from lib.class_plugin_core import Plugin

if sys.platform != 'linux2': USE_PYNOTIFY = False

if USE_PYNOTIFY:
    try: 
        import pynotify
    except ImportError:
        print("Module pynotify not found")
        USE_PYNOTIFY = False

if not USE_PYNOTIFY:
    from lib.utilits import WebKitStyle
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from lib.debug import Debug
    
    class _BuildTrayTheme:

        themePath = ''
        themeHeaderCSS = ''
        themeHeader = ''
        themeContent = ''
        themeContentCSS = ''
        traytheme_path = os.path.abspath('res/style/traytheme/')
        obj_mainWin = None
        
        def __init__(self,obj_mainWin):
            self.obj_mainWin = obj_mainWin
            self.traytheme_path = os.path.abspath(G['script_dir']+'//res/style/traytheme/')
            
            theme_dir = ('msg','system','onlalert')[2]
            
            self.themeHeader = self.ReadFile(self.traytheme_path+'/'+theme_dir+'/header.html')
            self.themeHeaderCSS = self.ReadFile(self.traytheme_path+'/'+theme_dir+'/header.css')
            
            #print self.themeHeaderCSS
            
            self.themeHeaderCSS =  self.themeHeaderCSS.replace('%path%', self.traytheme_path)
            
            img = self.GetLocalPath('res/Images/mail-unread-new.png')
            self.themeContent = self.ReadFile(self.traytheme_path+'/'+theme_dir+'/content.html').replace('%avatar%',img)
            self.themeContentCSS = self.ReadFile(self.traytheme_path+'/'+theme_dir+'/content.css')
            self.themeContentCSS = self.themeContentCSS.replace('%path%', self.traytheme_path)
    
        def ReadFile(self,path):
            Debug().info('Try read: %s' % (path))
            file_h = open(path,'r')
            data = file_h.read()
            file_h.close()
            #Debug().info(data)
            return data
        
        def GetLocalPath(self,path):
            full_path = os.path.abspath(path)
            #return QtCore.QUrl().fromLocalFile(QtCore.QString(full_path)).toString()
            
            return QtCore.QUrl().fromLocalFile(full_path).toString()

    class PopUp(QtGui.QWidget):
        
        close_timeout = 5000 # 3000
        Opacity = 0.7
        main_w_obj = None
        obj_mainWin = None
        obj_parent_plugin = None
        bottom_offset = 100 # Отступ от низа 26
        
        popUp_width = 200 #280
        popUp_height = 90 #110
        popUp_def_position = (1280, 982)#942-8
        popUp_margin = 8
        
        slide_steep = 5
        slide_animation_time = 10
        
        flags = QtCore.Qt.FramelessWindowHint| QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.ToolTip #| QtCore.Qt.WA_TransparentForMouseEvents
        
        def __init__(self,parent,obj_parent_plugin,msg):
            QtGui.QWidget.__init__(self)
            self.obj_mainWin = parent
            self.obj_parent_plugin = obj_parent_plugin
            
            self.setupUi()
            self.setWindowFlags(self.windowFlags() | self.flags)

            self.installEventFilter(self)
            self.go(msg)
            
        def eventFilter(self,obj,e):
            
            if e.type() == 10:
                self.setWindowOpacity(self.Opacity)
            elif e.type() == 11:
                self.setWindowOpacity(1)
            return False
            
            
        def setupUi(self):
            #self.resize(184, 163)
            self.resize(280, 110)
            self.gridLayout = QtGui.QGridLayout(self)
            self.gridLayout.setMargin(0)
            self.gridLayout.setVerticalSpacing(0)
            self.nickLabel = QtGui.QLabel(self)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.nickLabel.sizePolicy().hasHeightForWidth())
            self.nickLabel.setSizePolicy(sizePolicy)
            self.nickLabel.setMinimumSize(QtCore.QSize(0, 24)) # 0,24
            #self.nickLabel.setText("")
            self.nickLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.gridLayout.addWidget(self.nickLabel, 0, 0, 1, 1)
            self.textBrowser = QtGui.QTextBrowser(self)
            self.textBrowser.setMouseTracking(True)
            self.textBrowser.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.textBrowser.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
            self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.textBrowser.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.textBrowser.setOpenLinks(False)
            self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
            #QtCore.QMetaObject.connectSlotsByName(self)
            #self.setStyleSheet(WebKitStyle.getStyleBaseHref())
            
        def closeEvent(self,event):
            self.hide()
            QtGui.QWidget.closeEvent(self,event)
            return
            while self in self.obj_parent_plugin.popup_list:
                if len(self.obj_parent_plugin.popup_list) == 1:
                    del self.obj_parent_plugin.popup_list[0]
              
        def __del__(self): 
            pass
            #print ("~Popup")
        
        def setCloseTimer(self): 
            self.qTimer = QtCore.QTimer()
            self.qTimer.singleShot(self.close_timeout, self.close)
        
        def SetData(self,msg):
            self.nickLabel.setStyleSheet("background-image : url(res/Images/tray_pics/header.png);\n\ncolor : white; \n");
            #self.nickLabel.setStyleSheet(BuildTrayTheme.themeHeaderCSS)
            self.nickLabel.setText(BuildTrayTheme.themeHeader.replace("%fromnick%", msg[1]))
            
            self.textBrowser.setStyleSheet(BuildTrayTheme.themeContentCSS)
            self.textBrowser.setHtml(BuildTrayTheme.themeContent.replace('%message%', msg[0]))
            
            self.textBrowser.moveCursor(QtGui.QTextCursor.Start)
            self.textBrowser.ensureCursorVisible()
            
    
            
        def go(self,msg):
            self.SetData(msg)
            #self.setWindowOpacity(self.Opacity)
            self.slide()
            
        def slide(self,style=None):
            
            if not style: # Слевого угла выезжает
                self.MoveTo_HorizontallyLeft()
                self.show()
                self.target_pos = (self.geometry().x()-self.popUp_width,self.geometry().y())
                #print 'Move to %s %s' % self.target_pos               
                self.slideHorizontallyLeft()            
                
        def slideHorizontallyLeft(self):
            current_x = self.geometry().x()
            current_y = self.geometry().y()
            x_now_move = current_x-self.slide_steep
            #def PyQt4.QtCore.QRect(1680, 850, 300, 100)
            #target PyQt4.QtCore.QRect(1280, 955, 400, 40)
            if current_x > self.target_pos[0]:
                self.move(x_now_move,current_y)
                QtCore.QTimer.singleShot(self.slide_animation_time, self.slideHorizontallyLeft)
            else:
                self.setCloseTimer()
                #print 'End %s' % (self.geometry())  
                 
        def MoveTo_HorizontallyLeft(self):
            startWidthPos = QtGui.QApplication.desktop().width()-self.popUp_width# Ширина
            startHeightPos =  QtGui.QApplication.desktop().height()-self.popUp_height-self.bottom_offset # Высота
            x = startWidthPos+self.popUp_width# Лево, Право ШИРИНА 1280
            y = startHeightPos# вверх, Вниз! ВЫСОТА 974
            #print "Start Pos PyQt4.QtCore.QRect(%s, %s, %s, %s)" % ( x, y ,self.popUp_width,self.popUp_height)
            self.setGeometry(QtCore.QRect(x, y, self.popUp_width,self.popUp_height))
            #self.Message_Text.setGeometry(QtCore.QRect(0,0, self.popUp_width,self.popUp_height))
     
class PopupMessages(Plugin):

    sound_media = None
    Name = 'Show pupup messages'
    obj_mainWin = None
    popup_list = []
    timeout = 3000
    
    def OnLoad(self,parent,P):
        
        self.obj_mainWin = parent
        G['chat_win'].action_ShowPopup.setVisible(True)
        global BuildTrayTheme
        BuildTrayTheme = _BuildTrayTheme(self.obj_mainWin)
        P.AddEventHandler('chat_message_filter_msg', self.Message)
        
        self.Message('Pupup messages plugin loaded')
        return
        '''
        import thread
        import time
        def test():
            while 1:
                time.sleep(1)
                self.Message('msg')
        #thread.start_new_thread(test, () )
        test() 
        '''
        
    def Message(self,msg):
        if G['config'].settings['showpopupmsg'] == False: return
        
        if type(msg) == str:
            msg = (str(msg),'')
        else:
            msg = (unicode(msg[0]),str(msg[1]))
            
        if not USE_PYNOTIFY:
            
            i = 0
            for win in self.popup_list:
                del self.popup_list[i]
                i += 1
            self.popup_list.append(PopUp(self.obj_mainWin,self,msg))
            '''
            for win in self.popup_list:
                if win.isHidden():
                    del self.popup_list[i]
                i += 1
            '''
        else:
            #self.notify_msg(msg[1],msg[0])
            self.notify_msg_icon(msg[1],msg[0])
            
    def notify_msg(self,title_text='Title',text='There has to be text.'):
        pynotify.init("Basics")
        n = pynotify.Notification(title_text,text)
        #n.set_timeout(self.timeout)
        n.show()
        
    def notify_msg_icon(self,title_text='Title',text='There has to be text.',icon='res/Images/mail-unread-new.png'):
        pynotify.init("Basics")
        n = pynotify.Notification(title_text,text,os.path.abspath(icon))
        n.set_timeout(self.timeout)
        n.show()
                


                
        

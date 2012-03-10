#-*-coding: utf-8 -*-
'''
Created on 07.03.2011
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
from __builtin__ import G
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4 import QtWebKit


from lib.gui.class_tab import TAB
from lib.class_ChatConnection import ChatConnection
from lib.utilits import *
from lib.debug import Debug
from lib.utilits_parser import *
import sys
from lib import utilits_parser
#from lib.class_wordFiler import WordFilter

class TAB_Connection(TAB):
    
    obj_conn = None
    obj_parent = None
        
    chat_host = None
    chat_port = None
    chat_tokenpage = None
    chat_connName = ''
    notReadMessagesCount = 0
    isConnected = False
    
    def __init__(self): super(TAB_Connection,self).__init__(self.obj_parent)
    def init_TWO(self,connIndex=None,conn_par=None, IsAutoConn=False):
        if False: 
            self.obj_parent = QtGui.QTabWidget()
            self.Message_Webkit = QtWebKit.QWebView()
            self.lineEdit_Captcha = QtGui.QLineEdit()

        self.obj_parent = G['chat_win'].chat_tabs
        self.connIndex = connIndex
        #self.setWindowTitle('dasda [*]')
        #self.setWindowModified(True)
        self.SetupUI()
        
        if connIndex != None: 
            self.Settings_Load(connIndex)
        if conn_par and False:
            if IsAutoConn:
                self.chat_host, self.chat_port, self.chat_token_page = conn_par
            else:
                self.lineEdit_Host.setText(str(conn_par[0]))
                self.lineEdit_Port.setText(str(conn_par[1]))
                self.lineEdit_Token.setText(str(conn_par[2]))
        
        #self.tab_SetIcon_Modifed()
        
        #if False:
        #    Test_text = '[20:39:39] <b>&lt;<a href="event:insert,28793"><font color="#000000">28793</font></a></b><b>&gt;</b> '
        #    self.AddText('[20:39:39] <b>&lt;<a href="event:insert,28792"><font color="#000000">28792</font></a></b><b>&gt;</b>  искра, и ты покроешь собой город <a href="http://2ip.ru">http://2ip.ru</a> AND http://rghost.ru/4698495.view')
        #    self.AddText('[20:39:39] <b>&lt;<a href="event:insert,28793"><font color="#000000">28793</font></a></b><b>&gt;</b>  <span class="reply">&gt;&gt;28792</span> искра, и ты покроешь собой город <a href="http://py-chat.tk">http://py-chat.tk</a>')
        
        #    self.AddText(Test_text+' Text \\s <a href="http://rghost.ru/4698495.png">http://rghost.ru/4698495.png</a> Text')
            
        #self.WEB_view.setUrl(QtCore.QUrl('www.google.com'))
        #self.WEB_page.mainFrame().evaluateJavaScript()
        #self.WEB_page.mainFrame().setHtml('efefasfas')
        #self.Message_Webkit.load(QtCore.QUrl('http://www.google.com.ua/'))
        if IsAutoConn: 
            self.chat_host, self.chat_port, self.chat_tokenpage = (self.lineEdit_Host.text(),self.lineEdit_Port.text(),self.lineEdit_Token.text())
            self.conn_Start()
        
    def Settings_Load(self,index):
        sett = G['config'].settings
        current_index = sett['servers'][self.connIndex]
        Debug().info('Set %s' % current_index['host'])
        self.lineEdit_Name.setText(QtGui.QApplication.translate("MainWindow",current_index['user_nick'], None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_Name.setChecked(bool(current_index['NamefagMode']))
        self.lineEdit_Host.setText(current_index['host'])
        self.lineEdit_Port.setText(str(current_index['port']))
        self.lineEdit_Token.setText(current_index['token_page'])
        self.tab_SetName(current_index['name'])
            
    def Settings_Save(self,index):
        sett = G['config'].settings
        current_index = sett['servers'][index]
        current_index['user_nick'] = unicode(self.lineEdit_Name.text()).encode('utf-8')
        current_index['NamefagMode'] = bool(self.checkBox_Name.isChecked())
        current_index['howpopupmsg'] = bool(G['chat_win'].action_ShowPopup.isChecked())
        #self.action_ShowPopup.setChecked(bool(CONF_O.settings['']))
        G['config'].Save()
        
    def SetupUI(self):
        uic.loadUi('res/tab.ui',self)
        self.WEB_page = QtWebKit.QWebPage(self.Message_Webkit)
        
        self.groupBox_ConnStat.hide()
        self.Message_Webkit.setPage(self.WEB_page)
        self.WEB_page.connect(self.WEB_page, QtCore.SIGNAL("linkClicked(QUrl)"), self.WEB_LinkClicked )
        self.WEB_page.setLinkDelegationPolicy(self.WEB_page.DelegateAllLinks)
        self.Message_Webkit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        self.connect(self.Message_Webkit, QtCore.SIGNAL('customContextMenuRequested ( const QPoint & )'), lambda p: self.Message_Webkit_MenuRequested(p,self.Message_Webkit))
        
        self.Input.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.Input, QtCore.SIGNAL('customContextMenuRequested ( const QPoint & )'), lambda p: self.Input_MenuRequested(p,self.Input))
        #QtWebKit.QWebPage().OpenImageInNewWindow
        #QtWebKit.QWebPage().OpenLink
        #QtWebKit.QWebView().
        '''
            QWebView *view = QWebView(NULL);
            view->page->setLinkDelegationPolicy(QWebPage::DelegateAllLinks);
            /* Другие значения аргумента - QWebPage::DontDelegateLinks
            и QWebPage::DelegateExternalLink. QWebPage::DelegateAllLinks
            заставляет вместо того, чтобы открывать ссылки выдавать
            сигнал linkClicked(QUrl) */
            connect(view,SIGNAL(linkClicked(QUrl)),this,SLOT(openLink(QUrl)));
        '''
        self.font_Input = QtGui.QFont()
        self.font_Input.setFamily("Droid Sans")
        self.font_Input.setPointSize(14)
        self.Input.setFont(self.font_Input)
        
        self.WEB_page.mainFrame().setHtml(WebKitStyle.Build())
        self.groupBox_OnConnected.hide()
        self.groupBox_captcha.hide()
        self.connect(self.Button_Connect, QtCore.SIGNAL("clicked()"), self.conn_Start_parr )
 
        self.connect(self.ButtonSend, QtCore.SIGNAL("clicked()"),self.SendMessage)
        self.connect(self.Button_CaptchaOK, QtCore.SIGNAL("clicked()"), self.SendCaptcha)
        self.connect(self.Button_Disconnect, QtCore.SIGNAL("clicked()"), self.conn_Stop)
        self.connect(self.ButtonClear, QtCore.SIGNAL("clicked()"), self.MessagesClear)
        
        def SwitchMiniStyle(b):
            if b:
                self.groupBox_OnConnected.hide()
                self.widget_Bottom.hide()
            else:
                if self.isConnected: self.groupBox_OnConnected.show()
                self.widget_Bottom.show()
                
        self.connect(G['chat_win'], QtCore.SIGNAL("SwitchMiniStyle(bool)"),SwitchMiniStyle)
        
        def _SetMessageLen():
            msg_len = self.Input.toPlainText().length()
            if msg_len:
                if self.checkBox_Name.isChecked():
                    msg_len += self.lineEdit_Name.text().length()
                if msg_len > 255:
                    self.ButtonSend.setText('Send (%s) Too long!!' % (msg_len))
                else:
                    self.ButtonSend.setText('Send (%s)' % (msg_len))
                
            else:
                self.ButtonSend.setText('Send')
                
        self.connect(self.Input, QtCore.SIGNAL("textChanged()"), _SetMessageLen)
        self.lineEdit_Captcha.installEventFilter(self)
        self.Input.installEventFilter(self)
        self.installEventFilter(self)  
        #self.WEB_page.installEventFilter(self)
        #self.Message_Webkit.installEventFilter(self)
        
    def InputPasteText(self,text):
        self.Input.insertPlainText(text)
                                   
    def Input_MenuRequested(self,point,obj):
        Menu = QtGui.QMenu(self)
        Menu_def = obj.createStandardContextMenu()
        
        def PasteClipboardText():
            self.InputPasteText('*>'+QtGui.QApplication.clipboard().text()+'* # ')

        i = 1
        for def_action in  Menu_def.actions():
            if i == 9: 
                    action_paste = QtGui.QAction(u'Вставить-цит.', 
                                                 self, triggered = PasteClipboardText)
                    if not qStringToStr(QtGui.QApplication.clipboard().text()): 
                        action_paste.setDisabled(True)
                    Menu.addAction(action_paste)
            Menu.addAction(def_action)
            i += 1
        Menu.exec_(self.Input.mapToGlobal(point) )
        
    def MessagesClear(self): 
        self.WEB_page.mainFrame().evaluateJavaScript("clearChat();")
                
    def Message_Webkit_MenuRequested(self,point,obj=None):
        #print  point,obj
        
        Menu = QtGui.QMenu(self)
        
        
        '''
        Menu_servers = QtGui.QMenu(Menu)
        Menu_servers.setTitle("New tab")
        
        for item in  G['config'].settings['servers']:
            i_name =  G['config'].settings['servers'][item]['name']
            t = (item, i_name)
            #'%s - %s' % (i_name,item)
            action = QtGui.QAction('%s' % (i_name), self, 
                                   triggered = lambda x=0,a=t: G['chat_win'].CreateTab(connIndex=a[0],TabName=a[1],conn_par=None, IsAutoConn=False))
            
            Menu_servers.addAction(action)
        Menu.addMenu(Menu_servers)
        '''
        
        #QtGui.QAction("New tab", self, triggered = lambda x=None: G['chat_win'].CreateTab(1)))
        
        
            
        #Menu.addAction(QtGui.QAction("Get...", self, triggered = self.GET))
        #Menu.addAction(G['chat_win'].action_GetGetter)
        #DefaultMenu.setTitle('Default actions')
        #Menu.addAction(QtGui.QAction("Test", self))
        #QtCore.QString().fromUtf8
        q_text = self.WEB_page.selectedText()
        if q_text:
            def block(post_id):
                send_result = self.obj_conn.writeSocket('@block %s' % post_id)
            text = qStringToStr(q_text)
            text_qq = '*>'+text+'* # '
            Menu.addAction(QtGui.QAction(u'Цитировать', self,triggered = lambda x=0: self.Input.insertPlainText(text_qq)))
            if hasattr(self, 'obj_conn') and self.obj_conn:
                r = re.match('([^\s]\d+)',text)
                if r:
                    t = r.group(0)
                    action_block = QtGui.QAction('@block '+t,self, triggered = lambda x=0: block(t))
                    Menu.addAction(action_block)
        
        DefaultMenu = self.WEB_page.createStandardContextMenu()
        DefActionsQList = DefaultMenu.actions()
        for def_action in DefActionsQList:
            if def_action.text() == 'Reload': continue
            Menu.addAction(def_action)
        
        self.AddMainMenuActions(Menu)
    
        Menu.exec_(self.Message_Webkit.mapToGlobal(point) )
        
    def AddMainMenuActions(self,Menu):
        
        '''
        isUrl = False
        __disable_menu = ['Open in New Window','Save Link...',
                          'Open Link'
                          'Open Image','Save Image','Copy Image',
                          'Copy Image Address']
        
        
        for item in Menu.actions():
            #print item.data().text()
            if item.text() == 'Open Link':
                #QtGui.QAction().data().text()
                
                isUrl = True
                #Menu.removeAction(item)
                #continue
            
            if item.text() in __disable_menu:
                #print item.text()
                Menu.removeAction(item)
        '''
        
        #Menu.addAction(QtGui.QAction("New tab", self, triggered = lambda x=None: G['chat_win'].CreateTab(1)))
        ##Menu_WordFilter = QtGui.QMenu(Menu)
        ##Menu_WordFilter.setTitle("Word filter")
        ##Menu_WordFilter.addAction(QtGui.QAction("Edit...", self,
        ##                             triggered = G['chat_win'].WordFilterWindow))
        ##Menu.addMenu(Menu_WordFilter)
        #Menu.addAction(QtGui.QAction("Exit", self,
        #                             triggered = G['chat_win'].close))
        Menu_View = QtGui.QMenu(Menu)
        Menu_View.setTitle("View")
        
        Menu_Style = QtGui.QMenu(Menu)
        Menu_Style.setTitle("Style")
        style_current = str(QtGui.QApplication.style().objectName())
        for style in QtGui.QStyleFactory.keys():
                #QtGui.QApplication.sty
                style = str(style)
                set_style = lambda x,s = style: G['chat_win'].changeStyleByName( s )
                style_action = QtGui.QAction(style, self, triggered = set_style )
                style_action.setCheckable(True)
                if style_current.upper() == style.upper():
                    style_action.setChecked(True)

                Menu_Style.addAction(style_action)
                del set_style
        
        Menu_View.addMenu(Menu_Style)
        Menu.addMenu(Menu_View)
        Menu.addAction(G['chat_win'].action_ShowPopup)
        #beznogo_check.toggled(False)
        #self.action_SwitchMiniStyle.triggered.connect(lambda b: self.emit(QtCore.SIGNAL("SwitchMiniStyle(bool)"),b))
        
        #self.actionApp_quit.triggered.connect(self.close)
        ##DEL#Menu.addAction(G['chat_win'].beznogo_check)
        
        Menu.addSeparator()

    def OnConnected(self):
        #self.Messages.clear()
        self.isConnected = True
        self.groupBox_captcha.hide()
        self.groupBox_Connect.hide()
        self.groupBox_OnConnected.show()
        self.groupBox_Connect.setDisabled(False)
        self.Input.setFocus()
        
    def eventFilter(self,Qobj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if Qobj == self.lineEdit_Captcha and event.key() in (QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter):
                self.SendCaptcha()
                return True
            if Qobj == self.Input and event.key() in (QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter):
                self.SendMessage()
                return True
        if Qobj == self and event.type() == 26: self.tab_OnActive()
            
        if Qobj == self.Message_Webkit and event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                print (event,event.type(),Qobj)
                point =  event.pos()
                Menu = self.WEB_page.createStandardContextMenu()
                if Menu:
                    Menu.exec_(self.Message_Webkit.mapToGlobal(point) )
                else:
                    #del Menu
                    #Menu =
                    pass 
                #return True
        return False
        
    def conn_Start_parr(self):
        self.chat_host, self.chat_port, self.chat_tokenpage = (self.lineEdit_Host.text(),self.lineEdit_Port.text(),self.lineEdit_Token.text())
        self.conn_Start()
        
    def conn_Start(self):
        self.obj_conn = ChatConnection(G['chat_win'], self)
        self.SetSignalFor(self.obj_conn)
        self.obj_conn.chat_port = int(self.chat_port)
        self.obj_conn.chat_host = str(self.chat_host)
        self.obj_conn.chat_token_page = str(self.chat_tokenpage)
        self.groupBox_Connect.setDisabled(True)
        self.obj_conn.start()
            
    def conn_Stop(self): 
        if self.obj_conn:
            self.isConnected = False
            self.obj_conn.stop()
            
    def conn_Del(self):
        Debug().debug("Thread send del SIGNAL",Debug().RED)
        self.groupBox_captcha.hide()
        self.groupBox_OnConnected.hide()
        self.groupBox_Connect.show()
        self.groupBox_Connect.setDisabled(False)
        self.Button_Disconnect.setDisabled(False)
        self.Button_Connect.setDisabled(False)

    def SetSignalFor(self,obj):
        #print 'Set signals for %s' % (obj)
        G['chat_win'].connect(obj, QtCore.SIGNAL("conn_msg_chat(QString)"),self.SIGNAL_msg_chat)
        G['chat_win'].connect(obj, QtCore.SIGNAL("conn_msg_sys(QString)"), self.SIGNAL_msg_sys)
        G['chat_win'].connect(obj, QtCore.SIGNAL("conn_msg_chat_err(QString)"), self.SIGNAL_msg_chat)
        G['chat_win'].connect(obj, QtCore.SIGNAL("conn_captcha_show(QByteArray)"), self.Captcha_View)
        G['chat_win'].connect(obj, QtCore.SIGNAL("conn_authorization_success()"), self.OnConnected)
        G['chat_win'].connect(obj, QtCore.SIGNAL("conn_del()"), self.conn_Del)
        G['chat_win'].connect(obj, QtCore.SIGNAL("conn_online_users(int)"), lambda i: self.label_Online.setText('<b>Online:&nbsp;</b> %s' % (i)) )
        G['chat_win'].connect(obj, QtCore.SIGNAL("conn_radio_stat(QString)"), lambda s: self.label_Radio.setText('<b>Radio:&nbsp;</b> %s' % (s)) )
        
    def SIGNAL_msg_chat(self,s):
        s = qStringToStr(s)
        self.AddText(s)
        if not self.tab_IsActive(): 
            self.notReadMessagesCount += 1
            self.tab_SetIcon_Modifed()
        if not G['chat_win'].isActiveWindow():
            G['msg_counter'][0] += 1
            G['chat_win'].titleUpdate()
        G['plugin_o'].Event('chat_message', s) 
        
    def SIGNAL_msg_sys(self,s):
        s = qStringToStr(s)
        self.AddText(s,False)
        if not self.tab_IsActive(): 
            self.notReadMessagesCount += 1
            self.tab_SetIcon_Modifed()
        G['plugin_o'].Event('chat_message_sys', s)
        
    def WEB_LinkClicked(self,qUrl):
        anchort_text= qUrl.toString()
        if len(anchort_text) >= 5 and anchort_text[:5] == 'event':
                event_split = anchort_text.split(",")#['event:insert', '28031']
                if event_split[0] == 'event:insert':
                    self.Input.insertPlainText('>>'+event_split[1]+' ')
                if  event_split[0] == 'event:block_user':
                    print ('Block %s' % (event_split[1]))
        else:
            if qUrl.toString()[0:1] == 'h':
                OpenUrl_in_Browser(qUrl.toString()) 
            #G['chat_win'].AddCustomTab()

    def AddText(self,Text,parse=True):        
        if parse:
            Text = qStringToStr(Text)
            result = ParsePost(Text)
            
            if isinstance(result, tuple):
                time = result[0]
                num = result[1]
                
                msg = result[2]
                msg = msg.replace(r"'",r"&#39;").replace('\\', '&#92;')
                #msg = msg.replace(r"'",r"\'")
                #msg = msg.replace('\\', '&#92;')
                msg = Parser_IN(msg)
                if msg in ('','\t','\n','\r',' '):
                    ##print ("Empty message egnored [%s]" % (msg))
                    return False
                
                if not G['chat_win'].isActiveWindow():
                    G['plugin_o'].Event('chat_message_filter_msg', (msg,self.tab_GetName()))
    
                msg = AddImagesThumb(msg, G['config'].settings['image_thumb_size'])
                Text = """<div class="replico">
                <span class="inContact">%s</span>
                <span class="inContentTime">&nbsp;[%s]</span><br>
                <div class="m_highlight"><div class="m_received">%s</div></div>
                <div id="insert"></div>
                </div>""".replace('\n', '') % ('<a href="event:insert,%s" class="msgNum" name="p_%s">%s<a/>' % (num,num,num),time,msg)
                #Debug().debug('Add: '+Text)
                self.WEB_page.mainFrame().evaluateJavaScript("appendMessage('%s')" % (Text))
                return
                
            else:
                Text = Text.replace('\n','<br />')
                Text = Text.replace('\r','<br />')
                Text = Text.replace('\\', '&#92;')
                #Text = Text.replace(r"'",r"\'")
                Text = Text.replace(r"'",r"&#39;")
        Text = QtCore.QString.fromUtf8(Text+'<br />')
        self.WEB_page.mainFrame().evaluateJavaScript("appendMessage('%s')" % (Text) )
    
    def SendMessage(self):
        #msg = self.Input.toPlainText()
        msg = unicode(self.Input.toPlainText()).encode('utf-8')
        if not msg: return

        if self.checkBox_Name.isChecked():
            name = unicode(self.lineEdit_Name.text()).encode('utf-8')
            msg = name+msg
        send_result = self.obj_conn.writeSocket(msg)
        if True:
            self.Input.clear()
            
        
    def SendCaptcha(self): 
        self.Button_CaptchaOK.setDisabled(True)
        self.lineEdit_Captcha.setDisabled(True)
        result = self.obj_conn.writeSocket(unicode(self.lineEdit_Captcha.text()).encode('utf-8'))
    
    def Captcha_View(self,img_data = None):
        G['QAPP'].alert(self,0)
        image = QtGui.QPixmap()
        image.loadFromData(img_data)
        #width = image.width()height = image.height()
        self.lineEdit_Captcha.clear()
        self.label_Captcha.setPixmap(image)
        self.label_Captcha.setEnabled(True)
        self.groupBox_captcha.show()
        self.lineEdit_Captcha.setDisabled(False)
        self.Button_CaptchaOK.setDisabled(False)
        self.lineEdit_Captcha.setFocus()
        
    def GET(self):
        if not self.obj_conn:
            MessageBox(u'Подключение не осуществлено.','Error',type=QtGui.QMessageBox.Warning)
            return
        get_win = QtGui.QDialog(self)
        uic.loadUi('res/get.ui',get_win)
        get_win.setWindowTitle(u'Get getter - '+self.tab_GetName())
        get_win.lineEdit_Post_ID.setText(str(self.obj_conn.GET_GETTER[0]) )
        get_win.TextEdit_GetText.insertPlainText(self.obj_conn.GET_GETTER[1])
        #get_win.TextEdit_GetText.insertPlainText(QtCore.QString.fromUtf8(self.obj_conn.GET_GETTER[1]))
        if get_win.exec_():
            self.obj_conn.GET_GETTER[0] = int(get_win.lineEdit_Post_ID.text())
            self.obj_conn.GET_GETTER[1] = get_win.TextEdit_GetText.toPlainText()
            self.AddText(u'<p>*GetGetter: id:%s text: %s</p>' % (int(get_win.lineEdit_Post_ID.text()),get_win.TextEdit_GetText.toPlainText()),False)
            
    def OnClose(self,i):
        self.Settings_Save(self.connIndex)
        self.conn_Stop()
        ##self.deleteLater()
        
    def tab_OnActive(self):
        self.notReadMessagesCount = 0
        self.tab_SetIcon_None()
        
    def __del__(self):
        pass
        #Debug().debug("~TAB",Debug().RED)

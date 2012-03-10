#-*-coding: utf-8 -*-
'''
Created on 03.03.2011
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
from lib.debug import Debug
from sys import platform
import re
import os
import time
from PyQt4 import QtGui
from PyQt4 import QtCore

def OpenUrl_in_Browser(url):
    #TODO: Открывать ссылку в запущенном браузере
    if platform == 'win32':
        """ps = popen("tasklist.exe","r")
        pp = ps.readlines()
        ps.close()"""
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        
    else:
        browsers = ('chromium-browser','opera','firefox')
        
        os.system("%s '%s' &" % (browsers[1],url))
    
def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        #print '%r (%r, %r) %2.2f sec' % \
        #      (method.__name__, args, kw, te-ts)
        print ('%r %2.2f sec ' % (method.__name__,te-ts))
        return result

    return timed

class _WebKitStyle():
    
    setyleDirPath = os.path.abspath('res/style/webkitstyle')+'/'
    TemplateFilePath = 'Template.html'
    '''
    font_chat_message: !!python/tuple [sans, 14]
    font_main_wondow: !!python/tuple [Droid Sans, 9]
    font_text_input: !!python/tuple [Droid Sans, 14]
    '''
    #variantPath = 'Variants/Medium.css'
    #variantPath = 'Variants/Small.css'
    #variantFilePath = 'Variants/Big.css'
    variantFilePath = 'Variants/Custom_font.css'
    
    baseStyleFilePath = 'base.css'
    mainCommon_FilePath = '../main_common.css'
    
    def getAppStyle(self,file='res/style/style/qutim.qss'):
        path_to_style = QtCore.QUrl().fromLocalFile(QtCore.QString(os.path.abspath(file))).toString()
        data_style = ReadFile(file).replace('%path%',path_to_style)
        return data_style
        
        
    def Build(self):
        templateHtml = ReadFile(self.setyleDirPath + self.TemplateFilePath)
        Data_BaseStyle = ReadFile(self.setyleDirPath + self.mainCommon_FilePath)
        Data_BaseStyle += ReadFile(self.setyleDirPath + self.baseStyleFilePath)
        
        BaseHref = self.getStyleBaseHref()
        templateHtml = templateHtml.replace('%@',BaseHref,1)
        templateHtml = templateHtml.replace('%@',Data_BaseStyle,1)
        templateHtml = templateHtml.replace('%@',self.variantFilePath,1)
        
        templateHtml = templateHtml.replace('%@','')
        #print templateHtml
        return templateHtml

    def getStyleBaseHref(self):
        #return QtCore.QUrl().fromLocalFile(QtCore.QString(self.setyleDirPath + self.TemplateFilePath)).toString()
        return QtCore.QUrl().fromLocalFile(self.setyleDirPath + 
                                           self.TemplateFilePath).toString()
    
        
class MessageBox(QtGui.QMessageBox):
    
    def __init__(self,text = "Message Here",title = 'Сообщение:',
                 type = QtGui.QMessageBox.NoIcon):
        super(QtGui.QMessageBox, self).__init__(None)
        #text = QtCore.QString.fromUtf8(str(text))
        #title = QtCore.QString.fromUtf8(str(title))
        self.setText(text)
        #self.setIcon(QtGui.QMessageBox.Information); 
        self.setIcon(type); 
        self.setWindowTitle(title)
        #self.setIcon(None)
        self.exec_()
        
def qStringToStr(s):
    if type(s) == QtCore.QString:
        try:
            if False: s = QtCore.QString()
            #s = unicode(s) #.encode('utf-8')
            #s = str(s.toUtf8()).decode('utf-8')
            s = str(s.toUtf8()).decode('utf-8')
        except Exception , err:
            Debug().err('Decode: '+str(err))
        
    #s = str(QApplication.translate("MainWindow", s, None, QApplication.UnicodeUTF8))
    
    return s
    
def ReadFile(file):
    f = open(file)
    data = f.read()
    f.close()
    return data
        

WebKitStyle = _WebKitStyle()

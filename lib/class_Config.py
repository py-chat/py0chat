#-*-coding: utf-8 -*-
'''
Created on 04.03.2011
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
import PyQt4

try:
    import traceback
    import __builtin__
    from PyQt4 import QtCore
    import sys
    import os
    import pickle
    from lib.debug import Debug
except Exception, err:
    print 'Error %s' % (err)
    traceback.print_exc()
    sys.exit(1)

class Config():
    qset = None
    settings = {} # Словарь текущих настроек
    paths = {}
    enable_debug = False
    # Global dict
    G = { 
			'version':  ['1.20.1','Alpha',True],
			'QAPP': None,
			'plugin_o': object,
			'script_dir': './',
			'chat_win': object,
			'msg_counter': [0,0]
		}



    _def_settings = {
        'skip_plugins': ['*','PopupMessages.py'],
        'image_thumb_size':(150,150),
        'admin_pass': None,
        'open_server_tabs': (2,3),
        'autoconnect': True,
        'showpopupmsg': 1,
        'servers':{
                0:{
                    'protocol_type': '0chat',
                    'name':'Test',
                   'token_page': 'http://site.ru/',
                    'host': 'site.ru',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/icon.png'
                },
                
                1:{
                    'protocol_type': '0chat',
                    'name':'0chan.ru',
                    'token_page': 'http://0chan.ru/0chat',
                    'host': '0chan.ru',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/py-chat.tk.ico'
                },
                
                2:{
                    'protocol_type': '0chat',
                    'name': 'py-chat.tk',
                    'token_page': 'http://py-chat.tk',
                    'host': 'py-chat.tk',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/0chan.ru.ico'
                },
                
                3:{
                    'protocol_type': '1chat',
                    'name': '1chan.ru',
                    'token_page': 'http://py-chat.tk',
                    'host': 'py-chat.tk',
                    'port': 1984,
                    'user_nick': '**<аноним> **',
                    'NamefagMode': False,
                    'icon_path':'res/Images/0chan.ru.ico'   
                }
            },
        'style_color': {
            'originalPalette': True,
            'MsgNumColor': '#3366ff',
        },
        'view' : {
            'style':'Plastique',#  Plastique
            'font_text_input': ('Droid Sans',14),
            'font_chat_message': ('Droid Sans',14),
            'font_main_wondow': ('Droid Sans',9),
            'MainWindow_W': 0,
            'MainWindow_H': 0
        },
        'debug': {
            'print_log_in_console':False,
        }
    }
    
    def __init__(self):
        if self.G['version'][2]: 
            self.enable_debug = True
        
        self.G['config'] = self

        self.qset = QtCore.QSettings("settings.ini", QtCore.QSettings.IniFormat)
        __builtin__.qset = self.qset
        __builtin__.G = self.G
        __builtin__.CFG = self
        
        
    ### QSettings actions
    def setValue(self,*args, **kwargs):
        return self.qset.setValue(*args, **kwargs)
        
    def value(self,*args, **kwargs):
        return self.qset.value(*args, **kwargs)
        
    def valueStr(self,*args, **kwargs):
        qv = self.qset.value(*args, **kwargs)
        
        if isinstance(qv,PyQt4.QtCore.QVariant):
            return str(qv.toPyObject())    
        return qv
    def valueInt(self,*args, **kwargs):
        qv = self.qset.value(*args, **kwargs)
        
        if isinstance(qv,PyQt4.QtCore.QVariant):
            return int(qv.toPyObject())    
        return qv
        
        
    def sync(self):
        return self.qset.sync()
    ###
    
    def Save(self,settings = None):
        Debug().info('Save config...')
        self.setValue("View/WindowGeometry", self.G['chat_win'].saveGeometry());
        self.setValue("dic", str(pickle.dumps(self.settings,0)))
        self.sync()
        
    def Load_and_Return(self):
        Debug().info('Read config...')
        qs = self.value('dic')
        
        s = qs.toPyObject()
        try:
            settings = pickle.loads(str(s))
        except Exception, err:
            self.setValue('DisablePlugins',1)
            Debug().err(err)
            Debug().warr("Произошла ошибка при загрузке конфига, будут использованны настройки по умолчанию.")
            settings = self._def_settings
        return settings

    def Load(self):
        #TODO: Если значение параметра нет в загруженном конфиге то брать дефолтное
        self.settings = self.Load_and_Return()


        

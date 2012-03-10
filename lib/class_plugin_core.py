#-*-coding: utf-8 -*-
'''
Created on 05.03.2011
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

import os
import sys
#import thread
from lib.debug import Debug
from __builtin__ import G #@UnresolvedImport
from __builtin__ import CFG #@UnresolvedImport
#from lib.utilits import *

# Базовый класс плагина
class Plugin(object):
	Name = 'undefined'
	Version = '1.0'
	Window_Main = None
	
	# Методы обратной связи
	def OnLoad(self,Window_Main,P):
		pass

	def OnCommand(self, cmd, args):
		pass

class PluginHandler(object):
	events = {}
	Plugins = [] # Экземпляры загруженных плагинов
	
	def __init__(self):
		ev = {'test':[self.Event]}
	
	def AddEventHandler(self, EventName, EventFunction):
		#Debug().info(' Add Event Hendler: %s - call %s ' % (EventName, EventFunction))
		if EventName in self.events:
			self.events[EventName].append(EventFunction)
		else:
			self.events[EventName] = [EventFunction,]
		
	def Event(self, event, argv, *args):
		if event in self.events:
			#print 'Event: %s **args: %s ' % (event,args)
			for func in self.events[event]:
				#print 'Call: %s' % (func)
				#_thread.start_new_thread(func, (argv,) )
				func(argv)
		else:
			#Debug().err('Нет события для %s' % (event))
			pass

	def LoadPlugins(self,Window_Main):
		if CFG.valueInt('DisablePlugins',1) == 1:
			Debug().info("Plugins are disabled")
			return
		#if '*' in G['config'].settings['skip_plugins']: return
		#from lib.plugin_kernel import KernelPlugin
		plugins_dir = './plugins'
		try:
			ss = os.listdir(plugins_dir) # Получаем список плагинов в /plugins
			sys.path.insert( 0, plugins_dir) # Добавляем папку плагинов в $PATH, чтобы __import__ мог их загрузить
		except Exception, err:
			Debug().err(err)
			Debug().info('Create dir "%s"' % (plugins_dir))
			os.mkdir(plugins_dir)
	
		
		for s in ss:
			if s[-3:] != '.py': continue
			#if s in G['config'].settings['skip_plugins']: continue
			Debug().info('Found plugin: %s' % (s))
			__import__(os.path.splitext(s)[ 0], None, None, ['']) # Импортируем исходник плагина
			
		#p = KernelPlugin()
		#print Plugin.__subclasses__()
		for plugin in Plugin.__subclasses__(): # так как Plugin произведен от object, мы используем __subclasses__, чтобы найти все плагины, произведенные от этого класса
			p = plugin() # Создаем экземпляр
			self.Plugins.append(p)
			Debug().info('Load Plugin: %s v%s' % (p.Name, p.Version))
			p.OnLoad(Window_Main,self) # Вызываем событие загруки этого плагина
	
		return

from distutils.core import setup
import py2exe
import sys
import os
'''
	#Usage python -OO setup.py py2exe
	
	replace 
		<header>QtWebKit/QWebView</header>
	on
		<header>PyQt4.QtWebKit</header>
	in *.ui files
'''
sys.argv.append('py2exe') 
SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(SCRIPT_DIR)
os.system("pyrcc4.exe -o res_.py res_.qrc")

setup(
    
    #windows || console
	windows = [
               {
               'script':"pychat.py",
               "icon_resources": [(1, 'icon_of_exe.ico')]
               }
    ], 
    
    options= {
		"py2exe":{
			"includes":["sip","PyQt4", "PyQt4.QtNetwork","PyQt4.QtNetwork",
				"PyQt4.QtWebKit"],
			"optimize": 2,
			'compressed':True,
			}
	}
	
    
    
    
    )

raw_input("Finish!\nPress enter...")
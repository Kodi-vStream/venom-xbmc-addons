import os
import sys
import xbmc


sLibrary = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (sLibrary)
sLibrary = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib', 'gui' ) )
sys.path.append (sLibrary)
sLibrary = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib', 'handler' ) )
sys.path.append (sLibrary)
sLibrary = xbmc.translatePath( os.path.join( os.getcwd(), 'sites' ) )
sys.path.append (sLibrary)
sLibrary = xbmc.translatePath( os.path.join( os.getcwd(), 'hosters' ) )
sys.path.append (sLibrary)


import vstream
vstream.run()
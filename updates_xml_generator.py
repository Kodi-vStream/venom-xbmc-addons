""" addons.xml generator """

import os
import md5
import hashlib


class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__( self ):
        # generate files    
        self.path = "C:/Users/Venom/Documents/github/venom-xbmc-addons/plugin.video.vstream/resources/sites/"
        self._generate_addons_file()
    
        #self._generate_md5_file()
        # notify user
        print "Finished updating addons xml and md5 files"

    def _generate_addons_file( self ):
        # sites list
        addons = os.listdir(self.path)
        hash = md5.new()
        
        # loop thru and add each addons addon.xml file
        for addon in addons:
            
            _item = os.path.join( self.path, addon )

            hash.update( open(_item).read() )
                       
        # save file
        self._save_file( hash.hexdigest(), file="updates.xml.md5" )

    def _generate_md5_file( self ):
        try:
            # create a new md5 hash
            m = md5.new( open( "addons.xml" ).read() ).hexdigest()
            # save file
            #self._save_file( m, file="addons.xml.md5" )
        except Exception, e:
            # oops
            print "An error occurred creating addons.xml.md5 file!\n%s" % ( e, )

    def _save_file( self, data, file ):
        try:
            # write data to the file
            _path = "C:/Users/Venom/Documents/github/venom-xbmc-addons/"
            _file = os.path.join(_path, file )
            open( _file, "w" ).write( data )
        except Exception, e:
            # oops
            print "na pas sauvegarder %s file!\n%s" % ( _file, e, )


if ( __name__ == "__main__" ):
    # start
    Generator()

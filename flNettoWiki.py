#!/usr/bin/env python
"""
FLNettoWiki
Converts the .log file created by the program FLNet to
Wiki source code formated for use on the BEARS-STL Wiki
Community Portal page.

FLNettoWiki is the class containing the conversion methods

theApp is the class that runs as main when this file is 
invoked stand alone.

Update History:
* Wed Sep 04 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- Update to V1.0.3
- Updates for use with GUI for easier use.
* Mon Jan 23 2017 Mike Heitmann, N0SO <n0so@arrl.net>
- Updated to V1.0.2
- Added -t. --table option - Makes a Wiki table 
- instead of a list. Also changed version history
- to this format.
* Thu Jan 19 2017 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.1 - Initial release
"""
import datetime
import argparse

TABLESTART = \
"""
{|class='wikitable' border='1'
| align="left" style="background:#f0f0f0;"|'''SEQ'''
| align="left" style="background:#f0f0f0;"|'''CALL'''
| align="left" style="background:#f0f0f0;"|'''NAME'''
| align="left" style="background:#f0f0f0;"|'''NOTES'''
|-
"""
ROWEND = '|-'
TABLEEND = "|}"


class FLNettoWiki():
    def __init__(self, flnet_file_name = None, wikitext_name = None, whichnet = None, table = False):
        if (flnet_file_name != None):
            self.appMain(flnet_file_name, wikitext_name, whichnet, table)

    def __version__(self):
        return "1.0.3"

    def readflNetfile(self, flnet_file_name):
        flnet_text = []
        if (flnet_file_name == None):
            print("FLNettoWiki: No FLNet checkins file!")
        else:
            with open(flnet_file_name, 'r') as file:
               for nextline in file:
                   flnet_text.append(nextline)
        return flnet_text

    def convert_to_wiki(self, flnet_text):
        """
        Parses the FLNet log file and converts each line to
        WikiMedia numbered list source format:
        
        1. CALLSIGN - Name <net controller>
        2. CALLSIGN - Name
        3. CALLSIGN - Name
        ...0
        N. CALLSIGN - Name
        
        """
        wikitext = []
        needControl = True

        for line in flnet_text:
            #print ('fl line = %s'%(line))
            linewords = line.split()
            #print ('linewords = %s'%(linewords))
            name = ''
            comment = ''
            call = linewords[0]
            if (len(linewords) > 1):
                name = linewords[1]
            if (needControl):
                comment = '<net control>'
                needControl = False
            wikitext.append( \
                ('# %s  %s  %s'%(call, name, comment)) )
        #print ('wikitext = %s'%(wikitext))
        return wikitext

    def convert_to_wiki_table(self, flnet_text):
        """
        
        """

        wikitext =[]
        wikitext.append(TABLESTART)
        item = 0   
        needControl = True
        for line in flnet_text:
            item += 1
            print('line = %s'%(line))
            if (needControl):
                comment = '<net control>'
                needControl = False
            else:
                comment = ''
            temp = line.split()
            print ('Raw temp = %s\nLEN = %d'%(temp,len(temp)))
            call = temp[0]
            if (len(temp) > 1):
                name = temp[1]
            else:
                name = ''
            wikitext.append( ('|%d ||%s ||%s ||%s \n|-'%(\
                                  item, \
                                  call, \
                                  name, \
                                  comment)) )
                                                        
        wikitext.append(TABLEEND)
        return wikitext
            
    def make_wiki_entry(self, text, whichnet = None):
        """
        Adds the Wiki level 3 header with date and link to the
        BEARS Sunday Night Net page to the data converted by
        convert_to_wiki:
        
        ===January 15, 2017 [http:# www.w0ma.org/net_information.htm Sunday Night 2-Meter Net]===
        <data included in parameter text>

        Call this method with data from the convert_to_wiki method
        """
        entryText =[]
        now = datetime.datetime.now()
        entryline = "===" + now.strftime("%B %d, %Y")
        if ((whichnet == None) or \
            (whichnet == "Sunday") ):
            entryline += " [http://www.w0ma.org/net_information.htm Sunday Night 2-Meter Net]===\n\n"
        elif (whichnet == "VEOC"):
            entryline += " Monthly EOC VHF Equipment Check Net===\n\n"
        elif (whichnet == "UEOC"):
            entryline += " Monthly EOC UHF Equipment Check Net===\n\n"
        entryText.append(entryline)
        #linetext = text.split('\n')
        for entryline in text:
            entryText.append(entryline)
        return entryText

    def write_wiki_text_file(self, text, wikitext_name):
        with open(wikitext_name, 'w') as f:
	    for ltext in text:
                f.write(ltext+'\n')

    def appMain(self, inputfile, outputfile, whichnet, table):
        text = self.readflNetfile(inputfile)
        print("%s" % (text))
        if (table):
           wiki = self.convert_to_wiki_table(text)
        else:
           wiki = self.convert_to_wiki(text)
        print("%s" % (wiki))
        wentry = self.make_wiki_entry(wiki, whichnet)
        print ("%s" % (wentry))
        self.write_wiki_text_file(wentry, outputfile)

       
"""
The main app class.
Only gets called if this file is running stand alone, and
not if it's included as part of a larger application
"""
class theApp():        
    def __init__(self):
        self.appMain()

    def getVersion(self):
        vapp = FLNettoWiki()
        version = '%(prog) s ' + vapp.__version__()
        return version        

    def getArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version = self.getVersion())
        parser.add_argument("-i", "--inputfile", default=None,
            help="Specifies the FLNet input file name")
        parser.add_argument("-o", "--outputfile", default=None,
            help="Specifies the output file name for resulting Wiki page source code")
        parser.add_argument("-t", "--table", default=None,
            help="Format the output as  code for a Wiki Table")
        parser.add_argument("-w", "--whichnet", default= "Sunday",
            help='''
                 Specifies the net type:
                    Sunday = Sunday Night Two Meter Net,
                    VEOC = Monthly EOC VHF Equipment Check Net,
                    UEOC = Monthly EOC UHF Equipment Check Net
                 ''')
        args = parser.parse_args()
        if ( (args.inputfile == None) or \
             (args.outputfile == None) ):
            parser.print_help()
            #parser.print_usage() # for just the usage line
            parser.exit()
        return args

    def appMain(self):
        args = self.getArgs()
        app = FLNettoWiki(args.inputfile, args.outputfile, args.whichnet, args.table)                   

"""
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   app = theApp()

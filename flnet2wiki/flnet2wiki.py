#!/usr/bin/env python
"""
FLNettoWiki

FLNettoWiki is the class containing the conversion methods
"""
import datetime

TABLESTART = \
"""
{|class='wikitable' border='1'
| align="left" style="background:#f0f0f0;"|'''SEQ'''
| align="left" style="background:#f0f0f0;"|'''CALL'''
| align="left" style="background:#f0f0f0;"|'''NAME'''
| align="left" style="background:#f0f0f0;"|'''TIME'''
| align="left" style="background:#f0f0f0;"|'''NOTES'''
|-
"""
ROWEND = '|-'
TABLEEND = "|}"


class FLNettoWiki():
    def __init__(self, flnet_file_name = None, 
                       wikitext_name = None, 
                       whichnet = None, table = False):
        if (flnet_file_name != None):
            self.appMain(flnet_file_name, wikitext_name, 
                                          whichnet, table)

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
        
    def convert_to_wiki_line(self, linewords):
        name = ''
        time = ''
        comment = ''
        lwlen = len(linewords)
        call = linewords[0]
        if (lwlen > 1):
            name = linewords[1]
        if (lwlen >2):
            time = linewords[2]
        if (lwlen >3):
            #print ('More...')
            for i in range(3,(lwlen)):
                #print('linewords[%d] =%s'%(i, linewords[i]))
                comment += ' - ' + linewords[i]
        retdict = {
            'call': call,
            'name': name,
            'time': time,
            'comment': comment
        }
        return retdict

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
            linestuff = self.convert_to_wiki_line(linewords)
            #print('linestuff = %s'%( linestuff ))
            if (needControl):
                linestuff['comment'] += ' <net control>'
                needControl = False

            wikitext.append( \
                ('# %s  %s  %s %s'%(linestuff['call'], 
                                 linestuff['name'], 
                                 linestuff['time'],
                                 linestuff['comment'])) )
        return wikitext

    def convert_to_wiki_table(self, flnet_text):
        """
        Convert data to Wiki table format.
    Table headers and format are defined
    in TABLESTART
        """
        wikitext =[]
        wikitext.append(TABLESTART)
        item = 0   
        needControl = True
        for line in flnet_text:
            item += 1
            linewords = line.split()
            #print('line = %s'%(line))
            linestuff = self.convert_to_wiki_line(linewords)
            
            if (needControl):
                linestuff['comment'] += ' <net control>'
                needControl = False
            wikitext.append( ('|%d ||%s ||%s ||%s ||%s\n|-'%(\
                                  item, \
                                  linestuff['call'], \
                                  linestuff['name'], \
                                  linestuff['time'], \
                                  linestuff['comment'])) )
                                                        
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
        for entryline in text:
            entryText.append(entryline)
        return entryText

    def write_wiki_text_file(self, text, wikitext_name):
        with open(wikitext_name, 'w') as f:
            for ltext in text:
                f.write(ltext+'\n')

    def appMain(self, inputfile, outputfile, whichnet, table):
        text = self.readflNetfile(inputfile)
        #print("%s" % (text))
        if (table):
           wiki = self.convert_to_wiki_table(text)
        else:
           wiki = self.convert_to_wiki(text)
        #print("%s" % (wiki))
        wentry = self.make_wiki_entry(wiki, whichnet)
        #print ("%s" % (wentry))
        self.write_wiki_text_file(wentry, outputfile)

"""
Main program - print module name and version 
"""
if __name__ == '__main__':
   app = FLNettoWiki()
   print ('Classname: %s Version: %s'%(app.__class__.__name__,
                                       app.__version__()))
   

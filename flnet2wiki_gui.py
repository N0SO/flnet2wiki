#!/usr/bin/env python
import sys
python_version = sys.version_info[0]
if (python_version == 2):
    from Tkinter import *
    from tkMessageBox import *
    from tkFileDialog   import askopenfilename
    from tkFileDialog   import askdirectory
    from tkFileDialog   import asksaveasfilename
else:
    from tkinter import *
    from tkinter.messagebox import showinfo
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import askdirectory
    from tkinter.filedialog import asksaveasfilename
from flNettoWiki import FLNettoWiki
import os.path

VERSION = '1.0.0'

class wikiExtentions(FLNettoWiki):
    def __init__(self):
        self.logData = None
        self.fileName = None

class wikiWin(Frame):
    def __init__(self, RUN = True):
        self.appMain(RUN)
        
    #Creation of init_window
    def client_exit(self):
        print ("Exiting...")
        exit()

    def helpmenu(self):
        print ('Help Menu...')
        
    def About(self):
        print ('About...')
        pythonversion = sys.version.splitlines()
        infotext = \
        'FLNET2WIKI_GUI - Version ' + VERSION + '\n' + \
        'Utilities to convert FLNET files to Wiki TABLE format.\n'\
        + 'Python ' + pythonversion[0]
        showinfo('FLNET2WIKI_GUI', infotext)
        
    def OpenFile(self):
        print ("Open FLLog File!")
        fileName = askopenfilename(title = "Select FLNet Logfile:",
                              filetypes=[("LOG files","*.log"),
                                         ("CSV files","*.csv"),
                                         ("Text files","*.txt"),
                                         ("All Files","*.*")])
        if os.path.isfile(fileName):
            print('File name selected: %s'%(fileName))
            self.wikistuff.fileName = fileName
            self.wikistuff.logData = self.wikistuff.readflNetfile(fileName)
            self.fillLogTextfromData(self.wikistuff.logData, self.LogText)
            self.filemenu.entryconfigure("Convert to Wiki...", state="normal")
            self.filemenu.entryconfigure("Convert to Wiki Table...", state="normal")
            #print('Raw logDate: %s'%(self.wikistuff.logData))
        
    
    def SaveWiki(self):
        print ('Convert to Wiki format...')
        temp = self.wikistuff.convert_to_wiki(self.wikistuff.logData)
        wikiText = self.wikistuff.make_wiki_entry( \
                        temp, whichnet = self.netType.get())
        self.fillLogTextfromData(wikiText, self.LogText, 
                                                clearWin=True)

    def SaveWikiTable(self):
        print ('Convert to Wiki Table format...')
        temp = self.wikistuff.convert_to_wiki_table(self.wikistuff.logData)
        #print('===>WikiText:\n%s'%(temp))
        wikiText = self.wikistuff.make_wiki_entry( \
                                temp, 
                                whichnet = self.netType.get())

        self.fillLogTextfromData(wikiText, self.LogText, 
                                                clearWin=True)

    def fillLogTextfromData(self, Data, textWindow, 
                                             clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        for line in Data:
            textWindow.insert(END, line.strip()+'\n')

    def fillLogTextfromFile(self, filename, textWindow, 
                                            clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        try: 
           with open(filename,'r') as f:
              retText = f.readlines()
           self.fillLogTextfromData(retText, textWindow, clearWin)
        except IOError:
           retText = ('Could not read file: '%(fName))
        return retText
  
    def net_options(self):
        print('Net Type %s selected...'%(self.netType.get()))

    def init_window(self):
        self.root = Tk()
        self.netType = StringVar(None, 'Sunday')
        self.S = Scrollbar(self.root)
        self.LogText = Text(self.root, height=10, width=120)
        self.S.pack(side=RIGHT, fill=Y)
        self.LogText.pack(side=LEFT, fill=Y)
        self.S.config(command=self.LogText.yview)
        self.LogText.config(yscrollcommand=self.S.set)

        self.root.title("FLNet to Wiki Conversion Utilities")
        menu = Menu(self.root)
        self.root.config(menu=menu)
        self.filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open FLNet File", 
                                        command=self.OpenFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Convert to Wiki...", 
                                        command=self.SaveWiki, 
                                              state="disabled")
        self.filemenu.add_command(label="Convert to Wiki Table...",
                      command=self.SaveWikiTable, state="disabled")
        self.filemenu.add_command(label="Exit", 
                                            command=self.root.quit)
    
        self.optionsmenu = Menu(menu)
        menu.add_cascade(label='Options', menu=self.optionsmenu)
        self.optionsmenu.add_radiobutton(label = \
                                        'Sunday Night 2M Net',
                                        variable = self.netType,
                                        value = 'Sunday',
                                        command = self.net_options)
        self.optionsmenu.add_radiobutton(label = \
                                        'EOC VHF Check Net', 
                                        variable = self.netType,
                                        value = 'VEOC',
                                        command = self.net_options)
        self.optionsmenu.add_radiobutton(label = \
                                        'EOC UHF Check Net',
                                        variable = self.netType,
                                        value = 'UEOC',
                                        command = self.net_options)
    
    
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)
        return self.root

    def appMain(self,run = True):
        if (run):
            self.wikistuff = wikiExtentions()
            win = self.init_window()
            print ('run = True')
            win.mainloop()
        else:
            print ('run = False')

if __name__ == '__main__':
      #creation of an instance
      win = wikiWin()

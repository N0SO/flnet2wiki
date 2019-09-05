#!/user/bin/env python
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory
from tkFileDialog   import asksaveasfilename
from flNettoWiki import *

VERSION = '0.0.1'

class net2wikiGUI(FLNettoWiki):
    def __init__(self, RUN = True):
        pass
    
    def OpenFile(self):
        print ('Open File...')
        
    def SaveWiki(self):
        print ('Convert to Wiki format...')
        
    def SaveWikiTable(self):
        print ('Convert to Wiki Table format...')
        

    def appMain(self,run = True):
        win = wikiWin(self)
        
        if (run):
            win.root.mainloop()
        else:
            return win
        """
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

class wikiWin(Frame):
    def __init__(self, callbacks):
    
        # parameters that you want to send through the Frame class. 
#        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
#        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def client_exit(self):
        print "Exiting..."
        exit()

    def helpmenu(self):
        print ('Help Menu...')
        
    def About(self):
        print ('About...')
        
    def init_window(self):
        self.root = Tk()
        self.S = Scrollbar(self.root)
        self.LogText = Text(self.root, height=10, width=120)
        self.S.pack(side=RIGHT, fill=Y)
        self.LogText.pack(side=LEFT, fill=Y)
        self.S.config(command=self.LogText.yview)
        self.LogText.config(yscrollcommand=self.S.set)

        self.root.title("Wiki Conversion Utilities")
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        #filemenu.add_command(label="New", command=NewFile)
        filemenu.add_command(label="Open...", command=callbacks.OpenFile)
        filemenu.add_separator()
        filemenu.add_command(label="Convert to Wiki...", command=callbacks.SaveWiki)
        filemenu.add_command(label="Convert to Wiki Table...", command=callbacks.SaveWikiTable)
        filemenu.add_command(label="Exit", command=self.root.quit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

        #self.root.mainloop()
        
        
if __name__ == '__main__':
      #root = Tk()

      #root.geometry("900x300")

      #creation of an instance
      app = wikiWin()

      #mainloop 
      #root.mainloop()     
 

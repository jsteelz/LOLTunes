import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import re
import os

from db_interface import DB
from music_player import MusicPlayer

# For buttons without implementation yet
def doNothing(*args):
    pass

# Generic class for an image label with an onclick function (e.g. play button)
class ImgLabel():
    # Change the image of the image label on the fly
    def setImg(self, img):
        image = Image.open(img)
        image = image.resize((20, 20), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(image)
        self.label.configure(image=self.icon)

        # Necessary due to tkinter bug
        self.label.image = self.icon

    def __init__(self, root, img, row, col, rowspan, colspan, callback):
        # Open image for display
        image = Image.open(img)
        image = image.resize((20, 20), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(image)

        # Create and position the label
        self.label = ttk.Label(root, image=self.icon, style="TLabel", \
        cursor="hand2")
        self.label.grid(row=row, rowspan=rowspan, columnspan=colspan,\
        column=col, padx=0, pady=0)

        # Necessary due to tkinter bug
        self.label.image = self.icon

        # Bind callbacks to label
        self.label.bind("<Button-1>", callback)

# View for the 'about' section of the application
class Info():
    def __init__(self, root):
        # Create frame for info menu
        self.frame = ttk.Frame(root.mainframe, style="TFrame")
        self.frame.grid(column=0, row=2, sticky="W")

        # Blank line
        ttk.Label(self.frame, text="   ", style="TLabel")\
        .grid(column=0, row=0, sticky="W")

        # Title
        ttk.Label(self.frame, text="about", style="TLabel")\
        .grid(column=0, row=1, sticky="W")

        # Blank line
        ttk.Label(self.frame, text="   ", style="TLabel")\
        .grid(column=0, row=2, sticky="W")

        # Short description
        ttk.Label(self.frame, text="Still better than iTunes", style="TLabel")\
        .grid(column=0, row=3, sticky="W")

        # Blank line
        ttk.Label(self.frame, text="   ", style="TLabel")\
        .grid(column=0, row=4, sticky="W")

        # Search functionality
        ttk.Label(self.frame, text="Handy search tricks:", style="TLabel")\
        .grid(column=0, row=5, sticky="W")

        ttk.Label(self.frame, text=";s | ;song", style="TLabel")\
        .grid(column=0, row=6, sticky="W")
        ttk.Label(self.frame, text="search for songs", style="TLabel")\
        .grid(column=1, row=6, sticky="W")

        ttk.Label(self.frame, text=";al | ;album", style="TLabel")\
        .grid(column=0, row=7, sticky="W")
        ttk.Label(self.frame, text="search for albums", style="TLabel")\
        .grid(column=1, row=7, sticky="W")

        ttk.Label(self.frame, text=";ar | ;artist", style="TLabel")\
        .grid(column=0, row=8, sticky="W")
        ttk.Label(self.frame, text="search for artists", style="TLabel")\
        .grid(column=1, row=8, sticky="W")

        # Blank line
        ttk.Label(self.frame, text="   ", style="TLabel")\
        .grid(column=0, row=9, sticky="W")

        # Github page
        ttk.Label(self.frame, text="github.com/jsteelz", style="TLabel")\
        .grid(column=0, row=10, sticky="W")

        # Last adjustments before display
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=0)

# Defines view for the play menu section of the app
class PlayMenu():
    # Changes the pause/play icon when button is clicked
    def pausePlay(self):
        if self.play:
            self.play = False
            self.pp.setImg("../img/play.png")
        else:
            self.play = True
            self.pp.setImg("../img/pause.png")

    def __init__(self, root):
        # Music is by definition playing on init
        self.play = True

        # Images for pause/play buttons (useful when switching between the two)
        pImg1 = Image.open("../img/pause.png")
        pImg1 = pImg1.resize((20, 20), Image.ANTIALIAS)
        self.pauseImg = ImageTk.PhotoImage(pImg1)
        pImg2 = Image.open("../img/play.png")
        pImg2 = pImg2.resize((20, 20), Image.ANTIALIAS)
        self.playImg = ImageTk.PhotoImage(pImg2)

        # Create frame for play menu
        self.frame = ttk.Frame(root.mainframe, style="TFrame")
        self.frame.grid(column=0, row=0, sticky = "W")

        # First row
        # Song name
        self.song = tk.Entry(self.frame, disabledbackground="#282C34", bd=0, \
        disabledforeground='white', selectborderwidth=0, highlightthickness=0, \
        textvariable=root.songVar, state='disabled', cursor='arrow')
        self.song.grid(row=0, columnspan=8, sticky="WE", padx=5)
        self.pp = ImgLabel(self.frame, "../img/pause.png", 0, 8, 1, 1, \
        root.pausePlay)
        ImgLabel(self.frame, "../img/ff.png", 0, 9, 1, 1, \
        lambda *args: root.musicPlayer.ffwd())
        ImgLabel(self.frame, "../img/prevTrack.png", 0, 10, 1, 1, doNothing)

        # Second row
        tk.Entry(self.frame, disabledbackground="#282C34", bd=0, \
        disabledforeground='white', selectborderwidth=0, highlightthickness=0, \
        textvariable=root.artAlbVar, state='disabled', cursor='arrow')\
        .grid(row=1, column=0, columnspan=8, sticky="WE", padx=5)

        ImgLabel(self.frame, "../img/queue.png", 1, 8, 1, 1, doNothing)
        ImgLabel(self.frame, "../img/clear_queue.png", 1, 9, 1, 1, doNothing)
        ImgLabel(self.frame, "../img/stop.png", 1, 10, 1, 1, root.stop)

        for x in range(8):
            self.frame.grid_columnconfigure(x, minsize=30)
        for x in range(8, 11):
            self.frame.grid_columnconfigure(x, minsize=30)

# Defines view for the search bar section of the app
class SearchBar():
    # Clears the default search bar text when user first clicks on it
    def clearText(self, event):
        if not self.parent.searchActivated:
            self.parent.searchQuery.set('')
            self.parent.searchActivated = True

    def __init__(self, root):
        # To ensure clearText function works
        self.parent = root

        # Create frame for search menu
        self.frame = ttk.Frame(root.mainframe, style="TFrame")
        self.frame.grid(column=0, row=1, sticky = "W")

        # Add display elements
        self.searchBar = tk.Entry(self.frame, bg="#282C34", bd=0, \
        fg='white', selectbackground="white", \
        selectborderwidth=0, selectforeground="#282C34", \
        insertbackground='white', highlightthickness=0, \
        textvariable=root.searchQuery, font='TkFixedFont')
        self.searchBar.grid(row=0, column=0, columnspan=8, sticky="WE", padx=6)

        # Clear text when user clicks on the search bar for the first time
        self.searchBar.bind("<Button-1>", self.clearText)

        # Add searchbar-adjacent buttons
        ImgLabel(self.frame, "../img/delLib.png", 0, 8, 1, 1, doNothing)
        ImgLabel(self.frame, "../img/addMusic.png", 0, 9, 1, 1, root.addMusic)
        ImgLabel(self.frame, "../img/info.png", 0, 10, 1, 1, root.toggleInfo)

        # Last adjustments before display
        for x in range(8):
            self.frame.grid_columnconfigure(x, minsize=30)
        for x in range(8, 11):
            self.frame.grid_columnconfigure(x, minsize=30)

# Defines view for displaying search results
class ResultList():
    # Adds a song on a queue
    def addQueueItem():
        # Allow only 10 search results at once
        if self.curRow == 10:
            return
        pass

    # Add an artist search result to the tree
    def addResult(self, mainText, subText1, subText2, fileList):
        # Allow only 10 search results at once
        if self.curRow == 10:
            return

        self.curRow += 1

        main = ttk.Frame(self.frame, style="TFrame")
        main.grid(row=self.curRow, column=0, columnspan=11, pady=0, sticky='W')

        mainVar = tk.StringVar()
        mainVar.set(mainText)
        mainL = tk.Entry(main, disabledbackground="#282C34", bd=0, \
        disabledforeground='white', selectborderwidth=0, highlightthickness=0, \
        textvariable=mainVar, state='disabled', cursor='arrow')
        mainL.grid(row=0, column=0, columnspan=9, sticky="WE", padx=5)
        # mainL.bind("<Double-Button-1>", lambda *args: \
        # self.root.musicPlayer.play(fileList))

        if not subText1 == None:
            sub1Var = tk.StringVar()
            if not subText2 == None:
                sub1Var.set(subText1 + ' | ' + subText2)
            else:
                sub1Var.set(subText1)
            sub1L = tk.Entry(main, disabledbackground="#282C34", bd=0, \
            disabledforeground='white', selectborderwidth=0, \
            highlightthickness=0, font=(None, 10), textvariable=sub1Var, \
            state='disabled', cursor='arrow')
            sub1L.grid(row=1, column=0, columnspan=9, sticky="WE", padx=5)

        # Buttons for the result item
        ImgLabel(main, "../img/play.png", 0, 9, 2, 1, lambda *args:\
        self.root.playList(fileList))
        ImgLabel(main, "../img/addToQueue.png", 0, 10, 2, 1, lambda *args:\
        self.root.addList(fileList))

        # Last adjustments before display
        for x in range(8):
            main.grid_columnconfigure(x, minsize=30)
        for x in range(8, 11):
            main.grid_columnconfigure(x, minsize=30)

    def __init__(self, root, prevQuery):
        # For handling
        self.root = root
        self.frame = ttk.Frame(root.mainframe, style="TFrame")
        self.frame.grid(column=0, row=2, sticky = "NSEW")

        # The last query (ie if clicked on an album and now displaying songs)
        self.prevQuery = prevQuery
        # Keeps track of the current row being added
        self.curRow = 1

        # Show back button if previous query exists
        if not self.prevQuery == None:
            ImgLabel(self.frame, "../img/prev.png", 0, 0, 1, 1, doNothing)
        ttk.Label(self.frame, text="search results", style="TLabel")\
        .grid(row=0, column=1, columnspan=9)
        # ImgLabel for close search results button
        ImgLabel(self.frame, "../img/close.png", 0, 10, 1, 1, root.resetResults)

        # Last adjustments before display
        for x in range(8):
            self.frame.grid_columnconfigure(x, minsize=30)
        for x in range(8, 11):
            self.frame.grid_columnconfigure(x, minsize=30)

# Basically acts as the controller in MVC. Views provided by above classes.
class MainApplication(tk.Frame):

    # SEARCH FUNCTIONALITY

    # Displays search results given a certain query
    def searchForQuery(self, query):
        print('Not implemented')

    # Displays the search bar view (main view)
    def displayMain(self):
        self.searchBar = SearchBar(self)

    # Parses search value and initiates search
    def parseSearch(self, *args):
        query = self.searchQuery.get()

        # Remove menu below search bar if exists
        self.clearActiveMenu()

        if len(query) > 1 and self.searchActivated:
            self.activeMenu = 'results'
            self.resultsMenu = ResultList(self, None)

            # If an album search is specified
            if query[:4].lower() == ';al ' or query[:7].lower() == ';album ':
                query = ' '.join(query.split(' ')[1:])
                if not query == '':
                    results = self.db.query('albums', ('name', 'alb_artist', \
                    'genre'), query, ('name', 'alb_artist', 'genre'))

                    for result in results:
                        self.resultsMenu.addResult(result[0], result[1], \
                        result[2], None)
            # If an artist search is specified
            elif query[:4].lower() == ';ar ' or query[:8].lower() == ';artist ':
                query = ' '.join(query.split(' ')[1:])
                if not query == '':
                    results = self.db.query('artists', ('name',), query, \
                    ('name',))

                    for result in results:
                        self.resultsMenu.addResult(result[0], None, None,\
                        None)
            # If a song search is specified
            elif query[:3].lower() == ';s ' or query[:6].lower() == ';song ':
                query = ' '.join(query.split(' ')[1:])
                if not query == '':
                    results = self.db.query('songs', ('name', 'artist', \
                    'album', 'alb_artist'), query, ('name', 'artist', 'album', \
                    'length', 'file_path'))

                    for result in results:
                        length = ''
                        min = int(result[3] / 60)
                        sec = int(result[3] % 60)
                        if sec < 10:
                            sec = '0' + str(sec)
                        else:
                            sec = str(sec)

                        if min > 60:
                            hour = str(int(min / 60))
                            if min % 60 < 10:
                                min = '0' + str(min % 60)
                            else:
                                min = str(min % 60)
                            length = hour + ':' + min + ':' + sec
                        else:
                            length = str(min) + ':' + sec

                        self.resultsMenu.addResult(result[0], \
                        result[1], result[2], [[result[4], result[0], \
                        result[1], result[2]]])
            else:
                print('brute search')


    # Shell function to remove the search results pane
    def resetResults(self, event):
        self.resetSearch()
        self.clearActiveMenu()

    # PLAY FUNCTIONALITY

    # Takes in a query and plays the music associated with it
    def playList(self, list):
        self.displayPlay(None)
        self.musicPlayer.play(list, self.playMenu)

        self.resetResults(None)

    # Takes in a query and adds it to the play queue
    def addList(self, list):
        print("Not implemented addList")

    # Function that displays the play menu
    def displayPlay(self, event):
        # If one is already displayed, remove it
        if not self.playMenu == None:
            self.playMenu.frame.grid_forget()

        self.playMenu = PlayMenu(self)

    # Controls the music output on button click of pause/play
    def pausePlay(self, event):
        self.playMenu.pausePlay()

    # Controls stop button
    def stop(self, event):
        self.musicPlayer.stop()

        # Reset search bar
        self.resetSearch()

    # ABOUT SECTION

    # Function that toggles the info menu
    def toggleInfo(self, event):
        if not self.activeMenu == 'info':
            self.resetSearch()
            self.clearActiveMenu()
            self.activeMenu = 'info'
            self.infoMenu = Info(self)
        else:
            self.clearActiveMenu()

    # GENERIC CONTROLS

    # Resets the search bar
    def resetSearch(self):
        self.parent.focus_set()
        self.searchActivated = False
        self.searchQuery.set('Search library...')

    # Clears any menu below the search bar if currently displayed
    def clearActiveMenu(self):
        if self.activeMenu == 'info':
            self.infoMenu.frame.grid_forget()
        if self.activeMenu == 'results':
            self.resultsMenu.frame.grid_forget()

        # Reset global activeMenu var
        self.activeMenu = None

    # Function that toggles the add file menu
    def addMusic(self, event):
        dir = filedialog.askdirectory()

        if not dir == '':
            self.parent.title("LOL! adding some tunes...")
            for subdir, dirs, files in os.walk(dir):
                for file in files:
                    self.db.addFile(os.path.join(subdir, file))

            self.parent.title("LOLTunes")

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Variable to hold the db interface object
        self.db = DB()

        # Variable holding the active extra menu below the search bar
        self.activeMenu = None

        # Variable holding the play menu
        self.playMenu = None

        # Variable for whether or not user has clicked on search bar
        self.searchActivated = False

        # Variable to hold search query
        self.searchQuery = tk.StringVar()
        self.searchQuery.set("Search library...")
        self.searchQuery.trace("w", self.parseSearch)

        # Variable to hold song name
        self.songVar = tk.StringVar()
        self.songVar.set("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")

        # Variable to hold artist name
        self.artAlbVar = tk.StringVar()
        self.artAlbVar.set("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")

        # Variable to hold time
        self.timeVar = tk.StringVar()
        self.timeVar.set("0:00")

        # Variable to hold total time
        self.tTimeVar = tk.StringVar()
        self.tTimeVar.set("0:00")

        # Variable to hold the music player object
        self.musicPlayer = MusicPlayer(self.songVar, self.artAlbVar, \
        self.timeVar, self.tTimeVar)

        # Configure styles
        self.style = ttk.Style(self)
        self.style.theme_use('classic')
        self.style.configure('TLabel', background='#282C34', foreground='white'\
        , font='TkFixedFont')
        # self.style.configure('Hover.TLabel', background='#808080', \
        # foreground='white') UNUSED
        self.style.configure('Small.TLabel', background='#282C34',
        foreground='white', font=(None, 10))
        self.style.configure('TFrame', background='#282C34', font='TkFixedFont')

        # Create mainframe
        self.mainframe = ttk.Frame(self, style='TFrame')
        self.mainframe.grid(column=0, row=0, sticky='NSEW')

        # Display the main pane
        self.displayMain()

# Runs the main app
if __name__ == "__main__":
    root = tk.Tk()

    # Configure root properties
    root.resizable(False, False)
    root.configure(bg='#282C34', highlightthickness=0, bd=0, padx=5, pady=5)
    root.title("LOLTunes")

    # Create application instance
    app = MainApplication(root)
    app.grid(row=0, column=0, sticky="NSEW")

    # Run the application
    root.mainloop()

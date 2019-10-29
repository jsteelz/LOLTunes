import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import main_controls as mc
import re

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
        self.frame.grid(column=0, row=2, sticky = "W")

        # Title
        ttk.Label(self.frame, text="about", style="TLabel")\
        .grid(column=0, row=0, sticky="W")

        # Short description
        ttk.Label(self.frame, text="Still better than iTunes", style="TLabel")\
        .grid(column=0, row=1, sticky="W")

        # Blank line
        ttk.Label(self.frame, text="   ", style="TLabel")\
        .grid(column=0, row=2, sticky="W")

        # Search functionality
        ttk.Label(self.frame, text="Handy search tricks:", style="TLabel")\
        .grid(column=0, row=3, sticky="W")

        ttk.Label(self.frame, text=";s | ;song", style="TLabel")\
        .grid(column=0, row=4, sticky="W")
        ttk.Label(self.frame, text="search for songs", style="TLabel")\
        .grid(column=1, row=4, sticky="W")

        ttk.Label(self.frame, text=";al | ;album", style="TLabel")\
        .grid(column=0, row=5, sticky="W")
        ttk.Label(self.frame, text="search for albums", style="TLabel")\
        .grid(column=1, row=5, sticky="W")

        ttk.Label(self.frame, text=";ar | ;artist", style="TLabel")\
        .grid(column=0, row=6, sticky="W")
        ttk.Label(self.frame, text="search for artists", style="TLabel")\
        .grid(column=1, row=6, sticky="W")

        ttk.Label(self.frame, text=";in | ;inalbum", style="TLabel")\
        .grid(column=0, row=7, sticky="W")
        ttk.Label(self.frame, text="search by album", style="TLabel")\
        .grid(column=1, row=7, sticky="W")

        ttk.Label(self.frame, text=";by", style="TLabel")\
        .grid(column=0, row=8, sticky="W")
        ttk.Label(self.frame, text="search by artist", style="TLabel")\
        .grid(column=1, row=8, sticky="W")

        ttk.Label(self.frame, text=";g | ;type", style="TLabel")\
        .grid(column=0, row=9, sticky="W")
        ttk.Label(self.frame, text="search by genre", style="TLabel")\
        .grid(column=1, row=9, sticky="W")

        # Blank line
        ttk.Label(self.frame, text="   ", style="TLabel")\
        .grid(column=0, row=10, sticky="W")

        # Github page
        ttk.Label(self.frame, text="github.com/jsteelz", style="TLabel")\
        .grid(column=0, row=11, sticky="W")

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
        self.song = ttk.Label(self.frame, text=root.songQueue[0][0],\
        style="TLabel")
        self.song.grid(row=0, columnspan=8, sticky="W", padx=5)
        self.pp = ImgLabel(self.frame, "../img/pause.png", 0, 8, 1, 1, \
        root.pausePlay)
        ImgLabel(self.frame, "../img/ff.png", 0, 9, 1, 1, doNothing)
        ImgLabel(self.frame, "../img/prevTrack.png", 0, 10, 1, 1, doNothing)

        # Second row
        ttk.Label(self.frame, text=root.songQueue[0][1], style="TLabel")\
        .grid(row=1, columnspan=4, sticky="W", padx=5)

        ttk.Label(self.frame, text=root.songQueue[0][2], style="TLabel")\
        .grid(row=1, column=4, columnspan=4, sticky="W", padx=5)

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
        textvariable=root.searchQuery)
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

        # Testing purposes only
        self.searchBar.bind("<Return>", root.displayPlay) # Use keyrelease for real search

# Defines view for displaying search results
class ResultList():
    # Add an artist search result to the tree
    def addResult(self, mainText, rightText, subText1, subText1Q,\
    subText2, subText2Q, query):
        # Allow only 10 search results at once
        if self.curRow == 10:
            return

        self.curRow += 1

        main = ttk.Frame(self.frame, style="TFrame")
        main.grid(row=self.curRow, column=0, columnspan=11, pady=0)

        # Main content
        mainL = ttk.Label(main, text=mainText, style="TLabel")
        mainL.grid(row=0, column=0, columnspan=8, sticky="W", padx=5)
        mainL.bind("<Double-Button-1>", lambda *args: \
        self.root.playQuery(query))

        sub1L = ttk.Label(main, text=subText1, style="Small.TLabel", \
        cursor="hand2")
        sub1L.grid(row=1, column=0, columnspan=4, sticky="W", padx=5)
        sub1L.bind("<Button-1>", lambda *args: \
        self.root.searchForQuery(subText1Q))

        sub2L = ttk.Label(main, text=subText2, style="Small.TLabel", \
        cursor="hand2")
        sub2L.grid(row=1, column=4, columnspan=4, sticky="W")
        sub2L.bind("<Button-1>", lambda *args: \
        self.root.searchForQuery(subText2Q))

        # Buttons for the result item
        ImgLabel(main, "../img/play.png", 0, 9, 2, 1, lambda *args:\
        self.root.playQuery(query))
        ImgLabel(main, "../img/addToQueue.png", 0, 10, 2, 1, lambda *args:\
        self.root.addQuery(query))

        # Right text (e.g. song length)
        ttk.Label(main, text=rightText, style="Small.TLabel")\
        .grid(row=0, rowspan=2, column=7, columnspan=2)

        # Last adjustments before display
        for x in range(8):
            main.grid_columnconfigure(x, minsize=30)
        for x in range(8, 11):
            main.grid_columnconfigure(x, minsize=30)

    def __init__(self, root, prevQuery):
        # For handling
        self.root = root
        self.frame = ttk.Frame(root.mainframe, style="TFrame")
        self.frame.grid(column=0, row=2, sticky = "W")

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
        ImgLabel(self.frame, "../img/close.png", 0, 10, 1, 1, root.removeResults)

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

        self.removeResults(None)
        if len(query) > 1 and self.searchActivated:
            self.activeMenu = 'results'
            self.resultsMenu = ResultList(self, None)

            if (query[0] == ';'):
                if (query[1:4] == 'al ') or (query[1:7] == 'album '):
                    print('searching for an album')
                elif (query[1:3] == 's ') or (query[1:6] == 'song '):
                    print('searching for a song')
                elif (query[1:4] == 'ar ') or (query[1:8] == 'artist '):
                    print('searching for an artist')
                elif (query[1:4] == 'in ') or (query[1:9] == 'inalbum '):
                    print('searching by album')
                elif (query[1:4] == 'by '):
                    print('searching by artist')
                elif (query[1:3] == 'g ') or (query[1:6] == 'type '):
                    print('searching by genre')
                else:
                    print('brute search')
            else:
                print('brute search')


    # Shell function to remove the search results pane
    def removeResults(self, event):
        self.clearActiveMenu()

    # PLAY FUNCTIONALITY

    # Takes in a query and plays the music associated with it
    def playQuery(self, query):
        print("Not implemented play")

    # Takes in a query and adds it to the play queue
    def addQuery(self, query):
        print("Not implemented addquery")

    # Function that displays the play menu
    def displayPlay(self, event):
        # Testing purposes only
        self.songQueue.append(('song', 'artist', 'album'))

        self.playMenu = PlayMenu(self)

    # Controls the music output on button click of pause/play
    def pausePlay(self, event):
        mc.pp()
        self.playMenu.pausePlay()

    # Controls stop button
    def stop(self, event):
        mc.stop()

        # Clear song queue
        self.songQueue = []

        # Hide play menu
        self.playMenu.frame.grid_forget()

        # Reset search bar
        self.parent.focus_set()
        self.searchActivated = False
        self.searchQuery.set('Search library...')

    # ABOUT SECTION

    # Function that toggles the info menu
    def toggleInfo(self, event):
        if not self.activeMenu == 'info':
            self.clearActiveMenu()
            self.activeMenu = 'info'
            self.infoMenu = Info(self)
        else:
            self.clearActiveMenu()

    # GENERIC CONTROLS

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
            print(dir)
            self.parent.title("LOL! adding some tunes...")
            for subdir, dirs, files in os.walk(dir):
                for file in files:
                    dbt.addFile(os.path.join(subdir, file))
            self.parent.title("LOLTunes")

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Variable holding the active extra menu below the search bar
        self.activeMenu = None

        # Variable for whether or not user has clicked on search bar
        self.searchActivated = False

        # Variable to hold search query
        self.searchQuery = tk.StringVar()
        self.searchQuery.set("Search library...")
        self.searchQuery.trace("w", self.parseSearch)

        # List to hold current song queue. Upon app bootup, always empty.
        self.songQueue = []

        # Configure styles
        self.style = ttk.Style(self)
        self.style.theme_use('classic')
        self.style.configure('TLabel', background='#282C34', foreground='white')
        # self.style.configure('Hover.TLabel', background='#808080', \
        # foreground='white') UNUSED
        self.style.configure('Small.TLabel', background='#282C34',
        foreground='white', font=("", 10,))
        self.style.configure('TFrame', background='#282C34')

        # Create mainframe
        self.mainframe = ttk.Frame(self, style='TFrame', width=330)
        self.mainframe.grid(column=0, row=0)

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
    app.pack(side="top", fill="both", expand=True)

    # Run the application
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import main_controls as mc

class Info(tk.Frame):
    def __init__(self, root):
        # Create frame for search menu
        self.frame = ttk.Frame(root.mainframe, style="TFrame")
        self.frame.grid(column=0, row=2, sticky = "W")

        # Blank line
        ttk.Label(self.frame, text="   ", style="TLabel")\
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
        .grid(column=1, row=3, sticky="W")
        ttk.Label(self.frame, text="search for songs", style="TLabel")\
        .grid(column=2, row=3, sticky="W")

        ttk.Label(self.frame, text=";al | ;album", style="TLabel")\
        .grid(column=1, row=4, sticky="W")
        ttk.Label(self.frame, text="search for albums", style="TLabel")\
        .grid(column=2, row=4, sticky="W")

        ttk.Label(self.frame, text=";ar | ;artist", style="TLabel")\
        .grid(column=1, row=5, sticky="W")
        ttk.Label(self.frame, text="search for artists", style="TLabel")\
        .grid(column=2, row=5, sticky="W")

        ttk.Label(self.frame, text=";in | ;inalbum", style="TLabel")\
        .grid(column=1, row=6, sticky="W")
        ttk.Label(self.frame, text="search by album", style="TLabel")\
        .grid(column=2, row=6, sticky="W")

        ttk.Label(self.frame, text=";by", style="TLabel")\
        .grid(column=1, row=7, sticky="W")
        ttk.Label(self.frame, text="search by artist", style="TLabel")\
        .grid(column=2, row=7, sticky="W")

        ttk.Label(self.frame, text=";g | ;type", style="TLabel")\
        .grid(column=1, row=8, sticky="W")
        ttk.Label(self.frame, text="search by genre", style="TLabel")\
        .grid(column=2, row=8, sticky="W")

        # Github page
        ttk.Label(self.frame, text="github.com/jsteelz", style="TLabel")\
        .grid(column=0, row=9, sticky="W")

        # Last adjustments before display
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=2.5)

class AddMusic(tk.Frame):
    pass

# Defines view for the play menu section of the app
class PlayMenu():
    # Changes the pause/play icon
    def pausePlay(self):
        if self.play:
            # self.pp['text'] = "PL"
            self.play = False
        else:
            # self.pp['text'] = "PA"
            self.play = True

    def __init__(self, root):
        # Music is by definition playing on init
        self.play = True

        # Create frame for play menu
        self.frame = ttk.Frame(root.mainframe, style="TFrame")
        self.frame.grid(column=0, row=0, sticky = "W")

        # First row
        self.song = ttk.Label(self.frame, text=root.songQueue[0][0],\
        style="TLabel")
        self.song.grid(row=0, columnspan=8, sticky="W")

        pauseIcon = ImageTk.PhotoImage(Image.open("../img/pause.png"))
        self.pp = ttk.Label(self.frame, image=pauseIcon, style="TLabel")
        self.pp.grid(row=0, column=8)
        self.pp.image = pauseIcon

        ttk.Label(self.frame, text="F", style="TLabel")\
        .grid(row=0, column=9)

        ttk.Label(self.frame, text="B", style="TLabel")\
        .grid(row=0, column=10)

        # Second row
        ttk.Label(self.frame, text=root.songQueue[0][1], style="TLabel")\
        .grid(row=1, columnspan=4, sticky="W")

        ttk.Label(self.frame, text=root.songQueue[0][2], style="TLabel")\
        .grid(row=1, column=4, columnspan=4, sticky="W")

        queueIcon = ImageTk.PhotoImage(Image.open("../img/queue.png"))
        self.queue = ttk.Label(self.frame, image=queueIcon, style="TLabel")
        self.queue.grid(row=1, column=8)
        self.queue.image = queueIcon

        cQueueIcon = ImageTk.PhotoImage(Image.open("../img/clear_queue.png"))
        self.cQueue = ttk.Label(self.frame, image=cQueueIcon, style="TLabel")
        self.cQueue.grid(row=1, column=9)
        self.cQueue.image = cQueueIcon

        stopIcon = ImageTk.PhotoImage(Image.open("../img/stop.png"))
        self.stop = ttk.Label(self.frame, image=stopIcon, style="TLabel")
        self.stop.grid(row=1, column=10)
        self.stop.image = stopIcon

        # Last adjustments before display
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=2.5)
        for x in range(2):
            self.frame.grid_rowconfigure(x, minsize=30)
        for x in range(8):
            self.frame.grid_columnconfigure(x, minsize=50)
        for x in range(8, 11):
            self.frame.grid_columnconfigure(x, minsize=30)

        # Attach event listeners to buttons
        self.pp.bind("<Button-1>", root.pausePlay)
        self.stop.bind("<Button-1>", root.stop)

# Defines view for the search bar section of the app
class SearchBar():
    def __init__(self, root):
        # Create frame for search menu
        self.frame = ttk.Frame(root.mainframe, style="TFrame")
        self.frame.grid(column=0, row=1, sticky = "W")

        # Add display elements
        pauseIcon = ImageTk.PhotoImage(Image.open("../img/pause.png"))
        self.delLib = ttk.Label(self.frame, image=pauseIcon, style="TLabel")
        self.delLib.grid(row=0, column=8)
        self.delLib.image = pauseIcon

        self.searchBar = tk.Entry(self.frame, bg="#282C34", bd=0, \
        fg='white', selectbackground="white", \
        selectborderwidth=0, selectforeground="#282C34", \
        insertbackground='white', highlightthickness=0, \
        textvariable=root.searchQuery)
        root.searchQuery.set("Search library...")
        self.searchBar.grid(row=0, column=0, columnspan=9, sticky="W")

        ttk.Label(self.frame, text="AM", style="TLabel")\
        .grid(row=0, column=9)

        self.info = ttk.Label(self.frame, text="?", style="TLabel")
        self.info.grid(row=0, column=10)

        # Last adjustments before display
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=2.5)
        for x in range(8):
            self.frame.grid_columnconfigure(x, minsize=50)
        for x in range(8, 11):
            self.frame.grid_columnconfigure(x, minsize=30)

        # Attach the event listeners
        self.searchBar.bind("<Button-1>", root.clear_text)
        self.info.bind("<Button-1>", root.toggle_info)

        # Testing purposes only
        self.searchBar.bind("<Return>", root.displayPlay) # Use keyrelease for real search

class SearchResults(tk.Frame):
    pass

# Basically acts as the controller in MVC. Views provided by subclasses
class MainApplication(tk.Frame):
    # Clears the menu below the search bar if any is displayed
    def clearActiveMenu(self):
        if self.activeMenu == 'info':
            self.infoMenu.frame.grid_forget()
        # Further cases here as other views are built

        # Reset global activeMenu var
        self.activeMenu = None

    # Function that toggles the information display
    def toggle_info(self, event):
        if not self.activeMenu == 'info':
            self.clearActiveMenu()
            self.infoMenu = Info(self)
            self.activeMenu = 'info'
        else:
            self.clearActiveMenu()


    # Function that toggles the play menu
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
        self.songQueue = []
        self.playMenu.frame.grid_forget()

    # Clears default text from search bar
    def clear_text(self, event):
        if self.searchQuery.get() == "Search library...":
            event.widget.delete(0, "end")

    # Displays the search bar view (main view)
    def displayMain(self):
        self.searchBar = SearchBar(self)

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Variable holding the active extra menu below the search bar
        self.activeMenu = None

        # Variable to hold search query
        self.searchQuery = tk.StringVar()

        # List to hold current song queue. Upon app bootup, always empty.
        self.songQueue = []

        # Configure styles
        self.style = ttk.Style(self)
        self.style.theme_use('classic')
        self.style.configure('TLabel', background='#282C34', foreground='white')
        self.style.configure('TFrame', background='#282C34')

        # Create mainframe
        self.mainframe = ttk.Frame(self, style='TFrame')
        self.mainframe.grid(column=0, row=0)

        # Display the main panes
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

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import main_controls as mc

class Settings(tk.Frame):
    pass

class About(tk.Frame):
    pass

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
        self.artist = ttk.Label(self.frame, text=root.songQueue[0][0],\
        style="TLabel")
        self.artist.grid(row=0, columnspan=8, sticky="W")

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
            self.frame.grid_columnconfigure(x, minsize=40)
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

        ttk.Label(self.frame, text="AM", style="TLabel")\
        .grid(row=0, column=9)

        ttk.Label(self.frame, text="?", style="TLabel")\
        .grid(row=0, column=10)

        self.searchBar = tk.Entry(self.frame, bg="#282C34", bd=0, \
        fg='white', selectbackground="white", \
        selectborderwidth=0, selectforeground="#282C34", \
        insertbackground='white', highlightthickness=0, \
        textvariable=root.searchQuery)
        root.searchQuery.set("Search library...")
        self.searchBar.grid(row=0, column=0, columnspan=9, sticky="W")

        # Last adjustments before display
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=2.5)
        for x in range(8):
            self.frame.grid_columnconfigure(x, minsize=40)
        for x in range(8, 11):
            self.frame.grid_columnconfigure(x, minsize=30)

        # Attach the event listener to clear default text
        self.searchBar.bind("<Button-1>", root.clear_text)

        # Testing purposes only
        self.searchBar.bind("<KeyRelease>", root.playStarted)

class SearchResults(tk.Frame):
    pass

# Basically acts as the controller in MVC. Views provided by subclasses
class MainApplication(tk.Frame):
    # Function that displays the play menu on playback start
    def playStarted(self, event):
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
        self.playMenu = None

    # Clears default text from search bar
    def clear_text(self, event):
        if self.searchQuery.get() == "Search library...":
            event.widget.delete(0, "end")
        return None

    # Displays the search bar view (main view)
    def displayMain(self):
        self.searchBar = SearchBar(self)

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

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

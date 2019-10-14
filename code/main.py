import tkinter as tk
from tkinter import ttk
import main_controls as mc

class Settings(tk.Frame):
    pass

class About(tk.Frame):
    pass

class AddMusic(tk.Frame):
    pass

# Defines view for the play menu section of the app
class PlayMenu(tk.Frame):
    # Changes the pause/play icon
    def pausePlay(self):
        if self.play:
            self.pp['text'] = "PL"
            self.play = False
        else:
            self.pp['text'] = "PA"
            self.play = True

    def __init__(self, root):
        # Music is by definition playing on init
        self.play = True

        # First row
        self.artist = ttk.Label(root.mainframe, text=root.songQueue[0][0],\
        style="TLabel")
        self.artist.grid(row=0, columnspan=8, sticky="W")
        self.pp = ttk.Label(root.mainframe, text="PA", style="TLabel")
        self.pp.grid(row=0, column=8)
        ttk.Label(root.mainframe, text="F", style="TLabel")\
        .grid(row=0, column=9)
        ttk.Label(root.mainframe, text="B", style="TLabel")\
        .grid(row=0, column=10)

        # Second row
        ttk.Label(root.mainframe, text=root.songQueue[0][1], style="TLabel")\
        .grid(row=1, columnspan=4, sticky="W")
        ttk.Label(root.mainframe, text=root.songQueue[0][2], style="TLabel")\
        .grid(row=1, column=4, columnspan=4, sticky="W")
        ttk.Label(root.mainframe, text="Q", style="TLabel")\
        .grid(row=1, column=8)
        ttk.Label(root.mainframe, text="C", style="TLabel")\
        .grid(row=1, column=9)
        self.stop = ttk.Label(root.mainframe, text="S", style="TLabel")
        self.stop.grid(row=1, column=10)

        # Last adjustments before display
        for x in range(3):
            root.mainframe.grid_rowconfigure(x, minsize=30)
        for child in root.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Attach event listeners to buttons
        self.pp.bind("<Button-1>", root.pausePlay)
        self.stop.bind("<Button-1>", root.stop)

# Defines view for the search bar section of the app
class SearchBar(tk.Frame):
    def __init__(self, root):
        ttk.Label(root.mainframe, text="DL", style="TLabel")\
        .grid(row=2, column=8)
        ttk.Label(root.mainframe, text="AM", style="TLabel")\
        .grid(row=2, column=9)
        ttk.Label(root.mainframe, text="?", style="TLabel")\
        .grid(row=2, column=10)
        self.searchBar = tk.Entry(root.mainframe, bg="#282C34", bd=0, \
        fg='white', selectbackground="white", \
        selectborderwidth=0, selectforeground="#282C34", \
        insertbackground='white', highlightthickness=0, \
        textvariable=root.searchQuery)
        root.searchQuery.set("Search library...")
        self.searchBar.grid(row=2, column=0, columnspan=9, sticky="W")

        # Last adjustments before display
        for child in root.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        for x in range(8):
            root.mainframe.grid_columnconfigure(x, minsize=40)
        for x in range(8, 11):
            root.mainframe.grid_columnconfigure(x, minsize=25)

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

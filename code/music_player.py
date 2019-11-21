import vlc

class MusicPlayer():
    # Play a list of songs, replacing queue
    def play(self, toPlay, menu):
        # Set play menu
        self.playMenu = menu

        # Stop current music
        self.stop()

        # Check that queue is non-empty
        if len(toPlay) > 0:
            # Replace queue
            self.queue = toPlay
            self.queueIndex = 0

            # Change play menu text fields
            self.songVar.set(self.queue[self.queueIndex][1])
            self.artAlbVar.set(self.queue[self.queueIndex][2] + ' | ' + \
            self.queue[self.queueIndex][3])

            # Play first song in queue
            self.player = vlc.MediaPlayer(self.queue[self.queueIndex][0])
            self.player.play()

    # Play/pause
    def pp(self):
        if not self.player == None:
            self.player.pause()

    # Fast forward
    def ffwd(self):
        if not self.player == None:
            self.player.stop()

            try:
                queueIndex += 1
                self.player = vlc.MediaPlayer(self.queue[self.queueIndex][0])

                self.songVar.set(self.queue[self.queueIndex][1])
                self.artAlbVar.set(self.queue[self.queueIndex][2] + ' | ' + \
                self.queue[self.queueIndex][3])

                self.player.play()
            except:
                self.stop()

    # Previous track
    def prev(self):
        if not self.player == None:
            if self.player.get_time() > 2000:
                self.player.stop()
                self.player.play()
            else:
                try:
                    queueIndex -= 1
                    self.player = vlc.MediaPlayer(self.queue[self.queueIndex][0])
                    self.player.play()
                except:
                    self.player.stop()
                    self.player.play()

    # Clear queue
    def clear(self):
        if not self.player == None:
            self.player.stop()
            self.player = None

        self.queue = []

    # Stop
    def stop(self):
        if not self.player == None:
            self.player.stop()

            self.songVar.set("")
            self.artAlbVar.set("")

            self.playMenu.frame.grid_forget()

    # Add a list of songs to queue
    def addToQueue(self, toAdd):
        self.queue += toAdd

    def __init__(self, songVar, artAlbVar, timeVar, tTimeVar):
        # String variables containing song information on in player GUI
        self.songVar = songVar
        self.artAlbVar = artAlbVar
        self.timeVar = timeVar
        self.tTimeVar = tTimeVar

        # Variable to hold vlc mediaplayer
        self.player = None

        # Variable to hold GUI play menu
        self.playMenu = None

        # List of file paths containing music to play
        self.queue = []

        # Song being currently played in the queue (-1 for empty queue)
        self.queueIndex = -1

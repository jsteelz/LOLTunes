import main_controls as mc
from mutagen.easyid3 import EasyID3
import mutagen

def testAddMusic():
    # # m4a tests
    # mc.addMusic('/Users/JMS2921/Music/iTunes/iTunes Media/Music/Bill Evans/Explorations/')
    # mc.addMusic('/Users/JMS2921/Music/iTunes/iTunes Media/Music/Supertramp/Breakfast in America/')
    #
    # mp3 tests
    mc.addMusic("/Users/JMS2921/Music/iTunes/iTunes Media/Music/Thom Yorke/Tomorrow's Modern Boxes/")

    # DROPS A BOMB
    # mc.addMusic("/Users/JMS2921/Music/iTunes/iTunes Media/Music/")

    # mc.addMusic("/Users/JMS2921/Downloads/")

# testAddMusic()
# print(EasyID3.valid_keys.keys())
# song = EasyID3("/Users/JMS2921/Music/iTunes/iTunes Media/Music/Thom Yorke/Tomorrow's Modern Boxes/07 Pink Section.mp3")
#
# print(song['title'], song['artist'], song['albumartist'], song['album'],\
# song['genre'], song['date'])

# song = mutagen.File("/Users/JMS2921/Music/iTunes/iTunes Media/Music/D'Angelo/Voodoo/08 The Root.mp3")
# song = mutagen.File("/Users/JMS2921/Music/iTunes/iTunes Media/Music/Thom Yorke/Tomorrow's Modern Boxes/07 Pink Section.mp3")
# song = mutagen.File("/Users/JMS2921/Music/iTunes/iTunes Media/Music/Tom Misch/Beat Tape 2/07 Come Back.mp3")
# keys = song.keys()

# for key in keys:
#     print(key, song[key], '\n')

# The id3 format is a complicated joke that exists to make my life difficult

testAddMusic()

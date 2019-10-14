import sqlite3
from sqlite3 import Error
import os
import mutagen

# SQL commands to create tables
CREATE_GENRES = """CREATE TABLE IF NOT EXISTS genres (
                            name text PRIMARY KEY
                );"""

CREATE_ARTISTS = """CREATE TABLE IF NOT EXISTS artists (
                            name text PRIMARY KEY
                 );"""

CREATE_ALBUMS = """CREATE TABLE IF NOT EXISTS albums (
                            name text NOT NULL,
                            alb_artist text,
                            genre text,
                            FOREIGN KEY (alb_artist) REFERENCES artists (name),
                            FOREIGN KEY (genre) REFERENCES genre (name),
                            PRIMARY KEY (name, alb_artist)
                );"""

CREATE_SONGS = """CREATE TABLE IF NOT EXISTS songs (
                            file_path text PRIMARY KEY,
                            name text NOT NULL,
                            length real NOT NULL,
                            track_num integer,
                            year int,
                            artist text,
                            album text,
                            alb_artist text,
                            FOREIGN KEY (artist) REFERENCES artists (name),
                            FOREIGN KEY (album, alb_artist) REFERENCES album(name, alb_artist)
               );"""

# Wipe database by just straight up removing the .db file
def wipeDB(db_file):
    os.remove(db_file)

# Connect to the database file
def getConn(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

# Add the music information tables to the database
def createTables(conn):
    try:
        c = conn.cursor()
        c.execute(CREATE_GENRES)
        c.execute(CREATE_ARTISTS)
        c.execute(CREATE_ALBUMS)
        c.execute(CREATE_SONGS)
    except Error as e:
        print(e)

# Get the information from a song file
def getInfo(path, ext):
    try:
        song = mutagen.File(path)
    except mutagen.mp4.MP4StreamInfoError:
        print(path + ' is not a valid music file and cannot be read. \
              Press F to pay respects.')
        return None

    toReturn = {}

    if ext == '.m4a':
        extended_attrs = {'artist': '\xa9ART', 'album': '\xa9alb', \
                          'aArtist': 'aART', 'genre': '\xa9gen', \
                          'year': '\xa9day', 'track_num':  'trkn'}
        try:
            toReturn['songName'] = song['\xa9nam'][0]
            toReturn['track_len'] = song.info.length
        except KeyError:
            print('Could not get necessary song information for ' + path + \
                  '. Song not added. Press F to pay respects.')
            return None

        for attr in extended_attrs:
            try:
                if attr == 'track_num':
                    toReturn[attr] = song[extended_attrs[attr]][0][0]
                elif attr == 'year':
                    toReturn[attr] = int(song[extended_attrs[attr]][0])
                else:
                    toReturn[attr] = song[extended_attrs[attr]][0]
            except:
                print('Could not get ' + attr + ' for ' + path)
                toReturn[attr] = ''
    # The id3 format is a complicated joke that exists to make my life difficult
    elif ext == '.mp3':
        extended_attrs = {'artist': 'TPE1', 'album': 'TALB', \
                          'aArtist': 'TPE2', 'genre': 'TCON', \
                          'year': 'TDRC', 'track_num':  'TRCK'}
        try:
            # Gets the song title from id3 format
            title = ''
            for x in range(1, 4):
                try:
                    title += ' ' + str(song['TIT' + str(x)])
                except KeyError:
                    pass
            toReturn['songName'] = title[1:]
            toReturn['track_len'] = song.info.length
        except KeyError:
            print('Could not get necessary song information for ' + path + \
                  '. Song not added. Press F to pay respects.')
            return None

        for attr in extended_attrs:
            try:
                if attr == 'track_num':
                    toReturn[attr] = int(str(song[extended_attrs[attr]])\
                    .split('/')[0])
                elif attr == 'year':
                    toReturn[attr] = int(str(song[extended_attrs[attr]].text[0]\
                    ))
                elif attr in ['artist', 'aArtist', 'album']:
                    toReturn[attr] = (str(song[extended_attrs[attr]].text[0]))
                else:
                    toReturn[attr] = str(song[extended_attrs[attr]])
            except:
                print('Could not get ' + attr + ' for ' + path)
                toReturn[attr] = ''
    else:
        return None

    return toReturn

# Add a song to the database
def addEntry(conn, songInfo, path):
    c = conn.cursor()
    queryStart = "INSERT OR IGNORE INTO "

    # Add genre to database if in metadata
    if not songInfo['genre'] == '':
        genre = "genres(name) VALUES(?);"
        c.execute(queryStart + genre, (songInfo['genre'],))

    # Add artist to database if in metadata
    artist = "artists(name) VALUES(?);"
    if not songInfo['artist'] == '':
        c.execute(queryStart + artist, (songInfo['artist'],))

    # Add album artist to database if in metadata
    if not songInfo['aArtist'] == '':
        c.execute(queryStart + artist, (songInfo['aArtist'],))

    # Add album to database if in metadata
    if not songInfo['album'] == '':
        if not songInfo['genre'] == '':
            album = "albums(name, alb_artist, genre) VALUES(?,?,?);"
            c.execute(queryStart + album, (songInfo['album'],\
                      songInfo['aArtist'], songInfo['genre']))
        else:
            album = "albums(name, alb_artist) VALUES(?,?);"
            c.execute(queryStart + album, (songInfo['album'],\
                      songInfo['aArtist']))

    # Add song to database
    if not songInfo['album'] == '':
        if not songInfo['artist'] == '':
            song = "songs(name, length, track_num, year, artist, album, \
                    alb_artist, file_path) VALUES(?,?,?,?,?,?,?,?);"
            c.execute(queryStart + song, (songInfo['songName'],
                      songInfo['track_len'], songInfo['track_num'],\
                      songInfo['year'], songInfo['artist'], songInfo['album'], \
                      songInfo['aArtist'], path))
        else:
            song = "songs(name, length, track_num, year, album, alb_artist, \
                    file_path) VALUES(?,?,?,?,?,?,?);"
            c.execute(queryStart + song, (songInfo['songName'],\
                      songInfo['track_len'], songInfo['track_num'],\
                      songInfo['year'], songInfo['album'], songInfo['aArtist'],\
                      path))
    else:
        if not songInfo['artist'] == '':
            song = "songs(name, length, track_num, year, artist, file_path) \
                    VALUES(?,?,?,?,?,?)"
            c.execute(queryStart + song, (songInfo['songName'],
                      songInfo['track_len'], songInfo['track_num'],\
                      songInfo['year'], songInfo['artist'], path))
        else:
            song = "songs(name, length, track_num, year, file_path) \
                    VALUES(?,?,?,?,?)"
            c.execute(queryStart + song, (songInfo['songName'],\
                      songInfo['track_len'], songInfo['track_num'],\
                      songInfo['year'], path))

    print('Song added, updated, or maintained as such successfully.')

# Connect to database and add a music file
def addFile(path):
    dbPath = os.path.join('..', 'testdb', 'library.db')

    # Check if it is a valid file type
    fileN, fileExt = os.path.splitext(path)
    if fileExt not in ['.m4a', '.mp3', '.ogg', '.flac']:
        return

    print('\nAdding ' + path + '...')

    # Check if database tables exist
    # Assumption: tables exist iff libary.db created
    tablesExist = os.path.isfile(dbPath)

    # Connect to database file
    conn = getConn(dbPath)

    if conn is not None:
        # Create tables if they don't already exist
        if not tablesExist:
            print('Creating database tables...')
            createTables(conn)

        # Get song info
        songInfo = getInfo(path, fileExt)

        if not songInfo:
            return

        # Write song to db
        addEntry(conn, songInfo, path)

        # Commit db changes
        conn.commit()

        # Close db connection
        conn.close()
    else:
        print('Could not collect information. Database access failed.')

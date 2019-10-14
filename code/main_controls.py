import os
import db_tools as dbt

# Controls the search bar
def search(query):
    print('Not Implemented')

# Controls the play/pause button
def pp():
    print('Not Implemented')

# Controls the fast forward button
def ffwd():
    print('Not Implemented')

# Controls the previous track button
def prev():
    print('Not Implemented')

# Controls the show queue button
def showQueue():
    print('Not Implemented')

# Controls the clear queue button
def clear():
    print('Not Implemented')

# Controls the stop button
def stop():
    print('Not Implemented')

# Controls the delete library button
def deleteLibrary():
    print('Not Implemented')

# Controls the button to add music to the database
def addMusic(rootdir):
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            dbt.addFile(os.path.join(subdir, file))

# Controls the info button
def info():
    print('Not Implemented')

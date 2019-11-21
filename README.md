# LOLTunes

Ongoing project to build a simple Python-based music player. Based on Python3, VLC, and SQLite3.

### Dependencies

* Python 3
* VLC
* SQLite3

### Run it yourself

###### Open up terminal:

```bash
mkdir /path/to/your/directory
cd /path/to/your/directory
git clone this-repo
cd code
py main.py
```

###### Or make it into an app:

Follow the above steps, then:

```bash
insert code here
```

### Functionality

##### Search bar

Searching for music by default will return songs.
For more specific searches, use the following flags at the start of the search:
```
;s  | search songs
;al | search albums
;ar | search artists
```
Note that at present, the flags cannot be combined.

The search functionality tokenizes the search and searches by the following attributes:
* Song name
* Artist name
* Album artist name
* Album name
* Genre

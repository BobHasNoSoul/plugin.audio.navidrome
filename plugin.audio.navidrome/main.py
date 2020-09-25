#!/usr/bin/python
# -*- coding: utf-8 -*-

# Module: main
# Author: G.Breant
# Forked by: jeweet
# Created on: 14 January 2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import xbmcaddon
import xbmcplugin
import xbmcgui
import json
import shutil
import dateutil.parser
from datetime import datetime
"""
#### Debugging with eclipse and pydevd ####
# This part can be removed safely if you're not using the debugger.
# Don't forget to remove the dependency on script.module.pydevd from addon.xml as well in this case.
REMOTE_DBG = False

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pydevd # with the addon script.module.pydevd, only use `import pydevd`
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)
#### /Debugging with eclipse and pydevd ####
"""
# Add the /lib folder to sys
sys.path.append(xbmc.translatePath(os.path.join(xbmcaddon.Addon("plugin.audio.navidrome").getAddonInfo("path"), "lib")))

# Libsonic_extra overrides libsonic functions, TO FIX - we should get rid of this and use only libsonic
import libsonic_extra

from simpleplugin import Plugin
from simpleplugin import Addon

# Create plugin instance
plugin = Plugin()

connection = None

def popup(text, time=5000, image=None):
    title = plugin.addon.getAddonInfo('name')
    icon = plugin.addon.getAddonInfo('icon')
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (title, text,
                        time, icon))

def get_connection():
    global connection
    
    if connection is None:
        
        connected = False
        
        # Create connection
        try:
            connection = libsonic_extra.SubsonicClient(
                Addon().get_setting('subsonic_url'),
                Addon().get_setting('username', convert=False),
                Addon().get_setting('password', convert=False),
                Addon().get_setting('apiversion'),
                Addon().get_setting('insecure') == 'true',
                Addon().get_setting('legacyauth') == 'true',
                )
            connected = connection.ping()
        except:
            pass

        if connected is False:
            popup('Connection error')
            return False

    return connection

@plugin.action()
def root(params):
    
    # get connection
    connection = get_connection()
    
    if connection is False:
        return
    
    listing = []
    
    if Addon().get_setting('merge_folders') == True: 
		mediafolders = Addon().get_localized_string(30060)
		thumbnail = 'DefaultMusicArtists.png'
    else: 
		mediafolders = Addon().get_localized_string(30059)
		thumbnail = None
    
    menus = {
        'folders': {
            'name':     mediafolders, 
            'callback': 'browse_folders',
            'thumb':    thumbnail,
            'fanart':   None,
        },
        'playlists': {
            'name':     Addon().get_localized_string(30061),
            'callback': 'list_playlists',
            'thumb':    'DefaultMusicPlaylists.png',
            'fanart':   None,
        },
        'search': {
            'name':     Addon().get_localized_string(30062),
            'callback': 'search',
            'thumb':    'DefaultAddonsSearch.png',
            'fanart':   None,
        },  
    }
    # Iterate through categories
    for mid in menus:
        
        if 'thumb' in menus[mid]:
            thumb = menus[mid]['thumb']
        
        listing.append({
            'label':    menus[mid]['name'],
            'thumb':    thumb,
            'fanart':   None,
            'url':      plugin.get_url(
                            action=menus[mid]['callback'],
                            menu_id=mid
                        )
        })

    menus = {
        'albums_newest': {
            'name':     Addon().get_localized_string(30070),
            'thumb':    'DefaultMusicRecentlyAdded.png',
            'args':     {"ltype": "newest"},
            'fanart':   None,
        },
        'albums_frequent': {
            'name':     Addon().get_localized_string(30071),
            'thumb':    'DefaultMusicTop100Albums.png',
            'args':     {"ltype": "frequent"},
            'fanart':   None,
        },
        'albums_recent': {
            'name':     Addon().get_localized_string(30072),
            'thumb':   'DefaultMusicRecentlyPlayed.png',
            'args':     {"ltype": "recent"},
            'fanart':   None,
        },
        'albums_random': {
            'name':     Addon().get_localized_string(30073),
            'thumb':    'DefaultMusicAlbums.png',
            'args':     {"ltype": "random"},
            'fanart':   None,
        }
    }	
    # Iterate through albums
    for menu_id in menus:
        
        menu = menus.get(menu_id)
        
        if 'thumb' in menu:
            thumb = menu.get('thumb')

        listing.append({
            'label':    menu.get('name'),
            'thumb':    menu.get('thumb'),
            'url':      plugin.get_url(
                            action=         'list_albums',
                            page=           1,
                            query_args=     json.dumps(menu.get('args')),
                            menu_id=        menu_id
                        )
        })  
        
    menus = {
        'tracks_starred': {
            'name':             Addon().get_localized_string(30080),
            'thumb':            'DefaultMusicTop100Songs.png',
            'fanart':           None,
        },
        'tracks_random': {
            'name':             Addon().get_localized_string(30081),
            'thumb':            'DefaultMusicSongs.png',
            'fanart':           None,
        }
    }
    # Iterate through tracks
    for menu_id in menus:
        
        menu = menus.get(menu_id)
        
        if 'thumb' in menu:
            thumb = menu.get('thumb')

        listing.append({
            'label':    menu.get('name'),
            'thumb':    menu.get('thumb'),
            'url':      plugin.get_url(
                action=         'list_tracks',
                menu_id=        menu_id
            )
        })
      
    return plugin.create_listing(
        listing,
        cache_to_disk = True,
        sort_methods = None, 
        view_mode = None, 
        content = 'mixed',
    )

@plugin.action()
def browse_folders(params):
    connection = get_connection()
    
    if connection is False:
        return

    listing = []

    # Get items
    items = connection.walk_folders()

    # Iterate through items
    for item in items:
        entry = {
            'label':    item.get('name'),
            'url':      plugin.get_url(
                        action=         'browse_indexes',
                        folder_id=      item.get('id'),
                        menu_id=        params.get('menu_id')

            )
        }
        listing.append(entry)
        
    # Merge folders if setting == True or if there is only 1 media folder.
    if len(listing) == 1 or Addon().get_setting('merge_folders') == True:
        plugin.log('One single Media Folder found; do return listing from browse_indexes()...')
        return browse_indexes(params)
    else:	
        return plugin.create_listing(
        listing,
        cache_to_disk = True,
        sort_methods = None,
        view_mode = None, 
        content = 'files'        
        )
	
@plugin.action()
#@plugin.cached(cachetime) #cache (in minutes)
def browse_indexes(params):
    connection = get_connection()
    
    if connection is False:
        return

    listing = []
    
    # Get items 
    # optional folder ID
    folder_id = params.get('folder_id')
    items = connection.walk_index(folder_id)
            
    # Iterate through items
    for item in items:
        coverartsrc = 'coverArt' if 'coverArt' in item else 'id'
        if Addon().get_setting('coverart_from_server'): 
           image = connection.getCoverArtUrl(item.get(coverartsrc)) 
        else: 
           image = None
 
        entry = {
            'icon':     'DefaultArtist.png',
            'thumb':    image,
            'label':    item.get('name'),
            'url':      plugin.get_url(
                        action=     'list_directory',
                        id=         item.get('id'),
                        menu_id=    params.get('menu_id'),           
            ),
            'info': {
                  'music': {                
                        'artist': item.get('name'),
                        'mediatype': 'artist',
                        'rating': item.get('starred'),
                   }
            }
        }

####TO FIX        #context menu actions
        context_actions = []
        if can_star('artist',item.get('id')):
            action_star =  context_action_star('artist',item.get('id'))
            context_actions.append(action_star)
        if len(context_actions) > 0:
            entry['context_menu'] = context_actions

        listing.append(entry)
                
    return plugin.create_listing(
        listing,
        cache_to_disk = True,
        sort_methods = get_sort_methods('artists',params),
        view_mode = Addon().get_setting('view_artist'),
        content = 'artists'
    )

@plugin.action()
def list_directory(params):
    connection = get_connection()
    
    if connection is False:
        return

    listing = []
    
    # Get items
    id = params.get('id')
    items = connection.walk_directory_nonrecursive(id)
    dircount = 0
    songcount = 0

    # Iterate through items
    for item in items:
        genre_setting = item.get('genre') if (Addon().get_setting('view_genre')) else None
        
        # Is a directory
        if (item.get('isDir')==True):
            dircount += 1
            entry = {
                'label':    item.get('title'),
                'url':      plugin.get_url(
                            action=     'list_directory',
                            id=         item.get('id'),
                            menu_id=    params.get('menu_id')
                            ),
                'thumb':    connection.getCoverArtUrl(item.get('coverArt')),   
                'icon':    'DefaultMusicAlbums.png',            
                'info': {
                    'music': {
                              'mediatype': 'album',
                              'year':     item.get('year'),
                              'artist':   item.get('artist'),     
                              'rating':   item.get('starred'),
                              'genre':    genre_setting
                              }           
                        }
            }
            listing.append(entry)
    
        # Songs or a combination of both
        else:
            songcount += 1
            entry = get_entry_track(item,params)
            listing.append(entry)
        
        # Set view, sort and content 
        if (dircount == 0):
            view_mode_setting = Addon().get_setting('view_song')
            sort_mode = get_sort_methods('tracks',params)
            content_mode = 'songs'
        if (songcount == 0):
            view_mode_setting = Addon().get_setting('view_album')
            sort_mode = get_sort_methods('albums',params)
            content_mode = 'albums' 
            
        else:
            view_mode_setting = Addon().get_setting('view_song')
            sort_mode = get_sort_methods('tracks',params)
            content_mode = 'songs'

    # Only show in artist directory, maybe check results first?
    if (songcount == 0) and params.get('menu_id') == 'folders':
     topsongs = {
                'label':    item.get('artist') + '\'s top songs',
                'url':      plugin.get_url(
                            action=     'list_tracks',
                            query_args=  json.dumps({
                                           'artist': item.get('artist'),
                                           'count':  Addon().get_setting('tracks_per_page'),
                                         }),
                            menu_id=    'tracks_top',
                            ),
                'thumb':    'DefaultMusicTop100.png',  
                'info': {
                    'music': {
                              'mediatype': 'album',
                              'artist':    item.get('artist'),     
                              }           
                    }
                }        
     listing.append(topsongs)
     """
     artist_radio = {
                'label':    item.get('artist') + ' radio',
                'url':      plugin.get_url(
                            action=     'list_tracks',
                            id=         item.get('id'),
                            menu_id=    'artist_radio'
                            ),
                'thumb':    'DefaultMusicCompilations.png',  
                'info': {
                    'music': {            
                              'mediatype': 'album',
                              'artist':    item.get('artist'),     
                              }           
                    }
                }
     listing.append(artist_radio)
     """
    return plugin.create_listing(
        listing,
        cache_to_disk = True,
        sort_methods = sort_mode,
        view_mode = view_mode_setting,
        content = content_mode,
	)

@plugin.action()
def list_albums(params):
    
    #List albums from the library (ID3 tags)
    listing = []
    
    connection = get_connection()
    
    if connection is False:
        return

    #query
    query_args = {}
    try:
        query_args_json = params['query_args']
        query_args = json.loads(query_args_json)
    except:
        pass

    #Size, defined in settings
    albums_per_page = int(Addon().get_setting('albums_per_page'))
    query_args["size"] = albums_per_page
    
    #offset
    offset = int(params.get('page',1)) - 1;
    if offset > 0:
        query_args["offset"] = offset * albums_per_page

    #debug
    query_args_json = json.dumps(query_args)
    plugin.log('list_albums with args:' + query_args_json);

    #Get items
    if 'artist_id' in params:
        generator = connection.walk_artist(params.get('artist_id'))
    else:
        generator = connection.walk_albums(**query_args)
    
    #make a list out of the generator so we can iterate it several times
    items = list(generator)
    
    #coverart first in random album list if setting is true
    if Addon().get_setting('coverart_first') and params.get('menu_id') == 'albums_random':
        items = coverart_first(items)
    
    #check if there is only one artist for this album (and then hide it)
    artists = [item.get('artist',None) for item in items]
    if len(artists) <= 1:
        params['hide_artist']   = True

    # Iterate through items
    for item in items:
        album = get_entry_album(item, params)
        listing.append(album)
        
    if not 'artist_id' in params:
####TO FIX Pagination if we've not reached the end of the lsit
########### if type(items) != type(True): TO FIX
        link_next = navigate_next(params)
        listing.append(link_next)

    return plugin.create_listing(
        listing,
        cache_to_disk = True,
        sort_methods = get_sort_methods('albums',params), 
        view_mode = Addon().get_setting('view_album'),
        content = 'albums'
    )

@plugin.action()
def list_tracks(params):
    
    menu_id = params.get('menu_id')
    listing = []
    
    #query
    query_args = {}
    try:
        query_args_json = params['query_args']
        query_args = json.loads(query_args_json)
    except:
        pass

    #size
    tracks_per_page = int(Addon().get_setting('tracks_per_page'))
    query_args["size"] = tracks_per_page

    #offset
    offset = int(params.get('page',1)) - 1;
    if offset > 0:
        query_args["offset"] = offset * tracks_per_page
        
    #debug
    query_args_json = json.dumps(query_args)
    plugin.log('list_tracks with args:' + query_args_json);
    
    # get connection
    connection = get_connection()
    
    if connection is False:
        return

    # Album
    if 'album_id' in params:
        generator = connection.walk_album(params['album_id'])
        
    # Playlist
    elif 'playlist_id' in params:
        generator = connection.walk_playlist(params['playlist_id'])
##########TO FIX
#        tracknumber = 0
#        for item in items:
#            tracknumber += 1
#            items[item]['tracknumber'] = tracknumber
        
    # Top tracks
    elif menu_id == 'tracks_top':
        generator = connection.walk_tracks_top(query_args['artist'])
           
    # Starred
    elif menu_id == 'tracks_starred':
        generator = connection.walk_tracks_starred()
    
    # Random
    elif menu_id == 'tracks_random':
        generator = connection.walk_tracks_random(**query_args)
    
    #make a list out of the generator so we can iterate it several times
    items = list(generator)

    #check if there is only one artist for this album (and then hide it)
    artists = [item.get('artist',None) for item in items]
    if len(artists) <= 1:
        params['hide_artist'] = True
    
    #update stars
    if menu_id == 'tracks_starred':
        ids_list = [item.get('id') for item in items]
        stars_cache_update(ids_list)

    # Iterate through items
    key = 0;
    for item in items:
        track = get_entry_track(item,params)
        listing.append(track)
        key +=1
  
######TO FIX    # Pagination if we've not reached the end of the list
    # if type(items) != type(True): TO FIX
    #link_next = navigate_next(params)
    #listing.append(link_next)

    return plugin.create_listing(
        listing,
        cache_to_disk =     False,
        sort_methods=       get_sort_methods('tracks',params),
        view_mode =         Addon().get_setting('view_song'),
        content =           'songs'
    )

@plugin.action()
def list_playlists(params):
    
    connection = get_connection()
    
    if connection is False:
        return

    listing = []

    # Get items
    items = connection.walk_playlists()

    # Iterate through items
    for item in items:
        entry = get_entry_playlist(item,params)
        
        listing.append(entry)
        
    return plugin.create_listing(
        listing,
        sort_methods = get_sort_methods('playlists',params),
        view_mode = Addon().get_setting('view_albums'), 
        content = 'albums',
    )

@plugin.action()
def search(params):

    dialog = xbmcgui.Dialog()
    d = dialog.input(Addon().get_localized_string(30039), type=xbmcgui.INPUT_ALPHANUM)
    if not d:
        return False
    
    lmenu = []
    types = [
                {'type': "artist", 'locstr': 30085, 'image': "DefaultMusicArtists.png"},
                {'type': "album", 'locstr': 30086, 'image': "DefaultMusicAlbums.png"},
                {'type': "track", 'locstr': 30087, 'image': "DefaultMusicSongs.png"},
            ]
    
    for props in types:
        lmenu.append({
                        'label':    Addon().get_localized_string(props['locstr']),
                        'url':      plugin.get_url(
                                        action=         'get_search_results',
                                        page=           1,
                                        query_args=     json.dumps({
                                                            'query': d,
                                                            'type': props['type'],
                                                        }),
                                        firstEntry=     True,
                                        ),
                        'thumb':    props['image'],
                        'fanart':   None,
                    })
    return plugin.create_listing(
         lmenu, 
         cache_to_disk=True,         
         content = 'mixed'
    )

@plugin.action()
def get_search_results(params):
    # get connection
    connection = get_connection()

    if connection is False:
        return

    query_args = json.loads(params['query_args'])
    maxitems = int(Addon().get_setting('tracks_per_page' if query_args['type'] == "track" else 'albums_per_page'))
    
    # Get items
    # This uses the same maximum amount for all types, but since we only use the one we're interested in that's ok.
    items = connection.search2(
                    query=          query_args['query'], 
                    artistCount=    maxitems, 
                    artistOffset=   maxitems * params['page'], 
                    albumCount=     maxitems,
                    albumOffset=    maxitems * params['page'], 
                    songCount=      maxitems, 
                    songOffset=     maxitems * params['page'], 
                    musicFolderId=  None)
    
    itemfunc =   {
                        "get_entry_artist": get_entry_artist,
                        "get_entry_album": get_entry_album,
                        "get_entry_track": get_entry_track,
                    }
    listing = []
    # Maybe we should refactor "track" functions to "song" some day to stay in line with subsonic API lingo
    type = "song" if query_args['type'] == "track" else query_args['type']
    # Iterate through items
    if type in items['searchResult2']:
        for item in items.get('searchResult2').get(type):
            entry = itemfunc['get_entry_{0}'.format(query_args['type'])](item, params)
            listing.append(entry)
        
        prev = navigate_prev(params)
        if prev:
            listing.append(prev)
            maxitems += 1
        # TODO: check that there are actually more results available
        if len(listing) == maxitems:
            listing.append(navigate_next(params))
    else:
        d = xbmcgui.Dialog().ok(
                Addon().get_localized_string(30062), # Search
                Addon().get_localized_string(30088)  # No items found
            )
        return

    if query_args['type'] == "track":
          content = 'songs'
          view_mode_setting = Addon().get_setting('view_song')
    elif query_args['type'] == "album":
          content = 'albums'
          view_mode_setting = Addon().get_setting('view_album')
    else:
          content = 'artists'			 
          view_mode_setting = Addon().get_setting('view_artist')
        
    return plugin.create_listing(
           listing, 
           update_listing=not params.get('firstEntry', False),
           view_mode = view_mode_setting,
           content = content,
    )

@plugin.action()
def play_track(params):
    
    id = params['id']
    plugin.log('play_track #' + id);
    
    connection = get_connection()
    
    if connection is False:
        return

    url = connection.streamUrl(sid=id,
        maxBitRate=Addon().get_setting('bitrate_streaming'),
        tformat=Addon().get_setting('transcode_format_streaming')
    )

    return url


@plugin.action()
def star_item(params):

    ids=     params.get('ids'); #can be single or lists of IDs
    unstar=  params.get('unstar',False);
    unstar = (unstar) and (unstar != 'None') and (unstar != 'False') #TO FIX better statement ?
    type=    params.get('type');
    sids =   albumIds = artistIds = None

    #validate type
    if type == 'track':
        sids = ids
    elif type == 'artist':
        artistIds = ids
    elif type == 'album':
        albumIds = ids
            
    #validate capability
    if not can_star(type,ids):
        return;
        
    #validate IDs
    if (not sids and not artistIds and not albumIds):
        return;

    # get connection
    connection = get_connection()
    
    if connection is False:
        return

    ###
    
    did_action = False

    try:
        if unstar:
            request = connection.unstar(sids, albumIds, artistIds)
        else:
            request = connection.star(sids, albumIds, artistIds)

        if request['status'] == 'ok':
            did_action = True

    except:
        pass

    ###
    
    if did_action:
        
        if unstar:
            message = Addon().get_localized_string(30091)
            plugin.log('Unstarred %s #%s' % (type,json.dumps(ids)))
        else: #star
            message = Addon().get_localized_string(30092)
            plugin.log('Starred %s #%s' % (type,json.dumps(ids)))
            
        stars_cache_update(ids,unstar)
       
        popup(message)
            
        #TO FIX clear starred lists caches ?
        #TO FIX refresh current list after star set ?
        
    else:
        if unstar:
            plugin.log_error('Unable to unstar %s #%s' % (type,json.dumps(ids)))
        else:
            plugin.log_error('Unable to star %s #%s' % (type,json.dumps(ids)))

    return did_action
        

        
@plugin.action()
def download_item(params):

    id=     params.get('id'); #can be single or lists of IDs
    type=    params.get('type');
    
    #validate path
    download_folder = Addon().get_setting('download_folder')
    
    if not download_folder:
        popup("Please set a directory for your downloads")
        plugin.log_error("No directory set for downloads")

    #validate capability
    if not can_download(type,id):
        return;
    
    if type == 'track':
        did_action = download_tracks(id)
    elif type == 'album':
        did_action = download_album(id)
    
    if did_action:
        plugin.log('Downloaded %s #%s' % (type,id))
        popup('Item has been downloaded!')
        
    else:
        plugin.log_error('Unable to downloaded %s #%s' % (type,id))

    return did_action
    
def get_entry_playlist(item,params):
    image = connection.getCoverArtUrl(item.get('coverArt'))
    genre_setting = item.get('genre') if (Addon().get_setting('view_genre')) else None

    return {
        'label':    item.get('name'),
        'thumb':    image,
        'icon':    'DefaultMusicPlaylists.png',            
        'url':      plugin.get_url(
                        action=         'list_tracks',
                        playlist_id=    item.get('id'),
                        menu_id=        params.get('menu_id')
                    ),
        'info': {'music': {
            'mediatype':    'album',
            'title':        item.get('name'),
            'count':        item.get('songCount'),
            'duration':     item.get('duration'),
            'date':         convert_date_from_iso8601(item.get('created')),
            'genre':        genre_setting,
            'rating':       item.get('starred'),
        }}
    }

def get_entry_artist(item,params):
    coverartsrc = 'coverArt' if 'coverArt' in item else 'id'
    if Addon().get_setting('coverart_from_server'): 
       image = connection.getCoverArtUrl(item.get(coverartsrc)) 
    else: 
       image = None

    return {
        'label':    item.get('name'),
        'icon':     'DefaultArtist.png',
        'thumb':    image,
        'url':      plugin.get_url(
                        action=     'list_directory',
                        id=         item.get('id'),
                    ),
        'info': {
            'music': {
                'mediatype':    'artist',
                'artist':       item.get('name')
            }
        }
    }


def get_entry_album(item, params):
    coverartsrc = 'coverArt' if 'coverArt' in item else 'id'
    image = connection.getCoverArtUrl(item.get(coverartsrc))
    genre_setting = item.get('genre') if (Addon().get_setting('view_genre')) else None
 
    entry = {
        'label':    get_entry_album_label(item,params.get('hide_artist',False)),
        'thumb':    image,
        'icon':     'DefaultMusicAlbums.png',            
        'url': plugin.get_url(
            action=         'list_directory',
            id=             item.get('id'),
            hide_artist=    item.get('hide_artist'),
            menu_id=        params.get('menu_id')
        ),
        'info': {
            'music': {
                'mediatype': 'album',
                #'count':    item.get('songCount'),
                'date':     convert_date_from_iso8601(item.get('created')), #date added
                #'duration': item.get('duration'),
                'artist':   item.get('artist'),
                'album':    item.get('name'),
                'year':     item.get('year'),
                'genre':    genre_setting,
                'rating':   item.get('starred'),             
            }
        }
    }
    
    #context menu actions
    context_actions = []

    if can_star('album',item.get('id')):
        action_star =  context_action_star('album',item.get('id'))
        context_actions.append(action_star)

    if can_download('album',item.get('id')):
        action_download =  context_action_download('album',item.get('id'))
        context_actions.append(action_download)

    if len(context_actions) > 0:
        entry['context_menu'] = context_actions

    return entry

def get_entry_track(item,params):
    
    menu_id = params.get('menu_id')

    coverartsrc = 'coverArt' if 'coverArt' in item else 'id'
    image = connection.getCoverArtUrl(item.get(coverartsrc))
    genre_setting = item.get('genre') if (Addon().get_setting('view_genre')) else None
    
    entry = {
        'label':        get_entry_album_label(item,params.get('hide_artist',False)),
        'tracknumber':  item.get('track'),
        'thumb':        image,
        'url':          plugin.get_url(
                           action=     'play_track',
                           id=         item.get('id'),
                           menu_id=    menu_id
                        ),
        'is_playable':  True,
        'mimetype':     item.get("contentType"),
        'info': 
			{'music': {
            'mediatype':    'song',
            'title':        item.get('title'),
            'album':        item.get('album'),
            'tracknumber':  item.get('track'),
            'artist':       item.get('artist'),
            'year':         item.get('year'),
            'genre':        genre_setting,
            'size':         item.get('size'),
            'duration':     item.get('duration'),
            'date':         item.get('created'),
            'rating':       item.get('starred'),
            }
        }
    }
    
    #context menu actions
    context_actions = []

    if can_star('track',item.get('id')):
        action_star =  context_action_star('track',item.get('id'))
        context_actions.append(action_star)

    if can_download('track',item.get('id')):
        action_download =  context_action_download('track',item.get('id'))
        context_actions.append(action_download)

    if len(context_actions) > 0:
        entry['context_menu'] = context_actions

    return entry

def get_entry_track_label(item,hide_artist = False):
    if hide_artist:
        label = item.get('title', '<Unknown>')
    else:
        label = '%s - %s' % (
            item.get('artist', '<Unknown>'),
            item.get('title', '<Unknown>'),
        )
    return label

def get_entry_album_label(item,hide_artist = False):
    if hide_artist:
        label = item.get('name',item.get('title', '<Unknown>'))
    else:
        label = '%s - %s' % (
              item.get('artist', '<Unknown>'),
              item.get('name',item.get('title', '<Unknown>')),
        )
    return label

def get_sort_methods(type,params):
    sortable = [
        xbmcplugin.SORT_METHOD_NONE,
    ]
    
    if type is 'artists':
        
        artists = [
            xbmcplugin.SORT_METHOD_LABEL,
        ]

        sortable = artists
        
    elif type is 'albums':
        
        albums = [
            xbmcplugin.SORT_METHOD_VIDEO_YEAR, 
            xbmcplugin.SORT_METHOD_LABEL,
        ]
        
        if not params.get('hide_artist',False):
            albums.append(xbmcplugin.SORT_METHOD_ARTIST)

        # No sort options for subsonic album lists        
        if params.get('menu_id') != 'folders':
            albums = [
                  xbmcplugin.SORT_METHOD_NONE,
            ]

        sortable = albums
        
    elif type is 'tracks':

        tracks = [
            xbmcplugin.SORT_METHOD_TRACKNUM,
            xbmcplugin.SORT_METHOD_TITLE,
            xbmcplugin.SORT_METHOD_ALBUM,
            xbmcplugin.SORT_METHOD_SIZE,
            xbmcplugin.SORT_METHOD_DURATION,
            xbmcplugin.SORT_METHOD_VIDEO_YEAR,
            xbmcplugin.SORT_METHOD_BITRATE
        ]
        
        if not params.get('hide_artist',False):
            tracks.append(xbmcplugin.SORT_METHOD_ARTIST)
        
        if params.get('menu_id') == 'playlists':
            tracks = xbmcplugin.SORT_METHOD_PLAYLIST_ORDER,
        
        if params.get('menu_id') == 'tracks_random' or params.get('menu_id') == 'tracks_starred' or params.get('menu_id') == 'tracks_top':
            tracks = xbmcplugin.SORT_METHOD_NONE,

        sortable = tracks
        
    elif type is 'playlists':

        playlists = [
            xbmcplugin.SORT_METHOD_TITLE,
            xbmcplugin.SORT_METHOD_DURATION,
            xbmcplugin.SORT_METHOD_DATE
        ]
        
        sortable = playlists

    return sortable
    

def stars_cache_update(ids,remove=False):

    #get existing cache set
    starred = stars_cache_get()
    
    #make sure this is a list
    if not isinstance(ids, list):
        ids = [ids]
    
    #abord if empty
    if len(ids) == 0:
        return
    
    #parse items
    for item_id in ids:
        item_id = item_id
        if not remove:
            starred.add(item_id)
        else:
            starred.remove(item_id)
    
    #store them
    with plugin.get_storage() as storage:
        storage['starred_ids'] = starred
        
    plugin.log('stars_cache_update:')
    plugin.log(starred)


def stars_cache_get():
    with plugin.get_storage() as storage:
        starred = storage.get('starred_ids',set())

    plugin.log('stars_cache_get:')
    plugin.log(starred)
    return starred

def is_starred(id):
    starred = stars_cache_get()
    id = id
    if id in starred:
        return True
    else:
        return False

def navigate_next(params):
  
    page =      int(params.get('page',1))
    page +=     1
    
    title =  Addon().get_localized_string(30090) +" (%d)" % (page)

    return {
        'label':    title,
        'url':      plugin.get_url(
                        action=         params.get('action',None),
                        page=           page,
                        query_args=     params.get('query_args',None)
                    )
    }

def navigate_prev(params):
  
    page =      int(params.get('page',1))
    if page <= 1:
        return
    page -=     1
    
    title =  Addon().get_localized_string(30096) +" (%d)" % (page)

    return {
        'label':    title,
        'url':      plugin.get_url(
                        action=         params.get('action',None),
                        page=           page,
                        query_args=     params.get('query_args',None)
                    )
    }

def navigate_root():
    return {
        'label':    Addon().get_localized_string(30030),
        'url':      plugin.get_url(action='root')
    }

#converts a date string from eg. '2012-04-17T19:53:44' to eg. '17.04.2012'
def convert_date_from_iso8601(iso8601):
    date_obj = dateutil.parser.parse(iso8601)
    return date_obj.strftime('%d.%m.%Y')

def context_action_star(type,id):
    
    starred = is_starred(id)

    if not starred:

        label = Addon().get_localized_string(30093)
            
    else:
        
        #Should be available only in the stars lists;
        #so we don't have to fetch the starred status for each item
        #(since it is not available into the XML response from the server)

        label = Addon().get_localized_string(30094)
    
    return (
        label, 
        'XBMC.RunPlugin(%s)' % plugin.get_url(action='star_item',type=type,ids=id,unstar=starred)
    )

#Subsonic API says this is supported for artist,tracks and albums,
#But I can see it available only for tracks on Subsonic 5.3, so disable it.
def can_star(type,ids = None):
    
    if not ids:
        return False
    
    if not isinstance(ids, list) or isinstance(ids, tuple):
        ids = [ids]
        if len(ids) == 0:
            return False
    
    if type == 'track':
        return True
    elif type == 'artist':
        return True
    elif type == 'album':
        return True

    
def context_action_download(type,id):
    
    label = Addon().get_localized_string(30095)
    
    return (
        label, 
        'XBMC.RunPlugin(%s)' % plugin.get_url(action='download_item',type=type,id=id)
    )

def can_download(type,id = None):
    if id is None:
        return False
    
    if type == 'track':
        return True
    elif type == 'album':
        return True
    
def download_tracks(ids):

    #popup is fired before, in download_item
    download_folder = Addon().get_setting('download_folder')
    if not download_folder:
        return
    
    if not ids:
        return False
    
    #make list
    if not isinstance(ids, list) or isinstance(ids, tuple):
        ids = [ids]
        
    
    ids_count = len(ids)
    
    #check if empty
    if ids_count == 0:
        return False
    
    plugin.log('download_tracks IDs:')
    plugin.log(json.dumps(ids))

    # get connection
    connection = get_connection()
    
    if connection is False:
        return

    #progress...
    pc_step = 100/ids_count
    pc_progress = 0
    ids_parsed = 0
    progressdialog = xbmcgui.DialogProgress()
    progressdialog.create("Downloading tracks...") #Title

    for id in ids:

        if (progressdialog.iscanceled()):
            return False

        # debug
        plugin.log('Trying to download track #'+str(id))

        # get track infos
        response = connection.getSong(id);
        track = response.get('song')
        plugin.log('Track info :')
        plugin.log(track)
        
        # progress bar
        pc_progress = ids_parsed * pc_step
        progressdialog.update(pc_progress, 'Getting track informations...',get_entry_track_label(track))

        track_path_relative = track.get("path", None).encode('utf8', 'replace') # 'Radiohead/Kid A/Idioteque.mp3'
        track_path = os.path.join(download_folder, track_path_relative) # 'C:/users/.../Radiohead/Kid A/Idioteque.mp3'
        track_directory = os.path.dirname(os.path.abspath(track_path))  # 'C:/users/.../Radiohead/Kid A'

        #check if file exists
        if os.path.isfile(track_path):
            
            progressdialog.update(pc_progress, 'Track has already been downloaded!')
            plugin.log("File '%s' already exists" % (id))
            
        else:
            
            progressdialog.update(pc_progress, "Downloading track...",track_path)

            try:
                #get remote file (file-object like)
                file_obj = connection.download(id)

                #create directory if it does not exists
                if not os.path.exists(track_directory):
                    os.makedirs(track_directory)

                #create blank file
                file = open(track_path, 'a') #create a new file but don't erase the existing one if it exists

                #fill blank file
                shutil.copyfileobj(file_obj, file)
                file.close()

            except:
                popup("Error while downloading track #%s" % (id))
                plugin.log("Error while downloading track #%s" % (id))
                pass
        
        ids_parsed += 1
        
    progressdialog.update(100, "Done !","Enjoy !")
    xbmc.sleep(1000)
    progressdialog.close()

def download_album(id):

    # get connection
    connection = get_connection()
    
    if connection is False:
        return

    # get album infos
    response = connection.getAlbum(id);
    album = response.get('album')
    tracks = album.get('song')
    
    plugin.log('getAlbum:')
    plugin.log(json.dumps(album))

    ids = [] #list of track IDs
    
    for i, track in enumerate(tracks):
        track_id = track.get('id')
        ids.append(track_id)

    download_tracks(ids)

def coverart_first(list_input):
	america = list()
	restofworld = list()
	for item in list_input:
		if 'coverArt' in item:
			america.append(item)
		else:
			restofworld.append(item)
	return america + restofworld

# Start plugin from within Kodi.
if __name__ == "__main__":
    # Map actions
    # Note that we map callable objects without brackets ()
    plugin.run()

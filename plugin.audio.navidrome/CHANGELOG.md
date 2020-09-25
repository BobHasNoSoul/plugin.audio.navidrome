# Changelog

TODO:
* list tracks for album random e.d. is broken!
* Scrape fanart and artist bio on the fly when possible?
* Artist has genre (maybe music-folder?) and add sort method in artist list
* Set album artist in compilation album?
* Hide_artist feature not working as intended, f.e. random tracks and compilation albums
* Set star for album and artist
* Download for albums and artists
* Show path with artist/album/search/etc. on top
* Add on name in bar configurable, so you can call it Music
* Play button plays artist or album
* Manage playlists and add tracks to playlist in the plugin
* Raring stars show rating (better solution?)
* Info works in artist and album
* Bug: going back to artist list shows the album viewtype
* Pagination only in random tracks, not album tracks
* Starred items have a star icon instead of color, dont use kodi rating option
* Top Songs and radio feature in artist folder and context menu (config option), top songs thumb call subsonic doen voor lastfm plaatje?
* Similar artist feature, with above 3 config options, menu, as album, off, both
* Improve caching system, random - album - back different list
* Scrobble to lastfm
* Search filter GUI for tracks and albums, or global search addon
* Crash on Kodi 18 alpha
* Integrate statistics in kodi, library songs and artist? Or plugin root page
* Top songs, artist radio and similar artist items are configurable *CONFIG OPTIONS ARE THERE

## v3.1.2
* Top songs for an artist, basic functionality working
* Made artist thumb from server optional

## v3.1.1
* bugfixes

## v3.1.0
* Added a proper search function (artist, album, track)
* Added artist thumb from subsonic
* Fixed label and thumb in root menu for merged folder setting

## v3.0.1
* Sort methods fixed in all views (fixed missing track numbers also)
* Keep subsonic sort method for random, frequent, recent and newest albums.
* Coverart feature only works in random albums list as intended.
* Removed the colored star label, instead use rating stars for now.
* Playlists icons added

## v3.0.0
(Forked from 2.0.8 by gordielachance)
Released 27-03-2018
* Fixed the list of artist-folder content recursive, to result in a long list of tracks
* Changed the complete addon menu structure, single root page
* Added icons to menu options
* Removed the tag based library browse mode
* Added option to merge media-folders
* Improved metadata implementation
* Changed the content property for a view, to enable available skin views
* Added option to set view types for artist, album and song lists
* Added option to show albums with coverart first in the album list (Looks better in Widgets)
* First starred implementation, bad looking 
* Updated the English translation. The only language for now, please contribute!
* Code cleanup

## v2.0.8
Released 29th November 2017 (by Heruwar)
* Fixes a security issue where the password is sent as plaintext in the URL query parameters when methods from libsonic_extas are used. 
Also adds Subsonic hex encoding when using legacy auth.
* Adds support for URL paths like https://hostname.com/subsonic as requested in Github issue #17 and also encountered in some of the reports (#14 and #5)
* Fixes an error when the password only contains digits, which simpleplugin converts to a Long, which later fails when libsonic tries to salt the password expecting a string.

## v2.0.7
Released 18 April 2017
* Added Search (by silascutler)

## v2.0.6
Released 14 January 2017
* Upgrade to simpleplugin 2.1.0
* Browse/Library menus (file structure vs ID3 tags)
* Added multilanguage support

## v2.0.5
Released 15 October 2016
* Fixed images when listing entries

## v2.0.4
Released 5 October 2016
* Cache (permanently) starred items so we can know everywhere if an item is starred or not without querying it
* Colorize starred items
* Hide artist in lists if it is unique
* Removed list_artist_albums()
* Include simpleplugin v2.0.1 as library and remove KODI dependency

## v2.0.3
Released 4 October 2016
* Random tracks submenu
* Download tracks
* Star tracks
* Context menu for downloading or marking items as favorite

## v2.0.2
* main code (main.py) fully rewritten
* Use SimplePlugin framework (http://romanvm.github.io/script.module.simpleplugin/index.html)
* Cache datas

## v2.0.1
* New setting 'albums_per_page'
* New menu structure
* Albums : Newest / Most played / Rencently played / by Genre
* Tracks : Starred / Random by genre / Random by year
* Upgraded: libsonic to v.0.5.0 (https://github.com/crustymonkey/py-sonic)
* Code cleanup

## v2.0.0
Released 14 September 2015

Highlight:
* Added: support for starred items.
* Fixed: transcode format property was incorrect.
* Improved: playlist handling.
* Improved: metadata.
* Upgraded: libsonic.
* Upgraded: libsonic_extra.s

The full list of commits can be found [here](https://github.com/rembo10/headphones/compare/v1.0.0...v2.0.0).

## v1.0.0
Released 31 May 2015

Highlights:
* Added: support for playlists.
* Added: number of random items to show.
* Improved: metadata for items.
* Fixed: migrated to [`py-sonic`](https://github.com/crustymonkey/py-sonic) to interact with Subsonic.

The full list of commits can be found [here](https://github.com/rembo10/headphones/compare/ff86dfa49f914a18233dee295df74b73a70200e8...v1.0.0).

## Navidrome Kodi Plugin

A Navidrome plugin for kodi that allows you to play all of your awesome music from a self-hosted lightweight navidrome server.
This plugin was originally forked from a previous subsonic plugin that is incompatable with the current navidrome servers

(thats navidrome version 0.34.0 (a99924e) as of writing this) however this plugin dives right into there using the subsonic plugin and fixes the connection issues

DISCLAIMER: I did not write the entire plugin or server backend I merely fixed the plugin to allow it to work and updated it to have a more navidrome specific look and feel (it also breaks the connection to subsonic servers to allow navidrome)

### Please note this supports TLS v1 only at the moment, I am looking into upgrading it to tls 1.3 and 1.2 but with kodi being the main constraint here it may take a while.

This plugins github: 
https://github.com/BobHasNoSoul/plugin.audio.navidrome

forked from this plugin:
https://github.com/jeweet/plugin.audio.subsonic

## Features
* Browse by artist, albums (newest/most played/recently played/random), tracks (starred/random), and playlists
* Download songs
* Star songs

## Screenshots
Here you can see the plugin in its default skin
![screenshot](https://github.com/BobHasNoSoul/plugin.audio.navidrome/blob/master/screenshots/default/1.PNG?raw=true)
![screenshot](https://github.com/BobHasNoSoul/plugin.audio.navidrome/blob/master/screenshots/default/2.PNG?raw=true)
![screenshot](https://github.com/BobHasNoSoul/plugin.audio.navidrome/blob/master/screenshots/default/3.PNG?raw=true)
![screenshot](https://github.com/BobHasNoSoul/plugin.audio.navidrome/blob/master/screenshots/default/4.PNG?raw=true)

Here you can see the plugin in the skin called "Bingie"
![screenshot](https://github.com/BobHasNoSoul/plugin.audio.navidrome/blob/master/screenshots/bingie/1.PNG?raw=true)
![screenshot](https://github.com/BobHasNoSoul/plugin.audio.navidrome/blob/master/screenshots/bingie/2.PNG?raw=true)
![screenshot](https://github.com/BobHasNoSoul/plugin.audio.navidrome/blob/master/screenshots/bingie/3.PNG?raw=true)
![screenshot](https://github.com/BobHasNoSoul/plugin.audio.navidrome/blob/master/screenshots/bingie/4.PNG?raw=true)

## Installation
* Download the release zip
* install the plugin via zip

## Alternative Installation
* Navigate to your `.kodi/addons/` folder
* Clone this repository: `git clone https://github.com/BobHasNoSoul/plugin.audio.navidrome.git`
* (Re)start Kodi.

## License
See the `LICENSE` file.

Additional copyright notices:
* [Previous version of this plugin](https://github.com/jeweet/plugin.audio.subsonic) by jeweet
* [Previous version of this plugin](https://github.com/gordielachance/plugin.audio.subsonic) by gordielachance
* [Previous version of this plugin](https://github.com/basilfx/plugin.audio.subsonic) by basilfx
* [SimplePlugin](https://github.com/romanvm/script.module.simpleplugin/stargazers) by romanvm
* The original [SubKodi](https://github.com/DarkAllMan/SubKodi) plugin
* [`py-sonic`](https://github.com/crustymonkey/py-sonic) Python module

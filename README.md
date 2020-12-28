# UPDATE 28th dec 2020
# due to personal issues i will no longer be maintaining this repo, i will archive this to read only so others may find this useful.
# many thanks and stay safe.
# - BobHasNoSoul

## Navidrome Kodi Plugin

A Navidrome plugin for kodi that allows you to play all of your awesome music from a self-hosted lightweight navidrome server.
This plugin was originally forked from a previous subsonic plugin that is incompatable with the current navidrome servers

(thats navidrome version 0.34.0 (a99924e) as of writing this) however this plugin dives right into there using the subsonic plugin and fixes the connection issues

DISCLAIMER: I did not write the entire plugin or server backend I merely fixed the plugin to allow it to work and updated it to have a more navidrome specific look and feel (it also breaks the connection to subsonic servers to allow navidrome)

### Please note this supports TLS v1 only at the moment, I am looking into upgrading it to tls 1.3 and 1.2 but with kodi being the main constraint here it may take a while.
If you are using Caddy please enable tls 1.0 as documented here https://caddyserver.com/docs/caddyfile/directives/tls or by using something like the following syntax in your caddyfile
```
tls xxx@xxx.com {
    protocols tls1.0 tls1.2
    ciphers some_tls_1.0_1.1_ciphers
}
```
*The above syntax may differ depending on the version of caddy you are using V1/V2*

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
* Download the release zip.
* Install the plugin via zip.
* Configure plugin with the server address in the following format `https://example.com` or if you are using a local ip `http://192.168.1.x:4533`.
* Configure plugin with a user that has been created in the navidrome server (you cannot create accounts with this plugin).

## Alternative Installation
* Navigate to your `.kodi/addons/` folder.
* Clone this repository: `git clone https://github.com/BobHasNoSoul/plugin.audio.navidrome.git`.
* (Re)start Kodi.
* Configure plugin with the server address in the following format `https://example.com` or if you are using a local ip `http://192.168.1.x:4533`.
* Configure plugin with a user that has been created in the navidrome server (you cannot create accounts with this plugin).

## FAQ

*I Don't have a navidrome server, Where can I get one?*
You can get one by grabbing the server binary or compiling your own from navidrome.org (not to mention all the documentation, discord links etc)

*It wont connect, it just says "Connection Error"*
This could be any number of things but try the following:
- Check your server can be reached on a system outside of your host machine (like a phone or tablet via the ip:4533 in a web browser) if it cannot check your firewall on your host machine.
- Check your details are correct in the plugin, in the plugin the details are case-sensitive and http:// or https:// does matter if you have ssl it should be https:// if you do not it should be http://
- If you have a self-signed certificate, go to the advanced tab in the settings for the plugin and enable the self-signed option.

## License
See the `LICENSE` file.

Additional copyright notices:
* [Previous version of this plugin](https://github.com/jeweet/plugin.audio.subsonic) by jeweet
* [Previous version of this plugin](https://github.com/gordielachance/plugin.audio.subsonic) by gordielachance
* [Previous version of this plugin](https://github.com/basilfx/plugin.audio.subsonic) by basilfx
* [SimplePlugin](https://github.com/romanvm/script.module.simpleplugin/stargazers) by romanvm
* The original [SubKodi](https://github.com/DarkAllMan/SubKodi) plugin
* [`py-sonic`](https://github.com/crustymonkey/py-sonic) Python module

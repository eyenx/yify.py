yify.py
=======

Python script to interact wit yify-torrents api

How to Run
-----------

Use peerflix + the dabble site to watch yify movies on your Chromecast


This uses peerflix plus https://dabble.me/cast with the yify.py script found here https://github.com/eyenx/yify.py

Basic setup instructions: You will need nodejs, npm, and python-requests (Ubuntu)

`sudo apt-get install nodejs npm python-requests git`


Then

`sudo npm install peerflix -g`

By default the peerflix script looks for node but the binary is called nodejs most of the time. Run this and edit the very first line and change node to nodejs.

`sudo nano $(which peerflix)`

Then we need to clone the yify torrents script.

`git clone https://github.com/eyenx/yify.py`
`cd yify.py`

Edit yify.py and replace python with python3 in the very first line.

Run

./yify.py -c peerflix
to set the command that is run upon selecting a torrent

Export your browser variable (needed for yify.py but not used here)

export BROWSER=anything
Run

./yify.py -t <search term>
(-t signifies we want the torrent URL instead of the magnet link)

Select the movie you want and press enter. This will launch peerflix. Quickly copy the top URL into a Chrome window. In my case it was

http://192.168.1.135:8888

Let this load in the browser first. We need to make sure it has downloaded enough to start playing.

Then use this bookmarklet (the original bookmarklet from dabble doesn't recognize this URL as valid since it doesnt contain a file extension)

javascript:location.href='https://dabble.me/cast/?video_link='+document.location.href;

Then just click on that bookmarklet. The dabble page will load up. Use the normal cast extension to select your Chromecast and then hit Play. If it says error at first just refresh. It will stay connected to the chromecast and should start playing afterwards.

Note to stop peerflix you have to run

killall nodejs
in a terminal window.

I'll try to clean up this guide later. Just wanted to get my thoughts down for anybody that may want to try this.

EDIT: Cleaned up.

EDIT2: Windows instructions http://www.reddit.com/r/Chromecast/comments/1x992z/use_peerflix_the_dabble_site_to_watch_yify_movies/cf9tokp

usage:
------ 

yify.py <options> <search string>

  options:

  -l, --limit:       limit the max amount of movie results (integer 1-50)
  
  -q, --quality:     choose between 720p, 1080p or 3D.
  
  -r, --rating:      sets minimum imd rating (integer 1-10)
  
  -g, --genre:       genre see http://www.imdb.com/genre/ for full list.
  
  -s, --sort:        sort result by date, seeds, peers, size, alphabet, rating, downloaded.
  
  -o, --order:       order ascending or descending (asc/desc).
  
  -a, --autoadd:     automatically add every single search result through your command.
  
  -c, --command:     change your chosen default command to add the magnet links
  
  -t, --torrenturl:  use torrent url instead of magnet link

  Invalid input will try to search with default values.

TODO:
-----

- Add Browser functionality
- Add autoadd-all functionality

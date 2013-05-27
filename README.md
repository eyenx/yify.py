yify.py
=======

Python script to interact wit yify-torrents api

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

  Invalid input will try to search with default values.

TODO:
-----

- Add Browser functionality
- Add autoadd-all functionality

#!/usr/bin/python
#               _  __
#         _   _(_)/ _|_   _   _ __  _   _
#        | | | | | |_| | | | | '_ \| | | |
#        | |_| | |  _| |_| |_| |_) | |_| |
#         \__, |_|_|  \__, (_) .__/ \__, |
#         |___/       |___/  |_|    |___/
#
#
# Search and add magnet links directly from the api list-movies method of http://yify-torrents.com/

import sys,subprocess,json,getopt,os,re
try:
    from urllib import request as request_module
    from urllib.request import URLError
except ImportError:
#    print("Couldn't find urllib.Request, will use urllib2")
    import urllib2 as request_module
    from urllib2 import URLError


def usage(msg=""):
  print("""usage:

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

  """)

  error(msg)

# random error function, just used for errors
def error(msg):
  print(msg);
  sys.exit(1)

# getopt parser
def optparser():
  try:
    par,args=getopt.getopt(sys.argv[1:],"l:q:r:k:g:s:o:tac:",["torrenturl","limit=","quality=","rating=","keywords=","genre=","sort=","order=","autoadd","command="])
    return(par,args)
  except getopt.GetoptError as opterr:
    usage(str(opterr))

# output function with colors
def output(movies):
  red="\033[1;31m"
  green="\033[1;32m"
  yellow="\033[1;33m"
  blue="\033[1;34m"
  purple="\033[1;35m"
  turk="\033[1;36m"
  norm="\033[0m"
  sep=norm+" | "
  i=1
  # if dict then
  if type(movies) is dict:
    if 'error' in movies.keys():
        error(red+movies['error'])
    elif 'MovieList' in movies.keys():
      for movie in movies['MovieList']:
        print(purple+str(i)+sep+yellow+movie["MovieTitle"]+sep+green+movie["TorrentSeeds"]+sep+red+movie["TorrentPeers"]+sep+blue+movie["Size"]+sep+turk+movie["Quality"]+norm)
        i+=1
  # else just output some random error
    else:
      error(red+"There was some sort of other error")
  # else just output some random error
  else:
    error(red+"There was some sort of other error")

def userinput(r):
  inp=input("Add Torrent with respective number: ")
  try:
    if int(inp) not in range(int(r)+1):
      error("Your choice was invalid")
    else:
      return int(inp)
  except ValueError:
    error("There was an error in your input")

def toradd(com,arg):
  comls=com.split()
  comls.append(arg)
  subprocess.Popen(comls)
# change the config
def config(c):
  py=os.path.abspath(sys.argv[0])
  f=open(py,'r')
  d=f.read()
  f.close()
  pat=re.compile("(\n\s+command=\").*(\"\n)")
  pre,aft=re.search(pat,d).groups()
  nd=re.sub(pat,pre+c+aft,d)
  f=open(py,'w')
  f.write(nd)
  f.close()
  sys.exit("command variable was changed to: "+c+"\nWill now exit")



class Yify():

  # some constants

  url="http://yify-torrents.com/api/list.json"

  qualities=["720p","1080p","3D","ALL"]
  genres=["action","adventure","animation","biography","comedy","crime","documentary","drama","family","fantasy","film-noir","history","horror","music","musical","mystery","romance","sci-fi","short","sport","thriller","war","western"]
  ratings=range(11)
  limits=range(51)
  sorts=["date","seeds","peers","size","alphabet","rating","downloaded"]
  orders=["desc","asc"]

  def __init__(self,limit=15,quality="ALL",rating=0,genre="ALL",sort="seeds",order="desc",keywords=""):
    # set defaults (could be done better)
    self.set_limit(limit)
    self.set_quality(quality)
    self.set_rating(rating)
    self.set_genre(genre)
    self.set_sort(sort)
    self.set_order(order)
    self.set_keywords(keywords)

  def set_limit(self,limit):
    if int(limit) in self.limits:
      self.limit=limit
    else:
      self.limit=15
  def set_quality(self,quality):
    if quality in self.qualities:
      self.quality=quality
    else:
      self.quality="ALL"
  def set_rating(self,rating):
    if int(rating) in self.ratings:
      self.rating=rating
    else:
      self.rating=0
  def set_genre(self,genre):
    if genre in self.genres:
      self.genre=genre
    else:
      self.genre="ALL"
  def set_sort(self,sort):
    if sort in self.sorts:
      self.sort=sort
    else:
      self.sort="seeds"
  def set_order(self,order):
    if order in  self.orders:
      self.order=order
    else:
      self.order="desc"
  def set_keywords(self,keywords):
    self.keywords="%20".join(keywords) # join keywords with %20

  def createparam(self): # create param array
    self.params=[]
    self.params.append("limit="+str(self.limit))
    self.params.append("quality="+self.quality)
    self.params.append("rating="+str(self.rating))
    self.params.append("genre="+self.genre)
    self.params.append("sort="+self.sort)
    self.params.append("order="+self.order)
    self.params.append("keywords="+self.keywords)

  def request(self,params):
    prereq=request_module.Request(self.url+"?"+"&".join(params)) # join param array with "&"
    req=request_module.urlopen(prereq)  # get list
    resp=req.read().decode() # read, decode and json.load it
    self.jsondict=json.loads(resp)




# main function
if __name__=='__main__':
  # get options
  opts,args=optparser()
  if len(args)!=0: # if search string given
    ysearch=Yify(keywords=args)  # create class with keywords
  elif len(opts)>0:  # if no search string given, but options there, create class with no keywords (default)
    ysearch=Yify()
  else:
    usage("please input some options or arguments") # else, usage

  for p,a in opts: # parsing options + values
    if p in ["-a","--autoadd"]:
      autoadd=1 # autoaddoptionflag
    if p in ["-t","--torrenturl"]:
      torurl=1 # torrenturlflag
    if p in ["-l","--limit"]:
      ysearch.set_limit(a)
    if p in ["-q","--quality"]:
      ysearch.set_quality(a)
    if p in ["-r","--rating"]:
      ysearch.set_rating(a)
    if p in ["-g","--genre"]:
      ysearch.set_genre(a)
    if p in ["-s","--sort"]:
      ysearch.set_sort(a)
    if p in ["-o","--order"]:
      ysearch.set_order(a)
    if p in ["-c","--command"]:
      if a:
        config(a)
      else:
        error("you must define a command")
  # config
  command=""
  try:
    browser=os.environ["BROWSER"]
  except KeyError:
    error("Please define your environment variable $BROWSER first")

  command or usage("please first set your command and browser values") # exit if no command or browser

  ysearch.createparam() # create params list
  try:
    ysearch.request(ysearch.params)  # try the request or die
  except URLError:
    error("there was an error contacting the service")
  output(ysearch.jsondict) # call output function with json dict/array of yify class
  try:
    torurl
    dictkey="TorrentUrl"
  except NameError:
    dictkey="TorrentMagnetUrl"
  toradd(command,ysearch.jsondict['MovieList'][userinput(ysearch.jsondict['MovieCount'])-1][dictkey])

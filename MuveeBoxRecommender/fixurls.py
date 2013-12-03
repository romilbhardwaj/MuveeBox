import json
import urllib2

readdb = open('u.item', 'r')
fixeddb = open('ufixed.item', 'w')
notfoundfile = open('unotfound.item', 'w')

for line in readdb:
	ogline = line
	try:
		line=line.split('|')
		tofind = line[1][:-6].replace(" ", "%20")
		tofind = "".join(tofind.split())
		searchurl="http://www.omdbapi.com/?t=" + tofind
		print tofind
		movielist = json.load(urllib2.urlopen(searchurl))
		if(movielist['Response']=="False"):
			print "Not found in omdb, Searching in MyMovieApi"
			searchurl="http://mymovieapi.com/?title="+tofind+"&type=json&plot=simple&episode=1&limit=1&yg=0&mt=none&lang=en-US&offset=&aka=simple&release=simple&business=0&tech=0"
			movielist = json.load(urllib2.urlopen(searchurl))
			try:
				if (movielist['code']==404):
					print "No IMDB Data found for " + tofind
					notfoundfile.write(ogline)
					continue
			except TypeError:
				imdbmovie = movielist[0]
				line[4]=imdbmovie['imdb_url']
				line.insert(1, imdbmovie['imdb_id'])
				line = str("|".join(line))
				fixeddb.write(line)
		else:
			imdbmovie = movielist
			line[4]="http://www.imdb.com/title/" + imdbmovie['imdbID']
			line.insert(1, imdbmovie['imdbID'])
			line = str("|".join(line))
			fixeddb.write(line)
	except NameError:
		print "NameError. This should not happen man!"

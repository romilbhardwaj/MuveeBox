import json
import urllib2

f = open('u.item', 'r')
ff = open('ufixed.item', 'w')

for line in f:
	ogline = line
	try:
		line=line.split('|')
		print line
		tofind = line[1]
		searchurl="http://mymovieapi.com/?title="+tofind+"&type=json&plot=simple&episode=1&limit=1&yg=0&mt=none&lang=en-US&offset=&aka=simple&release=simple&business=0&tech=0"
		movielist = json.load(urllib2.urlopen(searchurl))
		imdbmovie = movielist[0]
		line[4]=imdbmovie['imdb_url']
		line.insert(1, imdbmovie['imdb_id'])
		line = str("|".join(line))
		print type(line)
		ff.write(line)
		print line
	except ValueError:
			print "No IMDB Data found for " + ogline
			ff.write(ogline)
	except KeyError:
			print "No IMDB Data found for " + ogline
			ff.write(ogline)


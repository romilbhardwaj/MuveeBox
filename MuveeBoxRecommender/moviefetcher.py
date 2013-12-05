# Using http://imdbpy.sourceforge.net/ and https://github.com/pythonforfacebook/facebook-sdk

import facebook
#import imdb NOT WORKING!
import json
import urllib2

fixeddb = open('usermovies.txt', 'w')
usergenres = open('usermoviegenres.txt', 'w')

def genrelist(moviegenres):
	genrelist = ['unknown','Action','Adventure','Animation','Children\'s','Comedy','Crime','Documentary','Drama','Fantasy','Film Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
	genreflags = dict.fromkeys(genrelist, 0)
	for genre in moviegenres:
		genreflags[genre]=1
	return [genreflags['unknown'],genreflags['Action'],genreflags['Adventure'],genreflags['Animation'],genreflags['Children\'s'],genreflags['Comedy'],genreflags['Crime'],genreflags['Documentary'],genreflags['Drama'],genreflags['Fantasy'],genreflags['Film Noir'],genreflags['Horror'],genreflags['Musical'],genreflags['Mystery'],genreflags['Romance'],genreflags['Sci-Fi'],genreflags['Thriller'],genreflags['War'],genreflags['Western']]
	
#Given a FB account and Graph API token, this inputs the individual movie ratings returns the dictionary of the movies with imdb_id as the key, and a dict of imdb_rating, genres_vector, user_rating (keys) as the value
def getmovieratings(account, token):
	graph = facebook.GraphAPI(token)
	#ia = imdb.IMDb()
	movies = graph.get_connections(account, "movies")
	usermovieinfo={}
	i=1

	for movie in movies['data']:
		try:
			if (i>11):
				break
			usermovie = {}
			moviename = movie['name']
			tofind=moviename
			searchurl="http://www.omdbapi.com/?t=" + urllib2.quote(tofind)
			movielist = json.load(urllib2.urlopen(searchurl))
			if(movielist['Response']=="False"):
				print "Not found in omdb, Searching in MyMovieApi"
				searchurl="http://mymovieapi.com/?title="+tofind+"&type=json&plot=simple&episode=1&limit=1&yg=0&mt=none&lang=en-US&offset=&aka=simple&release=simple&business=0&tech=0"
				movielist = json.load(urllib2.urlopen(searchurl))
				try:
					if (movielist['code']==404):
						print "No IMDB Data found for " + tofind
						continue
				except TypeError:
					imdbmovie = movielist[0]
					userrating = input("Enter your rating for " + imdbmovie['title'])
					op = "945\t" + str(imdbmovie['imdb_id']) + "\t" + str(userrating) +  "\t" + str(i) + "\n"
					genreop = imdbmovie['imdb_id']
					for genre in genrelist(imdbmovie['genre']):
						genreop = genreop + "\t" + str(genre)
					genreop = genreop + "\n"		
					usergenres.write(genreop)				
					i+=1
					fixeddb.write(op)
			else:
				imdbmovie = movielist
				userrating = input("Enter your rating for " + imdbmovie['Title'])
				op = "945\t" + str(imdbmovie['imdbID']) + "\t" + str(userrating) +  "\t" + str(i) + "\n"
				genreop = imdbmovie['imdbID']
				for genre in genrelist(imdbmovie['Genre'].split(", ")):
					genreop = genreop + "\t" + str(genre)
				genreop = genreop + "\n"
				usergenres.write(genreop)
				i+=1
				fixeddb.write(op)
		except KeyError:
			print "No IMDB Data found for " + moviename
	return usermovieinfo

account = raw_input('Enter your account name (eg apoorva.mittal2)')
token="CAACEdEose0cBANY4EtNN4PWSVbpz29AcdrFJ19iBzLL32V0RZCTo64b6TTdVegJFgzoG952pZCepoMPqhGHpdwiOcZAlFH11bzxbzvZCvFZC3wb8reczTkDkMDYOpeZBHrZBUqcamZAFyIaxnmulxaDyYOKbUhmZCjbbB5ddrYZAweJqnFHwHgcBeu2jGKNViJ37YZD"
print getmovieratings(account, token)

# Using http://imdbpy.sourceforge.net/ and https://github.com/pythonforfacebook/facebook-sdk

import facebook
#import imdb NOT WORKING!
import json
import urllib2

fixeddb = open('usermovies.txt', 'w')
usergenres = open('usermoviegenres.txt', 'w')
token="CAACEdEose0cBANqUvOOdsnQLL1fDuHgo6KK0e5ZALrfcuP7NsqPWb2kulSCGq4FjYGtDFky26aLD32WTHfppgmwwcTBx36YQkfvBJdWwSiNFZCQxYSyShiyLkDtZAZA9foS1hWZAUaneMOpEq2kbGlZCdG5F2JaZBLA77Y5VIvrpzK9qmOTzPMwnMHuEGpQHJ8ZD"

fixed_items = {} # keys: DB ID, values: IMDB ID
reverse_fixed_items = {} # keys: IMDB ID, values: DB ID

fbaba = open('ufixed.item', 'r')

for line in fbaba.readlines():
	fixed_items[int(line.split('|')[0])] = line.split('|')[1]
	reverse_fixed_items[line.split('|')[1]] = int(line.split('|')[0])

fbaba.close()

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
			if (i>6):
				break
			usermovie = {}
			moviename = movie['name']
			print ("\nSearching for " + moviename)
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
					if imdbmovie['imdb_id'] in reverse_fixed_items:				
						
						userrating = input("Enter your rating for " + imdbmovie['Title'] + ": ")
						op = "945\t" + str(int(reverse_fixed_items[imdbmovie['imdb_id']])) + "\t" + str(userrating) +  "\t" + str(i) + "\n"
						i+=1
					else:
						print (moviename + "Movie not found in the DB")
						continue
					genreop = imdbmovie['imdb_id']
					for genre in genrelist(imdbmovie['genre']):
						genreop = genreop + "\t" + str(genre)
					genreop = genreop + "\n"		
					usergenres.write(genreop)
					fixeddb.write(op)
			else:
				imdbmovie = movielist
				if imdbmovie['imdbID'] in reverse_fixed_items:
					
					userrating = input("Enter your rating for " + imdbmovie['Title'] + ": ")
					op = "945\t" + str(int(reverse_fixed_items[imdbmovie['imdbID']])) + "\t" + str(userrating) +  "\t" + str(i) + "\n"
					i+=1
				else:
					print (moviename + "Movie not found in the DB")
					continue
				genreop = imdbmovie['imdbID']
				for genre in genrelist(imdbmovie['Genre'].split(", ")):
					genreop = genreop + "\t" + str(genre)
				genreop = genreop + "\n"
				usergenres.write(genreop)
				fixeddb.write(op)
		except KeyError:
			print "No IMDB Data found for " + moviename
		except ValueError:
			print "No IMDB Data found for " + moviename
	fixeddb.close()
	return usermovieinfo
	
def getmovietitles(imdbids):
	print "\nHere are some of the movies you should watch: \n"
	for imdbid in imdbids:
		searchurl="http://mymovieapi.com/?id=" + imdbid + "&type=json&plot=simple&episode=1&lang=en-US&aka=simple&release=simple&business=0&tech=0"
		movielist = json.load(urllib2.urlopen(searchurl))
		imdbmovie = movielist
		try:
			print str(imdbmovie['title'])
		except KeyError:
			continue

account = raw_input('Enter your account name (eg apoorva.mittal2) ')
getmovieratings(account, token)
#print 'FLAG'

from main_recommender import recommender1
finalList = recommender1('usermovies.txt')

getmovietitles(finalList)


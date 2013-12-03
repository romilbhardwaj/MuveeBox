# Using http://imdbpy.sourceforge.net/ and https://github.com/pythonforfacebook/facebook-sdk

import facebook
#import imdb NOT WORKING!
import json
import urllib2
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

	for movie in movies['data']:
		try:
			usermovie = {}
			moviename = movie['name']
			print moviename
			searchurl="http://mymovieapi.com/?title="+moviename+"&type=json&plot=simple&episode=1&limit=1&yg=0&mt=none&lang=en-US&offset=&aka=simple&release=simple&business=0&tech=0"
			movielist = json.load(urllib2.urlopen(searchurl))
			imdbmovie = movielist[0]
			print "\nIMDB Data:\n"
			print "\nTitle: "+imdbmovie['title']
			print "\nRating: "+str(imdbmovie['rating'])
			print "\nURL: "+imdbmovie['imdb_url']
			userrating = input("Enter your rating ")
			#print genrelist(imdbmovie['genres'])
			usermovie['imdb_rating']=imdbmovie['rating']
			usermovie['genres_vector']=genrelist(imdbmovie['genres'])
			usermovie['user_rating']=userrating
			usermovieinfo[imdbmovie['imdb_id']] = usermovie
		except ValueError:
			print "No IMDB Data found for " + moviename
		except KeyError:
			print "No IMDB Data found for " + moviename
	return usermovieinfo

account = raw_input('Enter your account name (eg apoorva.mittal2)')
token="CAACEdEose0cBADnbYodh3EeuJEUggvhUI6qpVBC5kwPKFHZArY6OHG2ZBBJqYZAvtzNKz8zWOUtv3o8KTUT7zaAm9ZCc8kfPVg3O3ONeZA4nnwiBlC3L05TgsMr5EKUPvSnuzQw9ontnjnMA9e7riUUpBZBrVoZAKjZA4AGixq4mPjU1GK3Xup0swlyK3KoGgisZD"
#print getmovieratings(account, token)
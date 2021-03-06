'''
Created on Dec 1, 2013
@author: Apoorva, Amol (zyada accha)
'''

import re
import sys
import time
import operator
from math import sqrt
from math import cos
from pprint import pprint

class itemRecommender():
	'''
	classdocs
	'''
	def __init__(self):
		self.testdata = {}
		self.items = {}
		self.similarity = {}
		self.topSimilarity = []
		movieGenres = [
			'unknown',
			'Action',
			'Adventure',
			'Animation',
			'Children\'s',
			'Comedy',
			'Crime',
			'Documentary',
			'Drama',
			'Fantasy',
			'Film Noir',
			'Horror',
			'Musical',
			'Mystery',
			'Romance',
			'Sci-Fi',
			'Thriller',
			'War',
			'Western'
			]
	
	def loadTestDB(self, path, database):
		i = 0
		file = open(path, 'r')
		for line in file:
			i += 1
			fields = line
			fields = re.split('\t| |  |;|:|   ',line)
			user = int(fields[0])  
			movie = int(fields[1])
			rating = int(fields[2])
			if user in database:
				currentRatings = database[user]
			else:
				currentRatings = {}
			currentRatings[movie] = rating
			#print(currentRatings)
			database[user] = currentRatings
		file.close()
	
	def loadMovieDB(self, path, database):
		i = 0
		file = open(path, 'r')
		for line in file:
			i += 1
			fields = [x.split('|') for x in line.split('||')]
			fields = fields[0] + fields[1]
			movie = int(fields[0])
			title = fields[1]
			#release_date = fields[2]
			#url = fields[3]
			genre = [int(x) for x in fields[4:]]
			database[movie] = [title, genre] 
		file.close()
	
	def getMovie(self, movieID):
		return self.items[movieID]
			
	def obtainGenre(self, item):
		if self.items.has_key(item):
			return self.items[item][1]
		else:
			return 0
	
	def multiplier(self, item1, item2):
	# item1 is the movie the user rated
		genre1 = self.obtainGenre(item1)
		genre2 = self.obtainGenre(item2)
		result = 0
		for i in range(19):
			result += genre1[i] * genre2[i] * self.testdata[945][item1]
		return(result)
	
	def calculateSimilarity(self):
		#pprint(self.testdata)
		for item2 in self.items:
			if not self.testdata[945].has_key(item2):
				self.similarity[item2] = 0
				for item1 in self.testdata[945]:
					self.similarity[item2] = self.similarity[item2] + self.multiplier(item1, item2)
		self.topSimilarity = sorted(self.similarity, key = self.similarity.get, reverse = True)
		
	def obtain100movies(self):
		self.top100= [0 for x in range(100)]
		#f=open('good100movies.txt','w')
		for i in range(100):
			
			self.top100[i]=self.topSimilarity[i]
			#f.write(str(self.top100[i])+'\n') 
		#pprint(self.top100)
		
		# python will convert \n to os.linesep
		

	def getRecommendations(self):
		return(self.top100)
		
	def main(self):
		self.loadMovieDB('u.item', self.items)
		self.loadTestDB('sample.data', self.testdata)
		print self.testdata
		self.calculateSimilarity()
		self.obtain100movies()
		#pprint(self.items)
		#pprint(self.testdata)
		'''
		for key in self.testdata[945].keys():
			print key
		'''
		'''
		for line in f.readlines():
			print count, self.items[int(line.strip('\n'))][0]
			count += 1
		'''
		#pprint(self.topSimilarity)
		self.getRecommendations()
		
#r = itemRecommender()
#r.main()


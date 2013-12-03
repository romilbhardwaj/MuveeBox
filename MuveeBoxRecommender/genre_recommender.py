'''
Created on Dec 1, 2013
@author: Apoorva, Amol (zyada accha)
'''

import re
import sys
import time
from math import sqrt
from math import cos
from pprint import pprint

class recommender():
	
	def __init__(self):
		self.items = {}
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
	
	def loadBookDB(self,path,database):
	  
		#print("Database Loading ")
		
		i = 0
		#file=open("C:/Users/Apoorva/Desktop/CF/Dataset/ml-100k/u.data",'r')
		file=open(path,'r')
		# print("inside Database 1")
		for line in file:
			i += 1
			fields=line
			fields = re.split('\t| |  |;|:|   ',line)
			user=int(fields[0])  
			movie = int(fields[1])
			rating= int(fields[2])
			if user in database:
				currentRatings = database[user]
			else:
				currentRatings = {}
			currentRatings[movie] = rating
			# print(currentRatings)
			database[user] = currentRatings
		file.close()
	
	def pearson(self,rating1, rating2):
		#print("Pearson entrance")
		sum_xy = 0
		sum_x = 0
		sum_y = 0
		sum_x2 = 0
		sum_y2 = 0
		n = 0
	 
		for key in rating1:
			if key in rating2:
			
			  n += 1
			  x = rating1[key]
			
			  y = rating2[key]
			  sum_xy =sum_xy+x*y
			  
			  sum_x += x
			  sum_y += y
			  sum_x2 += pow(x, 2)
			  sum_y2 += pow(y, 2)
		if n == 0:
			return 0
		denominator = sqrt(((n*sum_x2)-(sum_x*sum_x))*((n*sum_y2)-(sum_y*sum_y)))
		numerator= ((n*sum_xy)-(sum_x*sum_y))
		#print numerator
		if denominator == 0:
			return 0
		else:
			return numerator / float(denominator)
	
	"""Returns distances of all the neighbors for an user"""
	def computeDistances(self, username):
		
		#print("inside CNN")
		distance=0
		distances = []
		eachDistance={}
		for instance in self.traindata:
			if instance != username:
				#print("inside CNN 4")
				distance = self.pearson(self.testdata[username],self.traindata[instance])
				
				distances.append((instance, distance))
		distances=sorted(distances, key=lambda x: x[1])
		
		distances = list(reversed(distances))
		
		return distances
	
	def calNeighbors(self,username):
		distances=self.computeDistances(username)
		k=10
		topMovies = []
		
		for i in range(10):
			count = 0
			userRatings=self.traindata[distances[i][0]]
			topUserRatings=sorted(userRatings, key=userRatings.get)
			for movie in topUserRatings:
				if movie not in topMovies and count < 2:
					topMovies.append(movie)
					count += 1
			topMovies.extend(topUserRatings)
		
		return topMovies
	
	def obtaintop20(self,username):
	
		#Reading the top 50 movies recommended by the item recommender:
		self.top50= [0 for x in range(50)]
		f=open('goodmovies.txt','r')
		i=0
		for line in f:
			movie=line.split("\n")
			self.top50[i]=movie[0]
			i+=1
		f.close()
		
		self.newtop50={}
		for item in self.top50:
			#print(item)
			item = int(item)
			rating=0
			totaldistance=0
			for user in self.traindata:
				if user!=username:
				
					userRatings=self.traindata[user]
					#pprint(userRatings)
					
					if item in userRatings.keys():
						#print(item)
						totaldistance+=  self.pearson(self.testdata[username],self.traindata[user])
						#rating += userRatings[item] *  self.pearson(self.testdata[username],self.traindata[user])
						
			for user in self.traindata:
				if user!=username:
					userRatings=self.traindata[user]
					#pprint(userRatings)
					
					if item in userRatings.keys():
						#print(item)
						
						rating += userRatings[item] *  (self.pearson(self.testdata[username],self.traindata[user]))/totaldistance 
				
			
			self.newtop50[item]=rating
		#pprint(self.newtop50)
		self.top20 = sorted(self.newtop50, key = self.newtop50.get, reverse = True)
	
	def calculateGenreScore(self, data):
		d = {}
		for user in data:
			d[user] = [0] * 19
			for movie in data[user]:
				genre = self.obtainGenre(movie)
				if genre != 0:
					for i in range(19):
						#pprint(d[user])
						d[user][i] += genre[i]
			for i in range(19):
				d[user][i] /= float(len(data[user].keys()))
		return d
	
	def obtainGenre(self, item):
		if self.items.has_key(item):
			return self.items[item][1]
		else:
			return 0
	
	def main(self):
		self.traindata={}
		self.testdata={}
		self.loadBookDB("u.data", self.traindata)
		self.loadBookDB("sample.data", self.testdata)
		self.loadMovieDB('u.item', self.items)
		self.trainGenreScore = self.calculateGenreScore(self.traindata)
		self.testGenreScore = self.calculateGenreScore(self.testdata)
		pprint(self.testGenreScore)
		pprint(self.trainGenreScore)
	   	
r = recommender()
r.main()

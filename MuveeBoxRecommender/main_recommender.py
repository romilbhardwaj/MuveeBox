from item_recommender import itemRecommender as IR
from user_recommender import recommender as UR
from genre_recommender import recommender as GR

def recommender1(testPath):
	ir = IR()
	ir.loadMovieDB('u.item', ir.items)
	ir.loadTestDB(testPath, ir.testdata)
	ir.calculateSimilarity()
	ir.obtain100movies()
	ir_list = ir.getRecommendations()

	ur = UR()
	ur.traindata = {}
	ur.testdata = {}
	ur.loadBookDB('u.data', ur.traindata)
	ur.loadBookDB(testPath, ur.testdata)
	mainuser = 945 
	ur.movies = {}
	ur.calNeighbors(mainuser)
	ur.obtaintop100(mainuser)
	ur_list = ur.top100

	gr = GR()
	gr.traindata = {}
	gr.testdata = {}
	gr.loadBookDB('u.data', gr.traindata)
	gr.loadBookDB(testPath, gr.testdata)
	gr.loadMovieDB('u.item', gr.items)
	gr.trainGenreScore = gr.calculateGenreScore(gr.traindata)
	gr.testGenreScore = gr.calculateGenreScore(gr.testdata)
	gr.calGenreDistance()
	gr.getRecommendations()
	gr_list = gr.recommendations

	ranking = {}
	
	fixed_items = {}
	
	f = open('ufixed.item', 'r')
	
	for line in f.readlines():
		fixed_items[int(line.split('|')[0])] = line.split('|')[1]
	
	f.close()
	
	for i in ir_list:
		if not ranking.has_key(i):
			ranking[i] = (100.0 / (2**ir_list.index(i)))
		else:
			ranking[i] *= (100.0 / (2**ir_list.index(i)))

	for i in ur_list:
		if not ranking.has_key(i):
			ranking[i] = (100.0 / (2**ur_list.index(i)))
		else:
			ranking[i] *= (100.0 / (2**ur_list.index(i)))

	for i in gr_list:
		if not ranking.has_key(i):
			ranking[i] = (100.0 / (2**gr_list.index(i)))
		else:
			ranking[i] *= (100.0 / (2**gr_list.index(i)))

	topMovies = sorted(ranking, key = ranking.get, reverse = True)
	
	i = 0
	j = 0
	
	finalList = []
	
	while i < 10:
		if fixed_items.has_key(topMovies[j]):
			finalList.append(fixed_items[topMovies[j]])
			i += 1
		j += 1
	
	return finalList


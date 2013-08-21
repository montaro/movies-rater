import os
from httplib2 import Http
import json
import operator
import urllib
import sys

argz = sys.argv[1:]
try:
    mdir = argz[0]
except Exception:
    print 'could not parse arguments\nusage: python movies-rater.py /home/arefaey/movies'
    exit()
os.chdir(mdir)
movies = [d for d in os.listdir('.') if os.path.isdir(d)]
print 'Total movies found: %s\n' % len(movies)

rated_movies = {}
unrated_movies = []

endpoint = "http://mymovieapi.com/?%s"
h = Http()
for movie in movies:
	try:
		params = urllib.urlencode({'title': movie, 'type':'json'})
		response, content = h.request(endpoint % params, "GET")
		jcontent = json.loads(content)
		if len(jcontent) > 0 and isinstance(jcontent, list):
			movie_details = jcontent[0]
			movie_rating = movie_details["rating"]
			rated_movies[movie] = movie_rating
		else:
			unrated_movies.append(movie)
	except ValueError:
		unrated_movies.append(movie)
		print "API response was invalid for movie: %s" % movie
	except KeyError:
		unrated_movies.append(movie)
		print "API response had no rating for movie: %s" % movie
print "\n#############################"
print "Rated Movies: %s \n" % len(rated_movies)
sorted_rated_movies = sorted(rated_movies.iteritems(), key=operator.itemgetter(1), reverse=True)
for rm in sorted_rated_movies:
	print rm

print "\n#############################"
print "Unrated Movies: %s \n" % len(unrated_movies)
for urm in unrated_movies:
	print urm
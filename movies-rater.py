#!/usr/bin/env python

import os
from httplib2 import Http
import json
import operator
import urllib
import sys
import re

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

"""
Extracting the movie name form file name and removing the noise like the "DVD", 1986, "torrent", etc..
Code is almost the same like the open source module here:
https://compscicafe.wordpress.com/2011/09/05/extracting-movie-name-regular-expression-torrent/
"""
def fix_name(movie_name):
    text1 = re.search('([^\\\]+)\.(avi|mkv|mpeg|mpg|mov|mp4)$', movie_name)
    if text1:
        movie_name = text1.group(1)
    movie_name = movie_name.replace('.', ' ').lower()
    text2 = re.search('(.*?)(dvdrip|xvid| cd[0-9]|dvdscr|brrip|divx|[\{\(\[]?[0-9]{4}).*', movie_name)
    if text2:
        movie_name = text2.group(1)
    text3 = re.search('(.*?)\(.*\)(.*)', movie_name)
    if text3:
        movie_name = text3.group(1)
    return movie_name.strip()


endpoint = "http://www.omdbapi.com/?%s"
h = Http()
for movie in movies:
    try:
        # import ipdb; ipdb.set_trace()
        movie = fix_name(movie)
        params = urllib.urlencode({'t': movie})
        response, content = h.request(endpoint % params, "GET")
        jcontent = json.loads(content)
        if bool(jcontent["Response"]):
            movie_rating = jcontent["imdbRating"]
            rated_movies[movie] = movie_rating
        else:
            unrated_movies.append(movie)
    except ValueError:
        unrated_movies.append(movie)
        print u"API response was invalid for movie: %s" % movie
    except KeyError:
        unrated_movies.append(movie)
        print u"API response had no rating for movie: %s" % movie
print "\n#############################"
print "Rated Movies: %s \n" % len(rated_movies)
sorted_rated_movies = sorted(rated_movies.iteritems(), key=operator.itemgetter(1), reverse=True)
for rm in sorted_rated_movies:
    print rm[0] + " : " + str(rm[1])

print "\n#############################"
print "Unrated Movies: %s \n" % len(unrated_movies)
for urm in unrated_movies:
    print urm
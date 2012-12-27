from __future__ import print_function

import json
import requests

IMDB_API_REQUST_URL = 'http://imdbapi.org'

class ActorComparer(object):

	def __init__(self):
		self.imdb_client = IMDBClient()

	def compare(self):

		first_movie_choice  = self._get_movie_choice_from_user('First query: ')
		second_movie_choice = self._get_movie_choice_from_user('Second query: ')
		first_movie_actors = set(first_movie_choice['actors'])
		second_movie_actors = set(second_movie_choice['actors'])
			
		common_actors = first_movie_actors & second_movie_actors

		print(
"""
Actors for %s: %s
Actors for %s: %s
Common actors: %s
""" % (
				first_movie_choice['title'],
				first_movie_actors,
				second_movie_choice['title'],
				second_movie_actors,
				common_actors
			)
		)

	def _get_movie_choice_from_user(self, prompt):
		query  = raw_input(prompt)
		results = self.imdb_client.search_by_title(query)
		self._print_results(results)
		choice = raw_input('Which is the best match? ')
		return results[int(choice)]

	def _print_results(self, results):
		for i, result in enumerate(results):
			print(
"""
Choice %i
Title: %s
Actors: %s
""" % (i, result['title'], result['actors'])
			)


class IMDBClient(object):
	def search_by_title(self, title):
		result = requests.get(
			IMDB_API_REQUST_URL,
			params={
				'q': title,
				'limit': 5
			}
		)
		return json.loads(result.text)

if __name__ == '__main__':
	actor_comparer = ActorComparer()
	actor_comparer.compare()

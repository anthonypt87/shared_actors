import mock
import unittest

import shared_actors


class SharedActorsUnitTestCase(unittest.TestCase):

	def setUp(self):
		self.actor_comparer = shared_actors.ActorComparer()
		self._patch_io()
		self._patch_client()

	def _patch_io(self):
		self.mock_raw_input = mock.patch(
			'__builtin__.raw_input',
			side_effect=['first_query', 0, 'second_query', 1]
		).start()
		self.mock_print = mock.patch(
			'__builtin__.print'
		).start()

	def _patch_client(self):
		self.search_by_title = mock.patch(
			'shared_actors.IMDBClient.search_by_title',
			side_effect=[
				[
					{
						'title': 'Movie 1',
						'actors': ['bob', 'john']
					}
				],
				[
					{
						'title': 'Movie 2',
						'actors': ['jane', 'john']
					},
					{
						'title': 'Movie 3',
						'actors': ['bob', 'crawfish']
					}
				]

			]
		).start()

	def test_compare(self):
		self.actor_comparer.compare()
		self.mock_print.assert_called_with(
"""
Actors for Movie 1: set(['bob', 'john'])
Actors for Movie 3: set(['crawfish', 'bob'])
Common actors: set(['bob'])
"""
		)


class IMDBIntegrationTestCase(unittest.TestCase):
	def test_search_by_title(self):
		imdb_client = shared_actors.IMDBClient()
		results = imdb_client.search_by_title('once upon a time')
		self.assertTrue(len(results), 5)

if __name__ == '__main__':
	unittest.main()

from os import path
import unittest

from comp62521.database import database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 1)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(len(db.publications), 1)

    def test_get_all_authors(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(db.get_all_authors(), [u'AUTHOR1', u'AUTHOR2'])

    def test_get_coauthor_data(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        start = db.min_year
        end = db.max_year
        self.assertEqual(db.get_coauthor_data(start, end, 'wrong pub type'), (('Author', 'Co-Authors'), []))
        self.assertEqual(db.get_coauthor_data(start, end, 0), (('Author', 'Co-Authors'), [[u'AUTHOR1 (1)',
                                                                                           u'AUTHOR2 (1)'],
                                                                                          [u'AUTHOR2 (1)',
                                                                                           u'AUTHOR1 (1)']]))

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary_average(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        self.assertEqual(db.get_publication_summary_average(1), (('Details', 'Conference Paper', 'Journal', 'Book',
                                                                  'Book Chapter', 'All Publications'),
                                                                 [['Median authors per publication', 1.5, 0, 1, 0, 1],
                                                                  ['Median publications per author', 2.0, 0.0, 0.0, 0.0,
                                                                   2.0]]))
        self.assertEqual(db.get_publication_summary_average(2), (('Details', 'Conference Paper', 'Journal', 'Book',
                                                                  'Book Chapter', 'All Publications'),
                                                                 [['Mode authors per publication', [1], [], [1], [],
                                                                   [1]],
                                                                  ['Mode publications per author', [1.0], [0.0], [0.0],
                                                                   [0.0], [2.0]]]))

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
                         "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
                         "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
                         "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
                         "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
                         "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
                         "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
                         "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
                         "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
                         "incorrect number of authors")
        self.assertEqual(data[0][-1], 1,
                         "incorrect total")

    def test_get_average_authors_per_publication_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(db.get_average_authors_per_publication_by_year(2), (('Year', 'Conference papers', 'Journals',
                                                                              'Books', 'Book chapters',
                                                                              'All publications'),
                                                                             [[9999, [2], [], [], [], [2]]]))
        self.assertEqual(db.get_average_authors_per_publication_by_year(0), (('Year', 'Conference papers', 'Journals',
                                                                              'Books', 'Book chapters',
                                                                              'All publications'),
                                                                             [[9999, 2.0, 0, 0, 0, 2.0]]))

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
                         "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
                         "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
                         "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
                         "incorrect year in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
                         "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
                         "incorrect year in result")
        self.assertEqual(data[0][1], 2,
                         "incorrect number of authors in result")

    def test_get_author_stats(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_author_stats()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(header, ("Author", "Number of conference papers",
                                  "Number of journals", "Number of books",
                                  "Number of book chapters", "Total publications", "Coauthors", "First", "Last"))
        self.assertEqual(data[0], [u'author1', 2, 0, 0, 0, 2, 1, 1, 0])
        self.assertEqual(data[1], [u'author2', 1, 0, 0, 0, 1, 1, 0, 1])

    def test_get_first_last_sole_stats(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        header, data = db.get_first_last_sole()
        self.assertEqual(header, ("Name", "First Author", "Last Author", "Sole Author"))
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(data[0], ("Stefano Ceri", 78, 25, 8))
        self.assertEqual(data[4][1], 0,
                         "The first authors ")
        self.assertEqual(data[4][2], 2,
                         "The last authors")
        self.assertEqual(data[4][3], 0,
                         "The sole author")

    def test_get_first_author_stat(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        first = db.get_first_author_stat(db.publications, 'Stefano Ceri')
        self.assertEqual(first, 78)
        pubs = [pub for pub in db.publications if pub.pub_type == 2]
        first = db.get_first_author_stat(pubs, 'Stefano Ceri')
        self.assertEqual(first, 3)
        pubs = [pub for pub in db.publications if pub.pub_type == 3]
        first = db.get_first_author_stat(pubs, 'Stefano Ceri')
        self.assertEqual(first, 4)

    def test_get_last_author_stat(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        last = db.get_last_author_stat(db.publications, 'Stefano Ceri')
        self.assertEqual(last, 25)

    def test_get_sole_author_stat(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        last = db.get_sole_author_stat(db.publications, 'Stefano Ceri')
        self.assertEqual(last, 8)

    def test_get_all_author_stats(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        stats = db.get_all_author_stats('Stefano Ceri')
        self.assertEqual(stats, (('Statistic', 'Conference Paper', 'Journal', 'Book', 'Book Chapter', 'Overall'),
                                 [['Publication', 100, 94, 6, 18, 218], ['First', 28, 43, 3, 4, 78],
                                  ['Last', 10, 10, 0, 5, 25], ['Sole', 7, 0, 0, 1, 8],
                                  ['Coauthors', 110, 152, 14, 40, 230]]))

    def test_get_author_pub_stat(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        count = db.get_author_pub_stat(db.publications, 'Stefano Ceri')
        self.assertEqual(count, 218)

    def test_get_coauthor_stat(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        count = db.get_coauthor_stat(db.publications, 'Stefano Ceri')
        self.assertEqual(count, 230)

    def test_get_matching_authors(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        authors = db.get_matching_authors('')
        self.assertEqual(authors, '')
        authors = db.get_matching_authors('Stefano Ceri')
        self.assertEqual(authors, [[['Publication', 100, 94, 6, 18, 218], ['First', 28, 43, 3, 4, 78],
                                    ['Last', 10, 10, 0, 5, 25], ['Sole', 7, 0, 0, 1, 8],
                                    ['Coauthors', 110, 152, 14, 40, 230], u'Stefano Ceri']])
        authors = db.get_matching_authors('Stefano')
        self.assertEqual(authors, [u'Stefano Butti', u'Stefano Ceri',
                                   u'Stefano Crespi-Reghizzi', u'Stefano Gevinti',
                                   u'Stefano Paraboschi'])
        authors = db.get_matching_authors('  Stefano  ')
        self.assertEqual(authors, [u'Stefano Butti', u'Stefano Ceri',
                                   u'Stefano Crespi-Reghizzi', u'Stefano Gevinti',
                                   u'Stefano Paraboschi'])

    def test_sort_authors_by_precedence(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        authors = db.sort_authors_by_precedence(["Brian Sam Alice", "Sam Alice", "Samuel Alice", "Alice Sam Brian",
                                                 "Sam Brian", "Samuel Brian", "Alice Esam", 'Brian Esam', 'Alice Sam',
                                                 'Brian Sam', 'Alice Sammer', 'Brian Sammer', 'Alice Samming',
                                                 'Brian Samming'], 'sam')
        self.assertEqual(authors, ['Alice Sam', 'Brian Sam', 'Alice Sammer',
                                   'Brian Sammer', 'Alice Samming', 'Brian Samming',
                                   'Sam Alice', 'Sam Brian', 'Samuel Alice',
                                   'Samuel Brian', 'Brian Sam Alice', 'Alice Sam Brian',
                                   'Alice Esam', 'Brian Esam']
)

    def test_sort_author_group_by_name(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        authors = db.sort_authors_by_precedence(["Brian Sam Alice", "Sam Alice", "Samuel Alice", "Alice Sam Brian",
                                                 "Sam Brian", "Samuel Brian", "Alice Esam", 'Brian Esam', 'Alice Sam',
                                                 'Brian Sam', 'Alice Sammer', 'Brian Sammer', 'Alice Samming',
                                                 'Brian Samming'], 'sam')
        authors = db.sort_author_group_by_name(authors, 2)
        self.assertEqual(authors,
                         ['Alice Sam Brian', 'Alice Esam', 'Alice Sam', 'Alice Sammer', 'Alice Samming',
                          'Brian Sam Alice', 'Brian Esam', 'Brian Sam', 'Brian Sammer', 'Brian Samming', 'Sam Alice',
                          'Sam Brian', 'Samuel Alice', 'Samuel Brian'])

    def test_get_all_author_network(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        network = db.get_all_author_network()
        self.assertEqual(network, {0 : {1}, 1: {0}})

    def test_get_all_author_network_graph(self):
        import networkx as nx
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        graph = db.get_all_author_network_graph()
        nodes = graph.nodes()
        self.assertEqual(nodes, [0, 1])
        edges = graph.edges()
        self.assertEqual(edges, [(0, 1)])
        attributes = nx.get_node_attributes(graph, 'name')
        self.assertEqual(attributes, {0: u'AUTHOR1', 1: u'AUTHOR2'})

    def test_get_author_id(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        author1_id = db.get_author_id('author2')
        self.assertEqual(author1_id, 1)

    def test_get_degree_of_separation(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        graph = db.get_all_author_network_graph()
        degree = db.get_degree_of_separation(graph, 'author1', 'author3')
        self.assertEqual(degree, None)

    def test_get_all_shortest_paths(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "publications_small_sample.xml")))
        graph = db.get_all_author_network_graph()
        paths = db.get_all_shortest_paths(graph, 'Sean Bechhofer', 'Simon Harper')
        self.assertEqual(paths, None)

    def test_get_network_data(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(db.get_network_data(), ([[u'AUTHOR1', 1], [u'AUTHOR2', 1]], {(0, 1)}))



if __name__ == '__main__':
    unittest.main()

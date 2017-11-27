from comp62521.statistics import average
import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]


class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors


class Author:
    def __init__(self, name):
        self.name = name


class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2


class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print "Error reading file (" + e.getMessage() + ")"
        infile.close()

        for p in self.publications:
            if self.min_year is None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year is None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def get_all_authors(self):
        return self.author_idx.keys()

    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year is None or p.year >= start_year) and
                    (end_year is None or p.year <= end_year) and
                    (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = {a2}

        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        data = []
        for a in coauthors:
            data.append([display(self, coauthors, a),
                         ", ".join([
                             display(self, coauthors, ca) for ca in coauthors[a]])])

        return header, data

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [func(auth_per_pub[i]) for i in np.arange(4)] + [func(list(itertools.chain(*auth_per_pub)))]
        return header, data

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [func(pub_per_auth[:, i]) for i in np.arange(4)] + [func(pub_per_auth.sum(axis=1))]
        return header, data

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [func(ystats[:, i]) for i in np.arange(4)] + [func(ystats.sum(axis=1))]
        return header, data

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [[set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1)]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([[len(S) for S in y] for y in yauth])

        func = Stat.FUNC[av]

        data = [func(ystats[:, i]) for i in np.arange(5)]
        return header, data

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
            + [func(auth_per_pub[i]) for i in np.arange(4)]
            + [func(list(itertools.chain(*auth_per_pub)))],
            [name + " publications per author"]
            + [func(pub_per_auth[:, i]) for i in np.arange(4)]
            + [func(pub_per_auth.sum(axis=1))]]
        return header, data

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
                  "Journal", "Book", "Book Chapter", "Total")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [len(a) for a in alist] + [len(ua)]]
        return header, data

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapters", "All publications")

        astats = [[[], [], [], []] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [[self.authors[i].name]
                + [func(L) for L in astats[i]]
                + [func(list(itertools.chain(*astats[i])))]
                for i in range(len(astats))]
        return header, data

    def get_publications_by_author(self):
        header = ("Author", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapters", "Total")

        astats = [[0, 0, 0, 0] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])]
                for i in range(len(astats))]
        return header, data

    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
                  "Journals", "Books",
                  "Book chapters", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [[y]
                + [func(L) for L in ystats[y]]
                + [func(list(itertools.chain(*ystats[y])))]
                for y in ystats]
        return header, data

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapters", "Total")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [[y] + ystats[y] + [sum(ystats[y])] for y in ystats]
        return header, data

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
                  "Journals", "Books",
                  "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [[y]
                + [func(ystats[y][:, i]) for i in np.arange(4)]
                + [func(ystats[y].sum(axis=1))]
                for y in ystats]
        return header, data

    def get_author_totals_by_year(self):
        header = ("Year", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapters", "Total")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [[y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
                for y in ystats]
        return header, data

    def add_publication(self, pub_type, title, year, authors):
        if year is None or len(authors) == 0:
            print "Warning: excluding publication due to missing information"
            print "    Publication type:", PublicationType[pub_type]
            print "    Title:", title
            print "    Year:", year
            print "    Authors:", ",".join(authors)
            return
        if title is None:
            print "Warning: adding publication with missing title [ %s %s (%s) ]" % (
                PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year is None or year < self.min_year:
            self.min_year = year
        if self.max_year is None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [(self.authors[key].name, data[key])
                for key in data]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [[self.authors[i].name, -1] for i in range(na)]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return nodes, links

    def first_last_author(self, name):
        name = ' '.join(name.strip().split())
        first = 0
        last = 0
        sole = 0
        for pub in self.publications:
            if self.authors[pub.authors[0]].name.lower() == name.lower():
                if len(pub.authors) == 1:
                    sole += 1
                else:
                    first += 1
            if self.authors[pub.authors[len(pub.authors) - 1]].name.lower() == name.lower():
                if len(pub.authors) != 1:
                    last += 1
        return first, last, sole

    def get_first_last_sole(self):
        header = ("Name", "First Author", "Last Author", "Sole Author")
        data = []
        for i in range(len(self.authors)):
            first, last, sole = self.first_last_author(self.authors[i].name)
            data.append((self.authors[i].name, first, last, sole))
        return header, data

    def get_author_stats(self):
        header, data = self.get_publications_by_author()
        header = ("Author", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapters", "Total publications", "Coauthors", "First", "Last")
        for i in range(len(data)):
            first, last, _ = self.first_last_author(data[i][0])
            coauthors = self.get_coauthor_details(data[i][0])
            data[i].append(len(coauthors) - 1)
            data[i].append(first)
            data[i].append(last)
        return header, data

    def get_first_author_stat(self, pubs, name):
        first = 0
        for p in pubs:
            if self.authors[p.authors[0]].name.lower() == name.lower():
                if len(p.authors) != 1:
                    first += 1
        return first

    def get_last_author_stat(self, pubs, name):
        last = 0
        for p in pubs:
            if self.authors[p.authors[len(p.authors) - 1]].name.lower() == name.lower():
                if len(p.authors) != 1:
                    last += 1
        return last

    def get_sole_author_stat(self, pubs, name):
        sole = 0
        for p in pubs:
            if self.authors[p.authors[0]].name.lower() == name.lower():
                if len(p.authors) == 1:
                    sole += 1
        return sole

    def get_author_pub_stat(self, pubs, name):
        count = 0
        for p in pubs:
            for a in p.authors:
                if self.authors[a].name.lower() == name.lower():
                    count += 1
        return count

    def get_coauthor_stat(self, pubs, name):
        count = 0
        coauthors = set()
        for p in pubs:
            for a in p.authors:
                if self.authors[a].name.lower() == name.lower():
                    for a2 in p.authors:
                        if a != a2:
                            coauthors.add(a2)
        count += len(coauthors)
        return count

    def get_all_author_stats(self, name):
        header = ("Statistic", "Conference Paper", "Journal", "Book", "Book Chapter", "Overall")
        name = ' '.join(name.strip().split())
        publications, first, last, sole, coauthor = ["Publication"], ["First"], ["Last"], ["Sole"], ["Coauthors"]
        for i in range(5):
            pubs = [pub for pub in self.publications if pub.pub_type == i or i == 4]
            publications.append(self.get_author_pub_stat(pubs, name))
            first.append(self.get_first_author_stat(pubs, name))
            last.append(self.get_last_author_stat(pubs, name))
            sole.append(self.get_sole_author_stat(pubs, name))
            coauthor.append(self.get_coauthor_stat(pubs, name))
        return header, [publications, first, last, sole, coauthor]

    def get_matching_authors(self, string):
        if string == "":
            return ''
        else:
            return self.sort_authors_by_precedence([author for author in self.get_all_authors()
                                                    if string.lower() in author.lower()], string)

    def sort_authors_by_precedence(self, results, string):
        out = []
        # last names
        out += self.sort_author_group_by_name([author for author in results
                                         if string.lower() == author.split()[-1].lower()], 0)
        out += self.sort_author_group_by_name(
            [author for author in results if string.lower() in author.split()[-1].lower()
             and author.split()[-1].lower().find(string.lower()) == 0 and author not in out], 1)
        # first names
        out += self.sort_author_group_by_name([author for author in results
                                         if string.lower() == author.split()[0].lower()], 1)
        out += self.sort_author_group_by_name(
            [author for author in results if string.lower() in author.split()[0].lower()
             and author.split()[0].lower().find(string.lower()) == 0 and author not in out], 2)
        # middle names
        out += self.sort_author_group_by_name([author for author in results
                                         if string.lower() in [x.lower() for x in author.split()[1:-1]]], 1)
        # string at index 1 in last name
        out += self.sort_author_group_by_name([author for author in results if string.lower() in author.split()[-1].lower()
                                         and author.split()[-1].lower().find(string.lower()) == 1], 0)
        #  the rest
        out += self.sort_author_group_by_name([author for author in results if author not in out], 1)
        if len(out) == 1:
            _, data = self.get_all_author_stats(out[0])
            data.append(out[0])
            return [data]
        else:
            return out

    def sort_author_group_by_name(self, authors, sort_type):
        if sort_type == 0:
            return sorted(authors, key=lambda name: (name.split()[0]))
        elif sort_type == 1:
            return sorted(authors, key=lambda name: (name.split()[-1], name.split()[0]))
        else:
            return sorted(authors, key=lambda name: (name.split()[0], name.split()[-1]))


class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = ["sub", "sup", "i", "tt", "ref"]
    PUB_TYPE = {
        "inproceedings": Publication.CONFERENCE_PAPER,
        "article": Publication.JOURNAL,
        "book": Publication.BOOK,
        "incollection": Publication.BOOK_CHAPTER}

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type is None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type is not None:
            self.chrs += chrs

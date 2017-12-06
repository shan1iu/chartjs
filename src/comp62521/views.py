from comp62521 import app
from database import database
from flask import (render_template, request, jsonify, json, Response)


def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([(fmt % i).rstrip('0').rstrip('.') for i in item]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result


@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "averages", 'title': "Averaged Data"}
    args["plotlink"] = "/plot/averages"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE]
    tables.append({
        "id": 1,
        "title": "Average Authors per Publication",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_authors_per_publication(i)[1])
            for i in averages]})
    tables.append({
        "id": 2,
        "title": "Average Publications per Author",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_publications_per_author(i)[1])
            for i in averages]})
    tables.append({
        "id": 3,
        "title": "Average Publications in a Year",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_publications_in_a_year(i)[1])
            for i in averages]})
    tables.append({
        "id": 4,
        "title": "Average Authors in a Year",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_authors_in_a_year(i)[1])
            for i in averages]})

    args['tables'] = tables
    args['class_6'] = "active"
    return render_template("averages.html", args=args)


@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset": dataset, "id": "coauthors", "title": "Co-Authors"}
    args["class_7"] = "active"
    args["plotlink"] = "/plot/coauthors"

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    return render_template("coauthors.html", args=args)


@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, }
    args["class_1"] = "active"
    return render_template('statistics.html', args=args)


@app.route("/author_stats")
def show_author_stats():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "author_stats", 'title': "Comprehensive Author Stats",
            "data": db.get_author_stats()}
    return render_template('author_stats.html', args=args)


@app.route("/search")
def search_for_author():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "search"}
    name = ""
    args['title'] = "Search for Author"
    if "name" in request.args:
        name = request.args.get("name")
    args["data"] = db.get_matching_authors(name)
    args["class_8"] = "active"
    return render_template('author_search.html', args=args)


@app.route("/authorstatistics/<name>")
def show_author_statistics(name):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "name": name}
    args["title"] = "Comprehensive Statistics for " + name
    args["data"] = db.get_all_author_stats(name)

    return render_template('author_statistics.html', args=args)


# @app.route("/plot/publication_summary")
# @app.route("/plot/publication_by_author")
# @app.route("/plot/publication_by_year")
# @app.route("/plot/author_by_year")
@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": status}

    if status == "publication_summary":
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()
        args["class_2"] = "active"
        args["plotlink"] = "/plot/publication_summary"

    if status == "publication_author":
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author()
        args["class_3"] = "active"
        args["plotlink"] = "/plot/publication_by_author"

    if status == "publication_year":
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()
        args["class_4"] = "active"
        args["plotlink"] = "/plot/publication_by_year"

    if status == "author_year":
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()
        args["class_5"] = "active"
        args["plotlink"] = "/plot/author_by_year"

    if status == "author_first_last_sole":
        args["title"] = "First, Last and Sole "
        args["data"] = db.get_first_last_sole()

    return render_template('statistics_details.html', args=args)


@app.route("/get_degree_static_page")
def show_degree_of_separation_static_page():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    args["title"] = "Degrees of Separation"
    args["class_9"] = "active"

    return render_template("degree_of_separation.html", args=args)


@app.route("/sprint_get_name/<name>")
def showSprintGetName(name):
    name = name.lower()
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    all_authors = db.get_all_authors()
    return_author = list()
    for author in all_authors:
        lower_author = author.lower() + ""
        if lower_author.startswith(name) or lower_author.startswith(name.upper()):
            return_author.append(author)
    # print return_author
    return jsonify({'data': return_author})


@app.route("/sprint4_get_plot/<author1>/<author2>")
def showSprintGetPlot(author1, author2):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    args["title"] = "Sprint4 Story4"
    graph = db.get_all_author_network_graph()
    path = db.get_all_shortest_paths(graph, author1, author2)
    degree = db.get_degree_of_separation(graph, author1, author2)
    # print "data : ", type(jsonify({'devices': data}))
    return jsonify({'data': path, 'degree': degree})


@app.route("/plot/publication_summary")
def showPlotPublicationSummary():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    args["title"] = "Graph - Publication Summary"
    args["gobacklink"] = "/statisticsdetails/publication_summary"
    args["class_2"] = "active"
    args["jsfunction"] = "plotPubSummary"
    return render_template("plot.html", args=args)


@app.route("/plot/publication_summary/data")
def showPlotPublicationSummaryData():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    data = db.get_publication_summary()
    print data
    return jsonify({"data": data})


@app.route("/plot/publication_by_author")
def showPlotPublicationByAuthor():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    args["title"] = "Graph - Publication By Author"
    args["gobacklink"] = "/statisticsdetails/publication_author"
    args["class_3"] = "active"
    args["jsfunction"] = "plotPubByAuthor"
    return render_template("plot.html", args=args)


@app.route("/plot/publication_by_author/data")
def showPlotPublicationByAuthorData():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    data = db.get_publications_by_author()
    return jsonify({"data": data})


# @app.route("/plot/publication_by_year")
@app.route("/plot/publication_by_year")
def showPlotPublicationByYear():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    args["title"] = "Graph - Publication By Year"
    args["gobacklink"] = "/statisticsdetails/publication_year"
    args["class_4"] = "active"
    args["jsfunction"] = "plotPubByYear"
    return render_template("plot.html", args=args)


@app.route("/plot/publication_by_year/data")
def showPlotPublicationByYearData():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    data = db.get_publications_by_year()
    return jsonify({"data": data})


# @app.route("/plot/author_by_year")
@app.route("/plot/author_by_year")
def showPlotAuthorByYear():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    args["title"] = "Graph - Author By Year"
    args["gobacklink"] = "/statisticsdetails/author_year"
    args["class_5"] = "active"
    args["jsfunction"] = "plotAuthorByYear"
    return render_template("plot.html", args=args)


@app.route("/plot/author_by_year/data")
def showPlotAuthorByYearData():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    data = db.get_author_totals_by_year()
    return jsonify({"data": data})


# @app.route("/plot/averages")
@app.route("/plot/averages")
def showPlotAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset}
    args["title"] = "Graph - Averages"
    args["gobacklink"] = "/statisticsdetails/averages"
    args["class_6"] = "active"
    args["jsfunction"] = "plotAverages"
    return render_template("plot.html", args=args)


@app.route("/plot/averages/data")
def showPlotAveragesData():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = dict()
    args["plotlink"] = "/plot/averages"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE]
    tables.append({
        "id": 1,
        "title": "Average Authors per Publication",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_authors_per_publication(i)[1])
            for i in averages]})
    tables.append({
        "id": 2,
        "title": "Average Publications per Author",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_publications_per_author(i)[1])
            for i in averages]})
    tables.append({
        "id": 3,
        "title": "Average Publications in a Year",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_publications_in_a_year(i)[1])
            for i in averages]})
    tables.append({
        "id": 4,
        "title": "Average Authors in a Year",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_authors_in_a_year(i)[1])
            for i in averages]})

    args['tables'] = tables
    args['class_6'] = "active"
    print args['tables']
    return jsonify({"data": args['tables']})


# @app.route("/plot/coauthors")


@app.route("/author_network")
def show_network():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "id": "author_network"}
    args['title'] = 'Research Network'
    args['header'] = ''
    name = ''
    if "name" in request.args:
        name = request.args.get("name")
        args['header'] = '{}\'s research network'.format(name)
    args['name'] = name
    args["class_10"] = "active"
    return render_template('author_network.html', args=args)


@app.route("/network/<name>")
def data(name):
    db = app.config['DATABASE']
    return jsonify(db.get_author_network(name))


@app.route("/home")
def get_home():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "id": "home"}
    args['title'] = 'Home'
    return render_template('home.html', args=args)


@app.route("/graphic")
def get_home_graphic():
    db = app.config['DATABASE']
    return jsonify(db.get_author_graphic())

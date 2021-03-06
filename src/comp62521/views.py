from flask import (render_template, request, jsonify)

from comp62521 import app
from database import database


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
def show_averages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "averages", 'title': "Averaged Data", "plotlink": "/plot/averages"}
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
def show_coauthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    pub_types = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset": dataset, "id": "coauthors", "title": "Co-Authors", "class_7": "active",
            "plotlink": "/plot/coauthors"}

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
    args["pub_str"] = pub_types[pub_type]
    return render_template("coauthors.html", args=args)


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
    args = {"dataset": dataset, "name": name, "title": "Comprehensive Statistics for " + name,
            "data": db.get_all_author_stats(name)}
    args["plotlink"] = "/plot/authorstatistics/" + name
    return render_template('author_statistics.html', args=args)


@app.route("/plot/authorstatistics/<name>")
def show_plot_author_statistics(name):
    dataset = app.config['DATASET']
    # db = app.config['DATABASE']
    args = {"dataset": dataset, "name": name, "title": "Comprehensive Statistics for " + name}
    args["gobacklink"] = "/authorstatistics/" + name
    return render_template('plot_author_statistics.html', args=args)


@app.route("/plot/authorstatistics/data/<name>")
def show_plot_data_author_statistics(name):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "name": name, "title": "Comprehensive Statistics for " + name,
            "data": db.get_all_author_stats(name)}
    return jsonify({"data": args["data"]})


@app.route("/statisticsdetails/<status>")
def show_publication_summary(status):
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

    return render_template('statistics_details.html', args=args)


@app.route("/get_degree_static_page")
def show_degree_of_separation_static_page():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "title": "Degrees of Separation", "class_9": "active"}

    return render_template("degree_of_separation.html", args=args)


@app.route("/get_name/<name>")
def get_author_name(name):
    name = name.lower()
    db = app.config['DATABASE']
    all_authors = db.get_all_authors()
    return_author = list()
    for author in all_authors:
        lower_author = author.lower() + ""
        if lower_author.startswith(name) or lower_author.startswith(name.upper()):
            return_author.append(author)
    return jsonify({'data': return_author})


@app.route("/get_plot/<author1>/<author2>")
def get_plot(author1, author2):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "title": "Sprint4 Story4"}
    graph = db.get_all_author_network_graph()
    path = db.get_all_shortest_paths(graph, author1, author2)
    degree = db.get_degree_of_separation(graph, author1, author2)
    return jsonify({'data': path, 'degree': degree})


@app.route("/plot/publication_summary")
def plot_publication_summary():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "title": "Graph - Publication Summary",
            "gobacklink": "/statisticsdetails/publication_summary", "class_2": "active", "jsfunction": "plotPubSummary"}
    return render_template("plot.html", args=args)


@app.route("/plot/publication_summary/data")
def plot_publication_summary_data():
    db = app.config['DATABASE']
    data = db.get_publication_summary()
    return jsonify({"data": data})


@app.route("/plot/publication_by_author")
def plot_publication_by_author():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "title": "Graph - Publication By Author",
            "gobacklink": "/statisticsdetails/publication_author", "class_3": "active", "jsfunction": "plotPubByAuthor"}
    return render_template("plot.html", args=args)


@app.route("/plot/publication_by_author/data")
def plot_publication_by_author_data():
    db = app.config['DATABASE']
    data = db.get_publications_by_author()
    return jsonify({"data": data})


@app.route("/plot/publication_by_year")
def plot_publication_by_year():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "title": "Graph - Publication By Year",
            "gobacklink": "/statisticsdetails/publication_year", "class_4": "active", "jsfunction": "plotPubByYear"}
    return render_template("plot.html", args=args)


@app.route("/plot/publication_by_year/data")
def plot_publication_by_year_data():
    db = app.config['DATABASE']
    data = db.get_publications_by_year()
    return jsonify({"data": data})


@app.route("/plot/author_by_year")
def plot_author_by_year():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "title": "Graph - Author By Year", "gobacklink": "/statisticsdetails/author_year",
            "class_5": "active", "jsfunction": "plotAuthorByYear"}
    return render_template("plot.html", args=args)


@app.route("/plot/author_by_year/data")
def plot_author_by_year_data():
    db = app.config['DATABASE']
    data = db.get_author_totals_by_year()
    return jsonify({"data": data})


@app.route("/plot/averages")
def plot_averages():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "title": "Graph - Averages", "gobacklink": "/averages", "class_6": "active",
            "jsfunction": "plotAverages"}
    return render_template("plot_averages.html", args=args)


@app.route("/plot/averages/data")
def plot_averages_ata():
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
    return jsonify({"data": args['tables']})


@app.route("/plot/coauthors/<pub_type>/<start_year>/<end_year>")
def plot_coauthors(pub_type, start_year, end_year):
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "title": "Graph - Co-author", "gobacklink": "/coauthors", "class_7": "active",
            "jsfunction": "plotCoauthor"}
    return render_template("plot_coauthors.html", args=args)


@app.route("/plot/coauthors/data/<pub_type>/<start_year>/<end_year>")
def plot_coauthors_data(pub_type, start_year, end_year):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "coauthors", "title": "Co-Authors", "class_8": "active",
            "plotlink": "/plot/coauthors", "data": db.get_coauthor_data(int(start_year), int(end_year), int(pub_type)),
            "start_year": start_year, "end_year": end_year, "pub_type": pub_type}
    return jsonify({"data": args["data"]})


@app.route("/author_network")
def show_network():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "id": "author_network", 'title': 'Research Network', 'header': ''}
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


@app.route("/")
def get_home():
    dataset = app.config['DATASET']
    args = {"dataset": dataset, "id": "home", 'title': 'Home', 'class_1': 'active'}
    return render_template('home.html', args=args)


@app.route("/graphic")
def get_home_graphic():
    db = app.config['DATABASE']
    return jsonify(db.get_author_graphic())

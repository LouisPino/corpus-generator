from flask import Flask, redirect, render_template, request, session, Response
from spotify import get_all_artist_songs, download_csv
from multidict import MultiDict 


app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = get_all_artist_songs(request.form.get("artist_names"), request.form.get("dancey-val"), dancey = True if request.form.get("dancey") == "on" else False, )
        return render_template("index.html", data=data)
    elif request.method == "GET":
        return render_template("index.html")

@app.route("/download-csv", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        output = download_csv(request.form["data"])
        return Response(output, 
                    mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=corpus.csv'})
    elif request.method == "GET":
        return render_template("index.html")
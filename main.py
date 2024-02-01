from flask import Flask, redirect, render_template, request, session
from spotify import get_all_artist_songs, download_csv
from multidict import MultiDict 


app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = get_all_artist_songs(request.form.get("artist_names"))
        return render_template("index.html", data=data)
    elif request.method == "GET":
        return render_template("index.html")

@app.route("/download-csv", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        download_csv(list(request.form.items())[1][1])
        return render_template("index.html")
    elif request.method == "GET":
        return render_template("index.html")
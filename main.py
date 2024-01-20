from flask import Flask, redirect, render_template, request, session
from spotify import get_all_artist_songs



app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = get_all_artist_songs(request.form.get("artist_names"))
        return render_template("index.html", data=data)
        # return render_template("index.html", test_data = [{"test_key": request.form.get("artist_id")}])
    elif request.method == "GET":
        return render_template("index.html")
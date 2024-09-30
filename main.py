from flask import Flask, redirect, render_template, request, session, Response, stream_with_context
from spotify import Tracks, Csv, Artists
from multidict import MultiDict 
import time


app = Flask(__name__, static_url_path="/static")
# SSE CONTINUOUS RENDERING USING STREAM_WITH_CONTEXT
def generate_data():
    # Simulating a process that fetches and yields data incrementally
    for i in range(10):  # Example loop to represent data fetching
        # Fetch data from Spotify API or perform processing here
        time.sleep(1)
        yield f"data: {i}\n\n"

@app.route('/stream', methods=["GET"])
def stream():
    return Response(stream_with_context(generate_data()), mimetype='text/event-stream')





@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = Tracks.get_all_artist_songs(request.form.get("artist_names"), request.form.get("dancey-val"), dancey = True if request.form.get("dancey") == "on" else False, )
        return render_template("index.html", data=data)
    elif request.method == "GET":
        return render_template("index.html")

@app.route("/get-artists", methods=["GET", "POST"])
def get_artists_route():
    if request.method == "POST":
        data = Artists.get(request.form.get("genre"), request.form.get("popularity-val"), request.form.get("limit"))
        return render_template("get-artists.html", data=data, names = ', '.join([artist["name"] for artist in data]))
    else:
        return render_template("get-artists.html")


@app.route("/update_artists", methods=["GET", "POST"])
def update_artists():
        return Response(stream_with_context(Artists.get(request.form.get("genre"), request.form.get("popularity-val"), request.form.get("limit"))), mimetype='text/event-stream')




@app.route("/download-csv", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        output = Csv.download(request.form["data"])
        return Response(output, 
                    mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=corpus.csv'})
    elif request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
import eventlet
eventlet.monkey_patch()
from flask import Flask, redirect, render_template, request, session, Response
from flask_socketio import SocketIO, emit
import asyncio
from spotify import Tracks, Csv, Artists
from multidict import MultiDict 
import time


app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app, async_mode='eventlet')  # Use 'eventlet' for async mode



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        filters = {}
        keys = request.form.keys()
        for key in keys:
            filters[key] = request.form.get(key) if request.form.get(key) != "" else 0
        del filters["artist_names"]

        data = Tracks.get_all_artist_songs(request.form.get("artist_names"), filters)
        tracks = data[0]
        error = int(data[1])
        return render_template("index.html", tracks=tracks, error=error)
    elif request.method == "GET":
        return render_template("index.html")

@app.route("/get-artists", methods=["GET", "POST"])
def get_artists_route():
    if request.method == "POST":
        # trigger_generator()
        return render_template("get-artists.html", 
                            #    data=data, names = ', '.join([artist["name"] for artist in data])
                            )

    else:
        return render_template("get-artists.html")





@app.route("/download-csv", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        output = Csv.download(request.form["data"])
        return Response(output, 
                    mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=corpus.csv'})
    elif request.method == "GET":
        return render_template("index.html")




@socketio.on('get_artists')
def handle_get_artists(data):  # Note: Removed async here
    print("hit")
    genre = data.get("genre")
    popularity_val = data.get("popularity-val")
    limit = data.get("limit")

    # Assuming Artists.get() yields data progressively
    for artist in Artists.get(genre, popularity_val, limit):
        print(artist)
        socketio.emit('artists', {'type': 'artists', 'data': artist}, room=request.sid)
        eventlet.sleep(0)  # Yield control to allow the event loop to process other events


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/send_message')
def send_message(msg):
    if msg["type"] == "artists":
        socketio.emit('artists', {'data': msg["data"]})
    elif msg["type"] == "tracks":
        socketio.emit('tracks', {'data': msg["data"]})    


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
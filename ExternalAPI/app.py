from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index(): # This is the function that will be called when the user visits the index page
    # If the user is submitting the form, then request.method will be equal to 'POST'
    if request.method == 'POST':
        # We can access the data the user submitted by using the request object
        artist_name = request.form['artist']
        # We can then use this data to search for albums using the search_albums function
        albums = search_albums(artist_name)
        save_albums_to_db(artist_name, albums)
        # We can then pass this data to the results.html template
        return render_template('results.html', artist=artist_name, albums=albums)
    # If the user visits the index page without submitting the form,
    # then request.method will be equal to 'GET'
    return render_template('index.html')


def search_albums(artist_name):
    API_KEY = '523532'
    URL = f'https://theaudiodb.com/api/v1/json/{API_KEY}/searchalbum.php?s={artist_name}'
    response = requests.get(URL)
    print(type(response))
    print(response)
    data = response.json()
    print(type(data))
    print(data)
    albums = data['album']
    return albums


@app.route('/sort-alphabetical', methods=['POST'])
def sort_alphabetical():
    artist_name = request.form['artist']
    albums = search_albums(artist_name)
    sorted_albums = sorted(albums, key=lambda album: album['strAlbum'])
    return render_template('results.html', artist=artist_name, albums=sorted_albums)


@app.route('/sort-year', methods=['POST'])
def sort_year():
    artist_name = request.form['artist']
    albums = search_albums(artist_name)
    sorted_albums = sorted(albums, key=lambda album: album['intYearReleased'])
    # Sort in a different way - avoid lambda
    return render_template('results.html', artist=artist_name, albums=sorted_albums)



def save_albums_to_db(artist_name, albums):
    conn = sqlite3.connect('albums.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS albums
         (artist TEXT, album TEXT, year INTEGER)''')

    for album in albums:
        c.execute("INSERT INTO albums VALUES (?, ?, ?)", (artist_name, album['strAlbum'], album['intYearReleased']))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)

# port=5000/5001 for use when at home

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
        # Calling the search_albums function will return a list of albums,
        # We can then pass this data to the results.html template
        return render_template('results.html', artist=artist_name, albums=albums)
    # If the user visits the index page without submitting the form,
    # then request.method will be equal to 'GET'
    return render_template('index.html')
    # Rendering the 'index.html' template and returning it as the response when the user visits
    # the index page without submitting the form


def search_albums(artist_name):
    API_KEY = '523532'
    URL = f'https://theaudiodb.com/api/v1/json/{API_KEY}/searchalbum.php?s={artist_name}'
    # Setting the API key and constructing URL for the API request based on the artist name
    response = requests.get(URL)
    # Sending a GET request to the API and storing the response
    print(type(response))
    print(response)
    # Printing for debugging purposes
    data = response.json()
    # Converting the response to JSON and storing it in a variable
    print(type(data))
    print(data)
    albums = data['album']
    # Extracting the 'album' key from the data dictionary, which contains a list of albums
    return albums


@app.route('/sort-alphabetical', methods=['POST'])
def sort_alphabetical():
    artist_name = request.form['artist']
    albums = search_albums(artist_name)
    sorted_albums = sorted(albums, key=lambda album: album['strAlbum'])
    # Extracting the artist name from the submitted form, calling the 'search_albums' function
    # to retrieve a list of albums, and sorting the albums alphabetically based on the
    # 'strAlbum' key using the sorted() function
    return render_template('results.html', artist=artist_name, albums=sorted_albums)
    # Rendering the 'results.html' template with the sorted albums and returning is as the response


@app.route('/sort-year', methods=['POST'])
def sort_year():
    artist_name = request.form['artist']
    albums = search_albums(artist_name)
    sorted_albums = sorted(albums, key=lambda album: album['intYearReleased'])
    # Extracting the artist name from the submitted form, calling the 'search_albums' function
    # to retrieve a list of albums, and sorting the albums by release year based on the
    # 'intYearReleased' key using the sorted() function
    # Sort in a different way - avoid lambda
    return render_template('results.html', artist=artist_name, albums=sorted_albums)



def save_albums_to_db(artist_name, albums):
    conn = sqlite3.connect('albums.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS albums
         (artist TEXT, album TEXT, year INTEGER)''')
# Establishing a connection to SQLite database file and creating a table named 'albums'
# if it doesn't already exist, with columns for artist name, album name, and release year
    for album in albums:
        c.execute("INSERT INTO albums VALUES (?, ?, ?)", (artist_name, album['strAlbum'], album['intYearReleased']))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)

# port=5000/5001 alternative for use when at home

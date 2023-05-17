BEGIN SEARCH

INPUT Artist as artist_name or artist name = input (from user input select search button)
THEN search for artist_name
    IF artist name found
    THEN display artist name and albums (through results.html)
ELSE display error message
END IF

END SEARCH

# Collective Algorithm

#BEGIN SEARCH
#set up routes
    
def search():
    #INPUT Artist as artist_name or artist_name = Artist
    artist_name = request.form['artist']
    #VAR URL = https://theaudiodb.com/api/v1/json/{API_KEY}/searchalbum.php?s=artist_name
    URL = f'https://theaudiodb.com/api/v1/json/523532/searchalbum.php?s=artist_name'
    #VAR response = GET artist_data from URL
    response = requests.get(URL)
    #VAR data = format response
    #print(type(response))
    #prtint(response)
    data = response.json()
    #print(type(data))
    #print(data)
    #DISPLAY data AS results.html
    return render_template('results.html', artist=artist_name, albums=albums)
#END SEARCH




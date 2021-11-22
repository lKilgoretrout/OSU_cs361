import os, requests
from flask import Flask, render_template, url_for
from load_data import load_data  # for loading IMDB values
from flask.globals import request
app = Flask(__name__)


IMDB_key = ""




# @lkilgoretrout Here is the endpoint you can access to get the meme resource: 
# https://fine-volt-331118.ue.r.appspot.com/  I decided to keep my project and 
# service separate after all lol Responses are in the format:
 # {"meme_url":"https://i.redd.it/1dyc8tfw3ox71.jpg%22,%22source%22:%22ProgrammerHumor%22%7D,
 # where meme_url is the link and source is the subreddit where the image is pulled from. 
 # It works flawlessly as of now, but there are a few minor improvements I would like to 
 # make in the next sprint.


# get Eric Roberts from from pickle file (IDMB database values)
# put into a global dictionary 
ER_movies = load_data()    # e.g. {'tt8435252': ['Broken Church', '2015', 'Drama']...}

def get_meme():
    '''response Example: {"meme_url":"https://i.redd.it/1dyc8tfw3ox71.jpg","source":"ProgrammerHumor"}'''
    response = requests.get('https://fine-volt-331118.ue.r.appspot.com/')
    print(response.text)
    response_json = response.json()
    
    meme = response_json["meme_url"]
    
    return meme
    
    
    
    
# chunlin's IMDB synopsis service:
def request_synopsis(imdb_id):
    '''INPUT: imdb_id, e.g. "tt123456"
       OUTPUT: json object '''
    # sends imdb database id and returns synopsis (string) from IMDB API
    response = requests.post('https://chunlin-api.ue.r.appspot.com/imdb', json={"IMDB":imdb_id})
    print(response.text)
    synopsis = response.json()
    
    return synopsis


def request_movie_poster(imdb_id):
    '''INPUT imdb_id, e.g. "tt123456" and sends a json GET request
       OUTPUT a <img> link inside a JSON response'''
    response = requests.get("http://127.0.0.1:6000/poster", json={"imdb_id":imdb_id})
    print(response.text)
    response_json = response.json()
    
    try:
        poster = response_json['poster']['posters'][0]['link']
    except IndexError:
        poster = None
    return poster

def query_database(movie_name):
    '''INPUT: string, a correctly spelled movie name
       OUTPUT: tuple, ("imdb_id","year","genre")
       RETURN None if movie_name not found '''
    
    imdb_id = None
    year, genre = '', ''
    found = False
    for id in ER_movies:
        if movie_name == ER_movies[id][0]:
            imdb_id = id
            year = ER_movies[id][1]
            genre = ER_movies[id][2]
            found = True
    if found:
        return (imdb_id,year,genre)
    else:
        return None

# loads welcome page
@app.route('/')
@app.route('/index')
def index():     
    meme = get_meme() 
    return render_template("index.j2",meme=meme, movies=ER_movies)

# handles the form on the index page
@app.route('/search')
def search():
    movie_name = request.args.get('movie_name') 
    
    id_year_genre = query_database(movie_name)
    print(id_year_genre)
    if not id_year_genre:
        return render_template("failure.j2", movie_name=movie_name)
    
    if id_year_genre:
        
        id = id_year_genre[0]
        year = id_year_genre[1]
        genre = id_year_genre[2]
        
        poster = request_movie_poster(id)
        synopsis = request_synopsis(id)
    
    return render_template("results.j2", movie_name=movie_name, synopsis=synopsis, poster=poster, year=year, genre=genre) 
    
    
@app.route('/results/<movie>', methods=['GET'])
def results(movie):
    
    if movie: 
        movie_name = movie
        
    id_year_genre = query_database(movie_name)
    if not id_year_genre:
        return render_template("failure.j2", movie_name=movie_name)
    
    id = id_year_genre[0]
    year = id_year_genre[1]
    genre = id_year_genre[2]
    
    poster = request_movie_poster(id)   
    synopsis = request_synopsis(id)
    
    return render_template("results.j2", poster=poster, movie_name=movie_name, synopsis=synopsis, year=year, genre=genre)    
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.j2'), 404
    
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 42000)) 
    app.run(port=port, debug=True)

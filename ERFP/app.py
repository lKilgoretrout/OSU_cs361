import os, api_keys
from services import *
from flask import Flask, render_template, url_for
from flask.globals import request

app = Flask(__name__)
IMDB_key = api_keys.IMDB_KEY

# get Eric Roberts from from pickle file (IDMB database values)
# put into a global dictionary 
global ER_movies
ER_movies = load_data()    # e.g. {'tt8435252': ['Broken Church', '2015', 'Drama']...}

# loads welcome page
@app.route('/')
@app.route('/index')
def index():     
    meme = get_meme() 
        
    # sorting movies by title, year or genre (from button on index page)
    if 'title' in request.args or 'year' in request.args or 'genre' in request.args:
        index = None
        if request.args.get('title'):   index = 0
        elif request.args.get('year'):  index = 1
        elif request.args.get('genre'): index = 2
        
        sorted_movies = [value for value in sorted(ER_movies.values(), key=lambda item: item[index])]
        
        return render_template("index.j2", movies=sorted_movies,meme=meme)
        
    else:
        movies = [value for value in ER_movies.values()]
        
        return render_template("index.j2", movies=movies,meme=meme)
    

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

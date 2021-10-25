import os
from flask import Flask, render_template
from flask.globals import request
app = Flask(__name__)


# loads welcome page
@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template("index.j2")
    
@app.route('/index/query', methods=['GET'])
def query():
    return render_template("results.j2")
    
@app.route('/results', methods=['GET'])
def results():
    query = request.args.get('actor_name')
    
    # TO DO: check local compiled database for actor,
    # if not in database, return error message on results page
    def check_database(query):
        # returns if movie in database and the imdb_id for it
        if query != "Christian Bale":
            return False
        else:
            return True
        
    # TO DO: run shortest path traversal between query
    # and Eric Roberts in compiled database
    def graph(query):
        # returns database keys for movies in degrees graph
        # --> tt123456, tt234567, tt345678
        pass

    # TO DO: make HTTP call to Chunlin's IMDB synopsis scraper
    def request_synopsis(imdb_id):
        # sends imdb database id's and returns synopsis from IMDB API
        pass
        
    # TO DO : make HTTP call to Rebecca
    def request_movie_poster(imdb_id):
        # sends imdb database id and returns movie poster from IMDB API ( or image scraper)
        pass
    
    
    # The following logic is all mock-up but the process is roughly what 
    # will happen when the user clicks the submit button
    if not check_database(query):                         # --> routes to failure page if query not in database or no conneciton to ER
        return render_template("failure.j2", query=query)
    
    
    #connections = graph(query)                                          # --> returns a list of imdb database keys
    #synopses = []                                         # --> dealing with the synopses is easy as they're strings
    #for value in  connections:
    #    synopses.append(request_synopses(value.id))
    #    request_movie_poster(value.id)  # not exactly sure yet on the best way to route the images
    
    synopses = [
        "In 1970, drug-fueled Los Angeles private investigator Larry 'Doc' Sportello investigates the disappearance of a former girlfriend.",
        "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful \
        Thanos before his blitz of devastation and ruin puts an end to the universe.",
        "New York City writing professor, Frannie Avery, has an affair with a police detective who is investigating \
        the murder of a beautiful young woman in her neighborhood.",
        "An industrial worker who hasn't slept in a year begins to doubt his own sanity."
    ]
    
    return render_template("results.j2", query=query, synopses=synopses)    
    
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.j2'), 404
    
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 42000)) 
    app.run(port=port, debug=True)
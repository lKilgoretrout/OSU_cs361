import pickle, requests


def load_data():
    # for reading also binary mode is important
    dbfile = open('tconst_title_startYear_genre.p', 'rb')     
    db = pickle.load(dbfile)    # pickled as a list of lists
    ER_dict = {}
    for line in db:
        # from each list --> dict:  {'tt8435252': ['Broken Church', '2015', 'Drama']}
        if line[2] == '\\N' and line[3] != '\\N':
            ER_dict[line[0]] = [line[1], '?', line[3]]     
        
        elif line[3] == '\\N' and line[2] != '\\N':                           
            ER_dict[line[0]] = [line[1], line[2], '?']
        
        elif line[2] == '\\N' and line[3] == '\\N':
            ER_dict[line[0]] = [line[1], '?', '?']
        
        else:
            ER_dict[line[0]] = [line[1], line[2], line[3]]
        
    
    dbfile.close()
    return ER_dict

global ER_movies
ER_movies = load_data()

def get_meme():
    '''response Example: 
       {"meme_url":"https://i.redd.it/1dyc8tfw3ox71.jpg","source":"ProgrammerHumor"}'''
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
    except KeyError:
        try:
            poster = response_json['poster']['items'][0]['image']
        except KeyError:
            poster = None
        except TypeError:
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
    return (imdb_id,year,genre) if found else None
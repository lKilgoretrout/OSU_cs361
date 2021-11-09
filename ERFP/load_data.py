import pickle
def load_data():
    # for reading also binary mode is important
    dbfile = open('tconst_title_startYear_genre.p', 'rb')     
    db = pickle.load(dbfile)
    ER_dict = {}
    for line in db:
        # from each list --> dict:  {'tt8435252': ['Broken Church', '2015', 'Drama']}
        if line[2] == '\\N':
            ER_dict[line[0]] = [line[1], '?', line[3]]
        else:
            ER_dict[line[0]] = [line[1], line[2], line[3]]
        #print(line)
    
    #for imdb_id in ER_dict:
    #    print(f"{imdb_id} : {ER_dict[imdb_id]}")
    dbfile.close()
    return ER_dict
load_data()
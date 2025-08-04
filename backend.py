from concurrent.futures import ThreadPoolExecutor
import json
import random
import requests
from SearchResults import *
from Searches import *
from HomePage import *
from collections import*
from flask import Flask, render_template, jsonify,request,redirect,url_for
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio=SocketIO(app)
apiKey = ""



@app.route('/')
def index():
    return render_template('index.html')
movieset = [1,2,3,4,5,6,7,8]
TMDBname={1:"299534",2:"299536",3:"900667",4:"503314",5:"284054",6:"541671",7:"1061474",8:"1930"}
movielink={1:"https://mcloud.vvid30c.site/watch/?v21#aTdNWXJHN2Q3OHZmUGZ1SGlDT2g4ZldNN2N4UTVHRlV2d2J5b3pyT1VTQjdsN01DYmNnMjhmc1FYaVZJdDdrN2JWMWI",2:"https://www.youtube.com/watch?v=mj4dVlxhfA4",3:"https://www.youtube.com/watch?v=ChsLmEpdNrI",4:"https://www.youtube.com/watch?v=kMHN4s38wyk",5:"https://www.youtube.com/watch?v=uCqUv9rm7-M",6:"https://www.youtube.com/watch?v=b9Rr9ygb-ac"}
names = ["","Avengers Endgame","Avengers Infinity War","One Piece Film Red","Dragon Ball Super Broly","Black Panther","Ballerina", "Superman (2025)","The Amazing Spider-Man Spider Man Spiderman (2012)"]
#The names list includes empty quotations because it accounts for the search beginning at 0


indexthread = ThreadPoolExecutor()
future = indexthread.submit(Searches.InvertedIndex,names)
nameindex=future.result()
indexthread.shutdown()

@app.route('/NameSearch', methods=['POST'])
def NameSearch():
    Name = request.form['moviename']
    Name = Name.lower()
    print(f"Request to Search: {Name}")
    for x in range(len(names)):
        if names[x].lower()==Name:
            print(names[x])
            print(x)
            return jsonify({'movienumber':x})
    #this movie could not be found, returning index outside of movielist
    return jsonify({'movienumber':-1})


@app.route('/indexpull', methods=['GET'])
def populateHomepage():
    return Homepage.indexpull(TMDBname,movieset,apiKey)

@app.route('/IndexSearches', methods=['POST'])
def indexSearches():
    data=request.get_json()
    query= data.get('query','')
    return jsonify(Searches.IndexSearches(nameindex,query))

@app.route('/movieInfo', methods=['POST'])
def movieinfo():
    data=request.get_json()
    results=data.get('indexes',[])
    print(results)
    return Searchresults.movieInfo(results,apiKey,TMDBname)

@app.route('/links', methods=['POST'])
def link():
    return Homepage.pulllink(movielink)



@app.route('/image+info', methods=['POST'])
def playerinfo():
    return(Homepage.playerinfo(TMDBname,apiKey))


@app.route('/player.html')
def player():
    link = request.args.get('link')
    return render_template('player.html', link=link)

@app.route('/searchresults.html', methods=['GET'])
def show_search_results():
    return render_template('searchresults.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

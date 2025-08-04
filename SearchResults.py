from Searches import *
from flask import jsonify
import requests
import json
class Searchresults:
    def movieInfo(results:list,apiKey:str,TMDBname:list):
        movieimages=[]
        movietitles=[]
        for movieindex in results: 
            url = f"https://api.themoviedb.org/3/movie/{TMDBname[movieindex]}?api_key={apiKey}"
            response = requests.get(url)
            data =response.json()
            imagelink=f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            movieimages.append(imagelink)
            movietitles.append(data["title"])
        return jsonify({"movieimages":movieimages,"movietitles":movietitles})


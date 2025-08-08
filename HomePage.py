from collections import *
from flask import jsonify,request
import requests
import random
class Homepage:
    def indexpull(TMDBname:list, movieset:list,apiKey:str):
        #shit's kinda ass, using a hashset that evaluates if len(5) later.
        #Ight I fixed it, now its close to O(1), this was faster than the hashset
        temporarylist=random.sample(movieset,5)
        b1=temporarylist[0]
        b2=temporarylist[1]
        b3=temporarylist[2]
        b4=temporarylist[3]
        b5=temporarylist[4]
        imagelist=[]
        for x in range(5):
            url = f"https://api.themoviedb.org/3/movie/{TMDBname[temporarylist[x]]}?api_key={apiKey}"
            response = requests.get(url)
            data =response.json()
            imagelink=f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            imagelist.append(imagelink)
        img1=imagelist[0]
        img2=imagelist[1]
        img3=imagelist[2]
        img4=imagelist[3]
        img5=imagelist[4]
        print(temporarylist)
        print(imagelist)
        return jsonify({'b1':b1, 'b2': b2, 'b3': b3, 'b4': b4, 'b5': b5,'img1': img1,'img2':img2,'img3':img3,'img4':img4,'img5':img5})
    
    def playerinfo(TMDBname:list,apiKey:str):
        infonum=int(request.form['infonum'])
        print(infonum)
        url = f"https://api.themoviedb.org/3/movie/{TMDBname[infonum]}?api_key={apiKey}"
        response = requests.get(url)
        data=response.json()
        x="Jagpreet"
        return jsonify({
            'movieimage':f"https://image.tmdb.org/t/p/w500{data['poster_path']}",

            'movietitle':data['title'], 
            'movieinfo':data['overview']
            })
    def pulllink(movielink:list):
        global link
        try:
            movieID = int(request.form['movieID'])
            link=movielink[movieID]
            if "youtube.com/" in link:
                link = f"https://www.youtube.com/embed/{link[32:]}"
                print(link)
            print(movieID, link)
            return jsonify({'link': link})
        except:
            print("Cannot parse")
            return jsonify("failed")
    
    


    









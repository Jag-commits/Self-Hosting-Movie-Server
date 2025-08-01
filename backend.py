import threading
import json
import random
import requests
from collections import*
from flask import Flask, render_template, jsonify,request,redirect,url_for
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio=SocketIO(app)
apiKey = ""



@app.route('/')
def index():
    return render_template('index.html')
movieset = [1,2,3,4,5,6]
TMDBname={1:"299534",2:"299536",3:"900667",4:"503314",5:"284054",6:"541671"}
movielink={1:"https://mcloud.vvid30c.site/watch/?v21#aTdNWXJHN2Q3OHZmUGZ1SGlDT2g4ZldNN2N4UTVHRlV2d2J5b3pyT1VTQjdsN01DYmNnMjhmc1FYaVZJdDdrN2JWMWI",2:"https://www.youtube.com/watch?v=mj4dVlxhfA4",3:"https://www.youtube.com/watch?v=ChsLmEpdNrI",4:"https://www.youtube.com/watch?v=kMHN4s38wyk",5:"https://www.youtube.com/watch?v=uCqUv9rm7-M",6:"https://www.youtube.com/watch?v=b9Rr9ygb-ac"}
#movieimages={1:"https://ohsmagnet.com/wp-content/uploads/2019/04/unnamed-607x900.jpg",2:"https://i.redd.it/gnv94oll6im01.jpg",3:"https://a.storyblok.com/f/178900/960x1348/a49c330773/3cc622bba797a81984c7e437b39bd3461662992599_main.jpg/m/filters:quality(95)format(webp)",4:"https://m.media-amazon.com/images/M/MV5BMTA5MTc1M2EtZWQ2Ni00ZmU2LTg3MzQtOTliMjE4OGM0ZWFiXkEyXkFqcGc@._V1_.jpg",5:"https://m.media-amazon.com/images/M/MV5BMTg1MTY2MjYzNV5BMl5BanBnXkFtZTgwMTc4NTMwNDI@._V1_.jpg",6:"https://www.themoviedb.org/t/p/w600_and_h900_bestv2/mKp4euM5Cv3m2U1Vmby3OGwcD5y.jpg"}
names = ["","Avengers Endgame","Infinity War","One Piece Film:Red","Dragon Ball Super:Broly","Black Panther","Ballerina"]
#The names list includes empty quotations because it accounts for the search beginning at 0
def binarysearch(list,value):
    start = 0
    end = len(list)-1
    for x in range(start,end+1):
        mid = int((start+(end))/2)
        if list[mid]==value:
            return list[mid]
        elif list[mid]>value:
            end = mid-1
        else:
            start = mid+1
    return False

#This makes a dictionary of words where the key is a word from the title and the value is the index location.
def buildInvertedIndex():
    index = defaultdict(set)
    for i,name in enumerate(names):
        for word in name.lower().split():
            index[word].add(i)
    return index


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

def NameSearch2(name: str):
    Name = name.lower()
    searchArray=Name.split()
    resultsArray=[]
    #Search through movies with matching words and add the movie # to the Results Page
    #There has to be a better way to check if 
    for x in range(len(names)):
        for y in range(len(searchArray)):
            if searchArray[y] in names[x].lower().split():
                resultsArray.append(x)
                break
    print(resultsArray)

#Most efficient search
def NameSearch3(search:str):
    search=search.lower().split()
    search.remove('the','a','of','with','this')
    print(search)
    results=[]
    for x in search:
        if x in index and index[x] not in results:
            results.append(index[x])
    return results

            


@app.route('/indexpull', methods=['GET'])
def indexpull():
    temporarylist=[]
    for x in range(5):
        while True:
            value=random.choice(movieset)
            if value in temporarylist:
                continue
            else:
                temporarylist.append(value)
                break
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


@app.route('/links', methods=['POST'])
def pulllink():
    global link
    try:
        movieID = int(request.form['movieID'])
        link=movielink[movieID]
        if "youtube.com/" in link:
            link = f"https://www.youtube.com/embed/{link[32:]}"
            print(link)
        print(index, link)
        return jsonify({'link': link})
    except:
        print("Cannot parse")
        return jsonify("failed")




@app.route('/image+info', methods=['POST'])
def movieinfo():
    infonum=int(request.form['infonum'])
    print(infonum)
    url = f"https://api.themoviedb.org/3/movie/{TMDBname[infonum]}?api_key={apiKey}"
    response = requests.get(url)
    data=response.json()
    return jsonify({'movieimage':f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
        'movietitle':data['title'], 
        'movieinfo':data['overview']})
    


@app.route('/player.html')
def player():
    link = request.args.get('link')
    return render_template('player.html', link=link)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

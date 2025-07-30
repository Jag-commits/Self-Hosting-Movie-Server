import threading
import json
from flask import Flask, render_template, jsonify,request,redirect,url_for
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio=SocketIO(app)
@app.route('/')
def index():
    return render_template('index.html')




movieset = [1,2,3,4,5]
moviename={1:"Avengers Endgame",2:"Infinity War",3:"One Piece:Red",4:"Dragon Ball Super:Broly",5:"Black Panther"}
movielink={1:"https://www.youtube.com/watch?v=kMHN4s38wyk",2:"https://www.youtube.com/watch?v=kMHN4s38wyk",3:"https://www.youtube.com/watch?v=kMHN4s38wyk",4:"https://www.youtube.com/watch?v=kMHN4s38wyk",5:"https://www.youtube.com/watch?v=kMHN4s38wyk"}


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

@app.route('/links', methods=['POST'])
def pulllink():
    global link
    try:
        button_number = int(request.form['button_number'])
        index = binarysearch(movieset, button_number)
        link=movielink[index]
        print(index, link)
        return jsonify({'link': link})
    except:
        print("Cannot parse")
        return jsonify("failed")
    
@app.route('/go-to-player')
def go_to_player():
    return redirect(url_for('player', link=link))    
@app.route('/player.html')
def player():
    link = request.args.get('link')
    return render_template('player.html', link=link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

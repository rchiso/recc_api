from flask import Flask, request, jsonify
from details import User
from recc import find_similar_songs

app = Flask(__name__)


def give_recc(content):
    username1 = content['username1']
    username2 = content['username2']
    songs_to_consider = content['songs_to_consider']
    n_reccs = content['n_reccs']
    user1 = User(username1)
    user2 = User(username2)
    ts1 = user1.fetch_top_songs(num=songs_to_consider)
    ts2 = user2.fetch_top_songs(num=songs_to_consider)
    reccs = find_similar_songs(ts1, ts2, num=n_reccs)
    result = []
    for recc in reccs:
        result.append(f'Song Name = {recc.name}, Artist = {recc.artist}')
    result = {'reccomendations': result}
    return result


@app.route("/")
def hello():
    return "Song reccomendation API. Send a POST request to /recc endpoint with the following 4 fields: username1, username2, songs_to_consider, n_reccs"


@app.route("/recc", methods=['POST'])
def return_data():
    content = request.json
    output = give_recc(content)
    return jsonify(output)
    

if __name__ == '__main__':
    app.run(debug=True, port=9000)

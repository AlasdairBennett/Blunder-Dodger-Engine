import time
from NegMaxx import NegMaxx
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/blunder_dodger_move', methods=['POST'])
def blunder_dodger_move():
    return jsonify({"Result": (NegMaxx(request.json['fen']).nega_wrapper())})


if __name__ == '__main__':
    app.run()

    # testFen = "r6r/1b2k1bq/8/8/7B/8/8/R3K2R b KQ - 3 2"
    #
    # n = NegMaxx(testFen)
    #
    # start = time.time()
    # print(n.nega_wrapper())
    # end = time.time()
    # print(end - start)

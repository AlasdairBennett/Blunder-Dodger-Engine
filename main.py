from AlphaBetaEngine import AlphaBetaEngine
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/blunder_dodger_move', methods=['POST'])
def blunder_dodger_move():
    return jsonify({"Result": (AlphaBetaEngine(request.json['fen']).ab_wrapper())})


if __name__ == '__main__':
    app.run()

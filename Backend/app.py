from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

games = {}  # Store ongoing games by session/user id if needed later

@app.route('/api/mines/start', methods=['POST'])
def start_mines():
    data = request.get_json()
    bet = float(data.get('bet', 0))
    mine_count = int(data.get('mineCount', 0))
    balance = float(data.get('balance', 0))

    if bet > balance:
        return jsonify({'error': 'Insufficient balance'}), 400

    if mine_count < 1 or mine_count >= 25:
        return jsonify({'error': 'Invalid mine count'}), 400

    # Generate mine positions from 0 to 24
    mine_positions = random.sample(range(25), mine_count)
    new_balance = balance - bet

    return jsonify({
        'minePositions': mine_positions,
        'newBalance': new_balance
    })

@app.route('/api/mines/reveal', methods=['POST'])
def reveal_tile():
    data = request.get_json()
    index = int(data.get('index'))
    mine_positions = data.get('minePositions')
    if index in mine_positions:
        return jsonify({'mine': True})
    return jsonify({'mine': False})

@app.route('/api/mines/cashout', methods=['POST'])
def cashout():
    data = request.get_json()
    balance = float(data.get('balance', 0))
    winnings = float(data.get('winnings', 0))
    return jsonify({
        'newBalance': balance + winnings
    })

if __name__ == '__main__':
    app.run(debug=True)
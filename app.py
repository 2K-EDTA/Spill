from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Global variables to store game data
players = []
game_data = {
    "chameleon": None,
    "board": [
        ["Cyclops", "Pegasus", "Medusa", "Sphinx"],
        ["Werewolf", "Unicorn", "Dragon", "Troll"],
        ["Loch Ness Monster", "Mermaid", "Phoenix", "Vampire"],
        ["Minotaur", "Hydra", "Yeti", "Centaur"]
    ],
    "started": False,
    "votes": {}
}

@app.route('/join', methods=['POST'])
def join_game():
    username = request.json.get('username')
    if username not in players:
        players.append(username)
    return jsonify({"status": "success", "players": players})

@app.route('/start', methods=['POST'])
def start_game():
    if not players:
        return jsonify({"status": "error", "message": "No players in the game"})
    
    game_data['chameleon'] = random.choice(players)
    game_data['started'] = True
    return jsonify({"status": "success", "chameleon": game_data['chameleon']})

@app.route('/vote', methods=['POST'])
def vote():
    username = request.json.get('username')
    vote = request.json.get('vote')
    game_data['votes'][username] = vote
    return jsonify({"status": "success", "votes": game_data['votes']})

@app.route('/reset', methods=['POST'])
def reset_game():
    game_data['chameleon'] = None
    game_data['started'] = False
    game_data['votes'] = {}
    return jsonify({"status": "success", "message": "Game reset"})

@app.route('/status', methods=['GET'])
def game_status():
    return jsonify({
        "players": players,
        "chameleon": game_data['chameleon'],
        "started": game_data['started'],
        "votes": game_data['votes']
    })

if __name__ == '__main__':
    app.run(debug=True)

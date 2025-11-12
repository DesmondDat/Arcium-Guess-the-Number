"""
Flask API for Guess the Number game
Handles all backend logic and crypto operations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from encryption import CommitRevealProtocol
from game import GuessTheNumberGame
import uuid
import json

app = Flask(__name__)
CORS(app)

# Store active games in memory (in production, use database)
active_games = {}

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Game API is running'}), 200

@app.route('/api/game/create', methods=['POST'])
def create_game():
    """Create a new game session"""
    try:
        data = request.json
        mode = data.get('mode', 'single')  # 'single' or 'two'
        player1 = data.get('player1', 'Player 1')
        player2 = data.get('player2', 'Computer' if mode == 'single' else 'Player 2')
        
        # Create game instance
        game = GuessTheNumberGame(min_num=1, max_num=100, max_guesses=10)
        game.setup_game(player1, player2)
        
        # Generate game ID
        game_id = str(uuid.uuid4())
        
        # Store game
        active_games[game_id] = {
            'game': game,
            'mode': mode,
            'player1': player1,
            'player2': player2,
            'created_at': __import__('datetime').datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'game_id': game_id,
            'mode': mode,
            'player1': player1,
            'player2': player2,
            'min': 1,
            'max': 100,
            'max_guesses': 10
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/game/<game_id>/commit', methods=['POST'])
def commit_number(game_id):
    """Commit to a secret number"""
    try:
        if game_id not in active_games:
            return jsonify({'success': False, 'error': 'Game not found'}), 404
        
        data = request.json
        secret = data.get('secret')
        
        if not isinstance(secret, int) or secret < 1 or secret > 100:
            return jsonify({'success': False, 'error': 'Invalid number'}), 400
        
        game_data = active_games[game_id]
        game = game_data['game']
        
        # Commit the number
        commitment_hash = game.commit_number(secret)
        
        # Store the hash for verification later
        game_data['commitment_hash'] = commitment_hash
        
        return jsonify({
            'success': True,
            'commitment_hash': commitment_hash,
            'message': 'Secret number committed and encrypted'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/game/<game_id>/guess', methods=['POST'])
def make_guess(game_id):
    """Make a guess"""
    try:
        if game_id not in active_games:
            return jsonify({'success': False, 'error': 'Game not found'}), 404
        
        data = request.json
        guess = data.get('guess')
        
        if not isinstance(guess, int):
            return jsonify({'success': False, 'error': 'Invalid guess'}), 400
        
        game_data = active_games[game_id]
        game = game_data['game']
        
        # Make the guess
        result = game.make_guess(guess)
        
        if not result['valid']:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 400
        
        stats = game.get_game_stats()
        
        return jsonify({
            'success': True,
            'guess': guess,
            'feedback': result['feedback'],
            'attempt': result['attempt'],
            'remaining': result['remaining'],
            'game_over': game.game_state['game_over']
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/game/<game_id>/reveal', methods=['POST'])
def reveal_game(game_id):
    """Reveal and verify the commitment"""
    try:
        if game_id not in active_games:
            return jsonify({'success': False, 'error': 'Game not found'}), 404
        
        game_data = active_games[game_id]
        game = game_data['game']
        
        # Reveal and verify
        result = game.reveal_and_verify()
        
        # Clean up game from memory
        del active_games[game_id]
        
        return jsonify({
            'success': True,
            'secret_number': result['secret_number'],
            'commitment_valid': result['commitment_valid'],
            'guesses_made': result['guesses_made'],
            'result': result['result'],
            'game_winner': result['game_winner'],
            'timestamp': result['timestamp']
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/game/<game_id>/stats', methods=['GET'])
def get_stats(game_id):
    """Get current game statistics"""
    try:
        if game_id not in active_games:
            return jsonify({'success': False, 'error': 'Game not found'}), 404
        
        game_data = active_games[game_id]
        game = game_data['game']
        stats = game.get_game_stats()
        
        return jsonify({
            'success': True,
            'phase': stats['phase'],
            'guesses_made': stats['guesses_made'],
            'guesses_remaining': stats['guesses_remaining'],
            'game_over': stats['game_over'],
            'recent_guesses': stats['recent_guesses']
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/concepts', methods=['GET'])
def get_concepts():
    """Get educational content about Arcium concepts"""
    return jsonify({
        'concepts': [
            {
                'title': 'Commitment',
                'description': 'Your secret number is encrypted and cryptographically bound. You cannot change it without breaking the commitment hash.',
                'key_points': [
                    'Encrypted data stays hidden',
                    'Hash proves commitment exists',
                    'Can\'t change mind later',
                    'Arcium uses this for data binding'
                ]
            },
            {
                'title': 'Reveal',
                'description': 'After the game, your encrypted commitment is decrypted to verify you were honest.',
                'key_points': [
                    'Decrypt only when authorized',
                    'Timestamp proves decision timing',
                    'Shows secret to verify claim',
                    'Arcium reveals results to authorized parties'
                ]
            },
            {
                'title': 'Verification',
                'description': 'The commitment hash is verified against decrypted data to prove you didn\'t cheat.',
                'key_points': [
                    'Hash matches = you\'re honest',
                    'Hash differs = you cheated',
                    'Cryptography proves truth',
                    'Arcium guarantees data integrity'
                ]
            }
        ]
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Export app for Vercel
handler = app

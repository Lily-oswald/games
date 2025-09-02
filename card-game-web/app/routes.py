from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from app.game.cardgame import CardGame, load_deck
import uuid

# Create a Blueprint for this module
blueprint = Blueprint('main', __name__)

@blueprint.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@blueprint.route('/game')
def game():
    """Render the game page."""
    return render_template('game.html')

@blueprint.route('/api/game/start', methods=['POST'])
def start_game():
    """Start a new game and return the initial state."""
    # Create a new game
    game = CardGame()
    
    # Generate a unique session ID for this game
    game_id = str(uuid.uuid4())
    
    # Store game state in session
    session['game_id'] = game_id
    session['deck'] = game.deck  # Store the actual deck
    session['deck_remaining'] = len(game.deck)
    session['current_step'] = game.current_step
    session['cards'] = []
    session['game_over'] = False
    session['message'] = game.game_message
    session['score'] = 0
    session['forbidden_suits'] = list(game.forbidden_suits) if hasattr(game, 'forbidden_suits') else []
    
    # Return the initial game state
    return jsonify({
        'game_id': game_id,
        'message': game.game_message,
        'next_action': game.get_current_step(),
        'deck_remaining': len(game.deck),
        'game_over': False
    })

@blueprint.route('/api/game/guess', methods=['POST'])
def make_guess():
    """Process a player's guess."""
    if 'game_id' not in session:
        return jsonify({'error': 'No active game session'}), 400
    
    data = request.get_json()
    if not data or 'guess' not in data:
        return jsonify({'error': 'Missing guess parameter'}), 400
    
    guess = data['guess']
    
    # Recreate the game state from the session
    game = CardGame()
    if 'deck' in session:
        game.deck = session['deck']  # Use the stored deck
    else:
        game.deck = load_deck()  # Fallback if no deck in session
    
    game.current_step = session['current_step']
    game.cards = session['cards']
    game.game_over = session['game_over'] 
    game.game_message = session['message']
    game.score = session['score']
    game.forbidden_suits = set(session.get('forbidden_suits', []))
    
    # Process the guess
    result = game.make_guess(guess)
    
    # Update the session
    session['deck'] = game.deck  # Store the actual deck
    session['deck_remaining'] = len(game.deck)
    session['current_step'] = game.current_step
    session['cards'] = game.cards
    session['game_over'] = game.game_over
    session['message'] = game.game_message
    session['score'] = game.score
    session['forbidden_suits'] = list(game.forbidden_suits) if hasattr(game, 'forbidden_suits') else []
    
    # Include deck remaining in the response
    result['deck_remaining'] = len(game.deck)
    
    return jsonify(result)

@blueprint.route('/api/game/reset', methods=['POST'])
def reset_game():
    """Reset the game session."""
    if 'game_id' in session:
        session.pop('game_id')
    
    return jsonify({'success': True})

def init_app(app):
    """Initialize the application with this blueprint."""
    app.register_blueprint(blueprint)
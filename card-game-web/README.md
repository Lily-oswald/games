# Card Game Web Application

This is a web-based implementation of the card guessing game where players guess card attributes through 4 stages.

## Game Rules

1. **Step 1: Red or Black** - Guess if the next card will be red or black
2. **Step 2: Higher or Lower** - Guess if the next card will be higher or lower than the first card
3. **Step 3: In Between or Outside** - Guess if the third card's rank will be in between or outside the first two cards
4. **Step 4: Guess the Suit** - Guess which suit the next card will be (Hearts, Diamonds, Clubs, or Spades)

Complete all four steps correctly to win!

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Session-based storage (no persistent database required)

## Project Structure

```
card-game-web/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # API routes and web endpoints
│   ├── game/
│   │   ├── __init__.py
│   │   ├── cardgame.py      # Game logic
│   │   └── deck.txt         # Card deck definition
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Application styling
│   │   └── js/
│   │       └── game.js      # Client-side game logic
│   └── templates/
│       ├── base.html        # Base template with common elements
│       ├── index.html       # Home page with game instructions
│       └── game.html        # Game interface
├── config.py                # Application configuration
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd card-game-web
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Open your web browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

## API Endpoints

- `GET /` - Home page with game instructions
- `GET /game` - Game interface
- `POST /api/game/start` - Start a new game
- `POST /api/game/guess` - Make a guess during the game
- `POST /api/game/reset` - Reset the current game

## Development

To run the application in development mode:

```bash
export FLASK_ENV=development
python run.py
```

## Deployment

The application can be deployed to various platforms like Heroku, AWS, or any other platform that supports Python applications.

For Heroku deployment:

1. Create a Procfile:
   ```
   web: gunicorn run:app
   ```

2. Deploy to Heroku:
   ```bash
   heroku create
   git push heroku main
   ```

## License

This project is open source and available under the MIT License.
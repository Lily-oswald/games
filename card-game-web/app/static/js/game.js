document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const startGameBtn = document.getElementById('start-game');
    const playAgainBtn = document.getElementById('play-again');
    const gameMessage = document.getElementById('game-message');
    const deckCount = document.getElementById('deck-count');
    const cardsDisplay = document.getElementById('cards-display');
    const guessControls = document.getElementById('guess-controls');
    const optionsButtons = document.getElementById('options-buttons');
    const question = document.getElementById('question');
    const gameOverDisplay = document.getElementById('game-over-display');
    const gameResult = document.getElementById('game-result');

    // Game state
    let gameActive = false;
    let gameId = null;

    // Card suit symbols
    const suitSymbols = {
        'hearts': '♥',
        'diamonds': '♦',
        'clubs': '♣',
        'spades': '♠'
    };

    // Initialize the game
    function init() {
        startGameBtn.addEventListener('click', startGame);
        playAgainBtn.addEventListener('click', startGame);
    }

    // Start a new game
    function startGame() {
        // Reset UI
        resetGameUI();
        
        // Hide start button and show loading state
        startGameBtn.style.display = 'none';
        gameMessage.textContent = 'Starting a new game...';
        
        // API call to start a game
        fetch('/api/game/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            gameId = data.game_id;
            gameActive = true;
            deckCount.textContent = data.deck_remaining;
            gameMessage.textContent = data.message;
            
            // Show game controls and options for the first step
            showNextStep(data.next_action);
        })
        .catch(error => {
            console.error('Error starting game:', error);
            gameMessage.textContent = 'Error starting game. Please try again.';
            startGameBtn.style.display = 'block';
        });
    }

    // Reset the game UI
    function resetGameUI() {
        cardsDisplay.innerHTML = '';
        gameOverDisplay.style.display = 'none';
        guessControls.style.display = 'none';
        optionsButtons.innerHTML = '';
        gameActive = false;
    }

    // Show the next step of the game
    function showNextStep(stepData) {
        if (!stepData) {
            return;
        }
        
        question.textContent = stepData.prompt;
        optionsButtons.innerHTML = '';
        
        // Create buttons for each option
        stepData.options.forEach(option => {
            const button = document.createElement('button');
            button.textContent = option;
            button.className = 'btn option-btn';
            button.dataset.option = option.toLowerCase();
            
            button.addEventListener('click', function() {
                makeGuess(option);
            });
            
            optionsButtons.appendChild(button);
        });
        
        // Show the guess controls
        guessControls.style.display = 'block';
    }

    // Make a guess
    function makeGuess(guess) {
        if (!gameActive) return;
        
        // Disable buttons while processing
        const buttons = optionsButtons.querySelectorAll('button');
        buttons.forEach(btn => btn.disabled = true);
        
        gameMessage.textContent = 'Processing your guess...';
        
        // API call to make a guess
        fetch('/api/game/guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ guess: guess })
        })
        .then(response => response.json())
        .then(data => {
            // Update the message
            gameMessage.textContent = data.message;
            
            // Add the card to the display
            if (data.current_card) {
                addCardToDisplay(data.current_card);
            }
            
            // Update the state
            if (data.game_over) {
                endGame(data.success ? 'win' : 'lose', data.message);
            } else {
                // Enable buttons for next step
                buttons.forEach(btn => btn.disabled = false);
                
                // Show next step
                if (data.next_step) {
                    showNextStep(data.next_step);
                }
            }
        })
        .catch(error => {
            console.error('Error making guess:', error);
            gameMessage.textContent = 'Error processing guess. Please try again.';
            buttons.forEach(btn => btn.disabled = false);
        });
    }

    // Add a card to the display
    function addCardToDisplay(card) {
        const cardElement = document.createElement('div');
        cardElement.className = 'card card-' + card.color.toLowerCase();
        
        const cardRank = document.createElement('div');
        cardRank.className = 'card-rank';
        cardRank.textContent = card.rank;
        
        const cardSuit = document.createElement('div');
        cardSuit.className = 'card-suit';
        cardSuit.textContent = suitSymbols[card.suit.toLowerCase()] || card.suit;
        
        cardElement.appendChild(cardRank);
        cardElement.appendChild(cardSuit);
        
        cardsDisplay.appendChild(cardElement);
    }

    // End the game
    function endGame(result, message) {
        gameActive = false;
        guessControls.style.display = 'none';
        gameOverDisplay.style.display = 'block';
        
        if (result === 'win') {
            gameResult.textContent = '🎉 You Win! 🎉';
        } else {
            gameResult.textContent = 'Game Over!';
        }
        
        // Reset the game on server
        fetch('/api/game/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).catch(err => console.error('Error resetting game:', err));
    }

    // Initialize the game
    init();
});
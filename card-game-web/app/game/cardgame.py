import random
import os

# Ordered list of card ranks for comparison
RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

def load_deck(filename=None):
    """Load the deck from a text file into a list of cards (dicts)."""
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), "deck.txt")
        
    deck = []
    with open(filename, "r") as f:
        for line in f:
            rank, suit, color = line.strip().split(",")
            deck.append({"rank": rank, "suit": suit, "color": color})
    return deck

def draw_card(deck, forbidden_suits=None, color_choice=None):
    """Draw a random card from the deck, avoiding forbidden suits and optional color filter."""
    available = deck.copy()  # Create a copy to avoid modifying the original
    if color_choice:
        available = [card for card in available if card["color"].lower() == color_choice.lower()]
    if forbidden_suits:
        available = [card for card in available if card["suit"] not in forbidden_suits]

    if not available:
        return None

    card = random.choice(available)
    deck.remove(card)  # Remove from the original deck
    return card

def rank_value(card):
    """Convert rank string to a comparable number."""
    return RANKS.index(card["rank"])

class CardGame:
    """A class to manage the card game state for the web version."""
    
    STEPS = ["color", "highlow", "betweenoutside", "suit"]
    
    def __init__(self):
        """Initialize a new game with a fresh deck."""
        self.deck = load_deck()
        self.current_step = 0
        self.cards = []
        self.current_card = None
        self.forbidden_suits = set()
        self.score = 0
        self.game_over = False
        self.game_message = "Let's play! Start by guessing Red or Black."
        
    def check_game_status(self):
        """Check if the game can continue."""
        # If we're out of cards, reload the deck
        if len(self.deck) < (4 - len(self.cards)):
            # This will only happen if we've almost gone through the entire deck
            # In a real game, you might want to shuffle in discards instead
            self.deck = load_deck()  # Reload a fresh deck
            self.game_message = "Reshuffled deck to continue the game."
            return True
        return True
    
    def get_current_step(self):
        """Get information about the current step."""
        if self.current_step >= len(self.STEPS):
            return None
        
        step_type = self.STEPS[self.current_step]
        
        if step_type == "color":
            return {
                "type": "color",
                "prompt": "Red or Black?",
                "options": ["Red", "Black"]
            }
        elif step_type == "highlow":
            return {
                "type": "highlow",
                "prompt": "Higher or Lower than the previous card?",
                "options": ["Higher", "Lower"],
                "context": self.cards[0]
            }
        elif step_type == "betweenoutside":
            return {
                "type": "betweenoutside",
                "prompt": "Will the next card be in between or outside the previous two cards?",
                "options": ["In Between", "Outside"],
                "context": [self.cards[0], self.cards[1]]
            }
        elif step_type == "suit":
            return {
                "type": "suit",
                "prompt": "Guess the suit of the next card",
                "options": ["Hearts", "Diamonds", "Clubs", "Spades"]
            }
        return None
    
    def make_guess(self, guess):
        """Process a user's guess."""
        if self.game_over or not self.check_game_status():
            return False
            
        step_type = self.STEPS[self.current_step]
        result = False
        
        # Process the guess based on current step
        if step_type == "color":
            self.current_card = draw_card(self.deck)
            self.cards.append(self.current_card)
            
            result = self.current_card["color"].lower() == guess.lower()
            if result:
                self.game_message = f"Correct! The card was {self.current_card['rank']} of {self.current_card['suit']} ({self.current_card['color']})."
                self.current_step += 1
                self.forbidden_suits.add(self.current_card["suit"])
            else:
                self.game_message = f"Wrong! The card was {self.current_card['rank']} of {self.current_card['suit']} ({self.current_card['color']}). Game over!"
                self.game_over = True
            
        elif step_type == "highlow":
            self.current_card = draw_card(self.deck, forbidden_suits=self.forbidden_suits)
            self.cards.append(self.current_card)
            self.forbidden_suits.add(self.current_card["suit"])
            
            card1_value = rank_value(self.cards[0])
            card2_value = rank_value(self.current_card)
            
            if guess.lower() == "higher":
                result = card2_value > card1_value
            else:  # "lower"
                result = card2_value < card1_value
                
            if result:
                self.game_message = f"Correct! The card was {self.current_card['rank']} of {self.current_card['suit']} ({self.current_card['color']})."
                self.current_step += 1
            else:
                self.game_message = f"Wrong! The card was {self.current_card['rank']} of {self.current_card['suit']} ({self.current_card['color']}). Game over!"
                self.game_over = True
                
        elif step_type == "betweenoutside":
            self.current_card = draw_card(self.deck, forbidden_suits=self.forbidden_suits)
            self.cards.append(self.current_card)
            self.forbidden_suits.add(self.current_card["suit"])
            
            low, high = sorted([rank_value(self.cards[0]), rank_value(self.cards[1])])
            val3 = rank_value(self.current_card)
            
            if low < val3 < high:
                actual_result = "in between"
            else:
                actual_result = "outside"
                
            result = actual_result == guess.lower()
            
            if result:
                self.game_message = f"Correct! The card was {self.current_card['rank']} of {self.current_card['suit']} ({self.current_card['color']})."
                self.current_step += 1
            else:
                self.game_message = f"Wrong! The card was {self.current_card['rank']} of {self.current_card['suit']} ({self.current_card['color']}). Game over!"
                self.game_over = True
                
        elif step_type == "suit":
            self.current_card = draw_card(self.deck)
            self.cards.append(self.current_card)
            
            result = self.current_card["suit"].lower() == guess.lower()
            
            if result:
                self.game_message = f"🎉 You win! The card was {self.current_card['rank']} of {self.current_card['suit']} ({self.current_card['color']})."
                self.score += 1
                self.game_over = True
            else:
                self.game_message = f"So close! The card was {self.current_card['rank']} of {self.current_card['suit']} ({self.current_card['color']}). Game over!"
                self.game_over = True
                
        return {
            "success": result,
            "message": self.game_message,
            "game_over": self.game_over,
            "current_card": self.current_card,
            "next_step": self.get_current_step() if not self.game_over else None
        }
    
    def get_game_state(self):
        """Return the current state of the game."""
        return {
            "deck_remaining": len(self.deck),
            "current_step": self.current_step,
            "cards": self.cards,
            "game_over": self.game_over,
            "message": self.game_message,
            "score": self.score,
            "next_action": self.get_current_step()
        }
        print(f"The card is: {card4['rank']} of {card4['suit']} ({card4['color']})")

        if guess == card4["suit"]:
            print("🎉 You win! 🎉")
            return
        else:
            print("Wrong! Starting over...\n")

    print("Deck doesn’t have enough cards left to continue.")

if __name__ == "__main__":
    game = CardGame()
    print("Game created!")
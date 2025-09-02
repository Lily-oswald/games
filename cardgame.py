import random

# Ordered list of card ranks for comparison
RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

def load_deck(filename="deck.txt"):
    """Load the deck from a text file into a list of cards (dicts)."""
    deck = []
    with open(filename, "r") as f:
        for line in f:
            rank, suit, color = line.strip().split(",")
            deck.append({"rank": rank, "suit": suit, "color": color})
    return deck

def draw_card(deck, forbidden_suits=None, color_choice=None):
    """Draw a random card from the deck, avoiding forbidden suits and optional color filter."""
    available = deck
    if color_choice:
        available = [card for card in available if card["color"].lower() == color_choice.lower()]
    if forbidden_suits:
        available = [card for card in available if card["suit"] not in forbidden_suits]

    if not available:
        return None

    card = random.choice(available)
    deck.remove(card)
    return card

def rank_value(card):
    """Convert rank string to a comparable number."""
    return RANKS.index(card["rank"])

def play_game():
    deck = load_deck()
    print("Let's play a game! (enter stop at any point to quit)\n")

    while len(deck) >= 4:  # need at least 4 cards for full round
        # Step 1: Red or Black
        choice = input("Red or Black? ").strip()
        if choice.lower() == "stop":
            print("Game stopped.")
            return

        card1 = draw_card(deck)
        if not card1:
            print("Deck is empty!")
            return
        print(f"First card: {card1['rank']} of {card1['suit']} ({card1['color']})")

        if card1["color"].lower() != choice.lower():
            print("Wrong! It was", card1['color'], end='')
            print("! Starting over...\n")
            continue
        print("Correct!\n")

        # Step 2: Higher or Lower
        guess = input("Higher or Lower? ").strip().lower()
        if guess == "stop":
            print("Game stopped.")
            return

        card2 = draw_card(deck, forbidden_suits={card1["suit"]})
        if not card2:
            print("Deck is empty!")
            return
        print(f"Second card: {card2['rank']} of {card2['suit']} ({card2['color']})")

        if (guess == "higher" and rank_value(card2) > rank_value(card1)) or \
           (guess == "lower" and rank_value(card2) < rank_value(card1)):
            print("Correct!\n")
            
        else:
            print("Wrong! Starting over...\n")
            continue

        # Step 3: In Between or Outside
        guess = input("In Between or Outside? ").strip().lower()
        if guess == "stop":
            print("Game stopped.")
            return

        card3 = draw_card(deck, forbidden_suits={card1["suit"], card2["suit"]})
        if not card3:
            print("Deck is empty!")
            return
        print(f"Third card: {card3['rank']} of {card3['suit']} ({card3['color']})")

        low, high = sorted([rank_value(card1), rank_value(card2)])
        val3 = rank_value(card3)

        if low < val3 < high:
            result = "in between"
        else:
            result = "outside"

        if guess == result:
            print("Correct!\n")
        else:
            print("Wrong! Starting over...\n")
            continue

        # Step 4: Guess the Suit
        guess = input("Guess the suit (Hearts, Diamonds, Clubs, Spades): ").strip().capitalize()
        card4 = draw_card(deck)
        print(f"The card is: {card4['rank']} of {card4['suit']} ({card4['color']})")

        if guess == card4["suit"]:
            print("🎉 You win! 🎉")
            return
        else:
            print("Wrong! Starting over...\n")

    print("Deck doesn’t have enough cards left to continue.")

if __name__ == "__main__":
    play_game()

import random

def number_guessing_game():
    """Main number guessing game function."""
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("Can you guess what it is?\n")
    
    # Generate random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    
    while True:
        try:
            guess = input("Enter your guess (or 'quit' to exit): ")
            
            if guess.lower() == 'quit':
                print(f"Thanks for playing! The number was {secret_number}")
                break
                
            guess = int(guess)
            attempts += 1
            
            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100!")
                continue
                
            if guess < secret_number:
                print("Too low! Try a higher number.")
            elif guess > secret_number:
                print("Too high! Try a lower number.")
            else:
                print(f"Congratulations! You guessed it in {attempts} attempts!")
                break
                
        except ValueError:
            print("Please enter a valid number!")
    
    return attempts

def play_multiple_rounds():
    """Allow playing multiple rounds and track best score."""
    best_score = float('inf')
    rounds_played = 0
    
    while True:
        rounds_played += 1
        print(f"\n--- Round {rounds_played} ---")
        
        attempts = number_guessing_game()
        
        if attempts < best_score:
            best_score = attempts
            print(f"New best score: {best_score} attempts!")
        
        play_again = input("\nWould you like to play again? (yes/no): ")
        if play_again.lower() not in ['yes', 'y']:
            break
    
    print(f"\nGame Over! You played {rounds_played} round(s).")
    if best_score != float('inf'):
        print(f"Your best score was {best_score} attempts.")
    print("Thanks for playing!")

if __name__ == "__main__":
    play_multiple_rounds()
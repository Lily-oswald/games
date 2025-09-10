import math

def piece_of_pi():
    # Get digits of pi as a string (50 digits after the decimal for now)
    pi_digits = str(math.pi).replace(".", "")[:51]  # "314159..." up to 50 digits
    
    print("Welcome to Piece of Pi!")
    print("Try to guess the digits of π one at a time.")
    print("We'll stop when you make a mistake.\n")
    
    score = 0
    
    for i, digit in enumerate(pi_digits):
        guess = input(f"Digit #{i+1}: ")
        
        if guess == digit:
            print("Correct!")
            score += 1
            # Show the correct digits so far, formatted as 3.14...
            if score == 1:
                display = pi_digits[0]
            else:
                display = pi_digits[0] + "." + pi_digits[1:score]
            print(display, "\n")
        else:
            print(f"Wrong! The correct digit was {digit}.")
            break
    
    print(f"\nGame Over! You got {score} digits correct.")
    if score == 1:
        display = pi_digits[0]
    elif score > 1:
        display = pi_digits[0] + "." + pi_digits[1:score]
    else:
        display = ""
    print(f"The first {score} digits of π are: {display}")

# Run the game
if __name__ == "__main__":
    piece_of_pi()

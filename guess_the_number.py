import random

player_name = input("Enter your name: ")
print()

# Pick a random number between 1 and 100
secret_number = random.randint(1, 100)

attempts = 0
lives = 5
guessed_correctly = False

print(f"Welcome, {player_name}!")
print("I'm thinking of a number between 1 and 100.")
print(f"You have {lives} lives: {'❤️ ' * lives}")

while not guessed_correctly and lives > 0:
    guess = int(input("Enter your guess: "))
    print()
    attempts += 1

    if guess < secret_number:
        lives -= 1
        print("Too low! Try again.")
        print(f"Lives left: {'❤️ ' * lives}")
        print()
    elif guess > secret_number:
        lives -= 1
        print("Too high! Try again.")
        print(f"Lives left: {'❤️ ' * lives}")
        print()
    else:
        guessed_correctly = True
        print(f"Correct! The number was {secret_number}.")
        print(f"You guessed it in {attempts} attempts.")

if not guessed_correctly:
    print(f"Game over! You ran out of lives. The number was {secret_number}.")
else:
    # Save this result to the leaderboard file
    with open("leaderboard.txt", "a") as file:
        file.write(f"{player_name},{attempts}\n")

# ---------- Show the leaderboard ----------
print()
print("=== LEADERBOARD (fewest attempts wins) ===")

try:
    with open("leaderboard.txt", "r") as file:
        lines = file.readlines()

    records = []
    for line in lines:
        name, tries = line.strip().split(",")
        records.append((name, int(tries)))

    records.sort(key=lambda record: record[1])

    for position, (name, tries) in enumerate(records[:5], start=1):
        print(f"{position}. {name} - {tries} attempts")

except FileNotFoundError:
    print("No records yet.")
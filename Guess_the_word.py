# Guess the word game
# Color-coded Feedback
import sys
import random
import asyncio
    
def load_game_data(game_data_file):
    game_data = {}
    try:
        with open(game_data_file, "r") as file:
            for line in file:
                category, words = line.strip().split(": ")
                game_data[category] = words.split(", ")
    except FileNotFoundError:
        print(f"Error: The file '{game_data_file}' was not found!")
    except Exception as e:
        print(f"An error occurred while loading game data: {e}")
    return game_data

def load_players_data(players_data_file):
    players_data = {}
    try:
        with open(players_data_file, "r") as file:
            for line in file:
                name, score = line.strip().split(": ")
                players_data[name] = int(score)
    except FileNotFoundError:
        print(f"Error: The file '{players_data_file}' was not found!")
    except Exception as e:
        print(f"An error occurred while loading players data: {e}")
    return players_data

def save_players_data(players_data_file, dic):
    with open(players_data_file, "w") as file:
        for name, score in dic.items():
            file.write(f"{name}: {score}\n")

def hangman_game(dic):
    chosen_words = []
    score = 0
    
    if not words:
        print("No game data available.")
        return
    else:  
        print("Game data loaded successfully.")
    if not players:
        print("No players data available.")
        return
    else:
        print("Players data loaded successfully.\nYou can start playing the game.\n")

    print("Welcome to the Hangman Game\nThe attempts will be reset after right guess.\nThe game ends if you ran out of attempts or you won, you won at score 200.\n")
    player_name = input("Enter your name: ").strip()
    if player_name in players:
            print(f"Welcome back, *{player_name}* Your current score is: '{players[player_name]}'pts.")
            score = players[player_name]
    else:
        print(f"Welcome, *{player_name}* You are a new player.")
        players[player_name] = 0
        print(f"Your current score is: '{score}' pts.")
    
    difficulty = input("Choose difficulty level (easy--medium--hard): ").lower().strip()
    if difficulty not in ["easy", "medium", "hard"]:
        print("Invalid difficulty level! Defaulting to 'medium'.")
        difficulty = "medium"
    if difficulty == "easy":
        intitial_attempts = 10
    elif difficulty == "medium":    
        intitial_attempts = 7
    else:
        intitial_attempts = 5
    print(f"You have '{intitial_attempts}' attempts to guess the word.")
    attempts = intitial_attempts
    
    categories = [i for i in words.keys()]    
    while attempts > 0:
        
        choosen_category = random.choice(categories)
        print(f"\nThe category choosen for you is:\n{'='*20}\n*{choosen_category}*\n{'='*20}")
        remaining_words = [word for word in dic[choosen_category] if word not in chosen_words]
        if not remaining_words:
            print(f"All words in the category '{choosen_category}' have been guessed!")
            continue

        choosen_word = random.choice(remaining_words)
        unknown_word = ["_"] * len(choosen_word)
        guessed_letters = []
        
        print(f"The word is: {" ".join(unknown_word)}")
        
        while True:
            # intergrating the time limit for each word
            guessed_letter = input("Enter the letter: ")
            if guessed_letter == "/commands":
                print("Available commands: (/hint, /exit, /players ,/commands,)")
                continue
            elif guessed_letter == "/players":
                print("The players and their scores are:")
                for player, score in players.items():
                    print(f"{player}: {score} pts")
                continue
            elif guessed_letter == "/hint":
                if attempts > 1 or score > 20:
                    attempts_dedution = {"easy": 1, "medium": 2, "hard": 3}
                    if attempts > attempts_dedution[difficulty]:
                        attempts -= attempts_dedution[difficulty]
                        print(f"Hint used! You have '{attempts}' attempts left.")
                    else:
                        score -= 20
                        print(f"Hint used! You lost 20 points. Your score is now '{score}' points.")
                        
                    unrevealed_letters = [i for i, char in enumerate(unknown_word) if char == "_"]
                    if unrevealed_letters:
                        hint_index = random.choice(unrevealed_letters)
                        unknown_word[hint_index] = choosen_word[hint_index]
                        print(f"Hint: The word now is {' '.join(unknown_word)}\n")
                else:
                    print("You don't have enough attempts or points to use a hint.")    
                continue
            elif guessed_letter == "/exit":
                print("Exiting the game. Thank you for playing!")
                return
            elif len(guessed_letter) != 1 or guessed_letter.isalpha() == False:
                print("Invalid input! Please enter a single alphabetic letter.\n")
                continue
            elif guessed_letter in unknown_word:
                print(f"You already guessed that letter! Guessed letters: {', '.join(guessed_letters)}")
                continue
            guessed_letters.append(guessed_letter)
            
            if guessed_letter in choosen_word:
                for idx, char in enumerate(choosen_word):
                    if char == guessed_letter:
                        unknown_word[idx] = guessed_letter        
                print(f"The word now is: {" ".join(unknown_word)}\n")        
            else:
                attempts -= 1
                print(f"Wrong guess! You have {attempts} attempts left.\n")    
                if attempts == 0:
                    print(f"Game over! The word was: '{choosen_word}'.")
                    print(f"Game over! your score is {score} pts.")
                    break
                
            if "".join(unknown_word) == choosen_word:
                score += 12
                attempts = intitial_attempts
                players [player_name] = score
                print(f"Congratulations*{player_name}* You guessed right, The word is: '{choosen_word}', Your score now is: '{score}'pts, You have '{attempts}' attempts now.")
                chosen_words.append(choosen_word)
                break
            
        if score > 200:
            print(f"*Congratulations *{player_name}*, You have won the game with a score of '{score}' pts.*")
            print("Thank you for playing!")
            break
        
        save_players_data("playersdata.txt", players)
    
words = load_game_data("gamedata.txt")    
players = load_players_data("playersdata.txt")
hangman_game(words)
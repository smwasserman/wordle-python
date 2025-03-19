import random


def get_word_length() -> int:
    while True:
        try:
            word_length = int(input("Enter a length of word to play with.\nLENGTH> "))
            if word_length not in range(2, 23):
                raise ValueError
            return word_length
        except ValueError:
            print("Please input a valid length")


def get_word_bank(word_length: int) -> list:
    with open('dictionary.txt', 'r') as dictionary:
        word_bank = [word.strip('\n') for word in dictionary if len(word.strip('\n')) == word_length]
    return word_bank


def get_new_guess(word_length: int, word_bank: list, used_guesses: list) -> str:
    while True:
        try:
            new_guess = input(f'\nGUESS_{len(used_guesses) + 1}> ').casefold()
            if len(new_guess) != word_length:
                raise ValueError(f"Please enter a {word_length}-letter word.")
            if new_guess not in word_bank:
                raise ValueError("Please enter a real word")
            if new_guess in used_guesses:
                raise ValueError("Please enter a word you haven't guessed yet.")
            return new_guess
        except ValueError as error_message:
            print(error_message)


def gen_row_colors(guess_word: str, secret_word: str, word_length: int) -> list:
    color_list = ['Gray'] * word_length
    secret_word = list(secret_word)
    for i, (guess_char, secret_char) in enumerate(zip(guess_word, secret_word)):
        if guess_char == secret_char:
            color_list[i], secret_word[i] = 'Green', '_'
    for i, guess_char in enumerate(guess_word):
        for j, secret_char in enumerate(secret_word):
            if guess_char == secret_char and color_list[i] != 'Green':
                color_list[i], secret_word[j] = 'Yellow', '_'
    return color_list


def gen_keyboard_colors(key_colors: dict, new_guess: str, guess_color: list):
    for letter, color in zip(new_guess, guess_color):
        if color == 'Green':
            key_colors[letter] = 'Green'
        elif key_colors[letter] == 'White':
            key_colors[letter] = color


def color_letter(letter: str, color: str) -> str:
    colors = {
        'Green': f"\033[97m\033[42m\033[01m {letter.upper()} \033[00m",
        'Yellow': f"\033[97m\033[43m\033[01m {letter.upper()} \033[00m",
        'Gray': f"\033[97m\033[100m\033[01m {letter.upper()} \033[00m",
        'White': f"\033[30m\033[48;5;255m\033[01m {letter.upper()} \033[00m"
    }
    return colors.get(color, ' ')


def print_table(used_guesses: list, color_list: list, word_length: int):
    indent = (((10 - word_length) * 3 // 2) - 1) * ' ' if word_length < 10 else ''
    for i in range(6):
        try:
            print(indent, ''.join(map(color_letter, used_guesses[i], color_list[i])))
        except IndexError:
            print(indent, '\n'.join([color_letter(letter=' ', color='White') * word_length]))


def print_keyboard(key_colors: dict):
    keyboard, _ = ['QWERTYUIOP', '_ASDFGHJKL', '____ZXCVBNM'], print('')
    [print(''.join([color_letter(key, key_colors.get(key.casefold())) for key in row])) for row in keyboard]


def check_if_game_over(new_guess: str, secret_word: str, used_guesses: list) -> str:
    if new_guess == secret_word:
        print(f"\nCongratulations! You guessed the word '{secret_word.upper()}' in {len(used_guesses)} guesses!")
        return 'W'
    elif len(used_guesses) == 6:
        print(f"\nYOU LOSE!\nYou were not able to guess the secret word '{secret_word.upper()}'.")
        return 'L'
    else:
        return ''


def play_again() -> bool:
    while True:
        try:
            keep_playing = input("Would you like to play again? (Yes or No)\nCONTINUE? ")
            if keep_playing.casefold() in {'yes', 'y'}:
                return True
            elif keep_playing.casefold() in {'no', 'n'}:
                return False
            else:
                raise ValueError
        except ValueError:
            print('Please answer Yes or No')


def run_game():
    word_length = get_word_length()
    word_bank = get_word_bank(word_length)
    random.seed(input('Enter a seed to start the random number generator.\nSEED> '))
    result_list, keep_playing = [], True
    while keep_playing:
        result, used_guesses, guess_color_list = '', [], []
        key_colors = {letter: 'White' for letter in 'abcdefghijklmnopqrstuvwxyz'}
        secret_word = random.choice(word_bank)
        print(f"\nI've chosen a secret {word_length}-letter word. Make a guess.\n")
        while not result:
            print_table(used_guesses, guess_color_list, word_length)
            print_keyboard(key_colors)
            new_guess = get_new_guess(word_length, word_bank, used_guesses)
            used_guesses.append(new_guess)
            guess_color = gen_row_colors(new_guess, secret_word, word_length)
            guess_color_list.append(guess_color)
            gen_keyboard_colors(key_colors, new_guess, guess_color)
            result = check_if_game_over(new_guess, secret_word, used_guesses)
        result_list.append(result)
        print_table(used_guesses, guess_color_list, word_length)
        keep_playing = play_again()
    print(f"You won {result_list.count('W')} time{'s' if result_list.count('W') != 1 else ''} "
          f"and lost {result_list.count('L')} time{'s' if result_list.count('L') != 1 else ''}")


if __name__ == '__main__':
    run_game()

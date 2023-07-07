import sys, time

with open(r"possible_words.txt", "r") as f: # gets all possible words and stores it in a list
    possible_words = f.read().split("\n")

orig_len = len(possible_words)

incorrect_letters = []

misplaced_letters = []
misplaced_letters_pos = []

correct_letters = []
correct_letters_pos = []

removed_words = []

def gather_data(): # gets guess and result and translates into list data
    global incorrect_letters, misplaced_letters, misplaced_letters_pos, correct_letters, correct_letters_pos
    guess = input("\nEnter your guess: ")

    if guess == "exit":
        sys.exit()

    output = input("\nEnter the result: ")

    if output == "fup":
        gather_data()

    incorrect_letters, misplaced_letters, misplaced_letters_pos, correct_letters, correct_letters_pos = translate_data(guess, output)

def translate_data(guess, output): # caegorizes every letter into its right list based off result
    i_ltr, m_ltr, m_ltr_pos, c_ltr, c_ltr_pos = [], [], [], [], []
    for i, x in enumerate(output):
        if x == "i":
            i_ltr.append(guess[i])
        if x == "m":
            m_ltr.append(guess[i])
            m_ltr_pos.append(i) # stores index for misplaced and correct letters since that's important
        if x == "c":
            c_ltr.append(guess[i])
            c_ltr_pos.append(i)
    return i_ltr, m_ltr, m_ltr_pos, c_ltr, c_ltr_pos


def eliminate_words(incorrect_letters, misplaced_letters, misplaced_letters_pos, correct_letters, correct_letters_pos, recommending): # removes words that cannot be the answer based off data gathered
    impossible_words = []
    for word in possible_words:
        for index, letter in enumerate(word):
            if letter in incorrect_letters and letter not in misplaced_letters:
                impossible_words.append(word) # stores immpossible words in a list rather than removing them here because it's bad practice to remove an element while you're iterating through the list
                continue

            for i, correct_ltr in enumerate(correct_letters):
                if letter != correct_ltr and index == correct_letters_pos[i]:
                    impossible_words.append(word)
                    continue

            for i, misplaced_letter in enumerate(misplaced_letters):
                if misplaced_letter not in word:
                    impossible_words.append(word)
                    continue

                if letter == misplaced_letter and index == misplaced_letters_pos[i]:
                    impossible_words.append(word)
    if not recommending: # only removes if we actually want to and not when we're trying to reccomend a word to the user
        for word in impossible_words:
            if word not in removed_words: # some words will be in the impossible words list multiple times - stops error from happening
                possible_words.remove(word)
            removed_words.append(word)
    else:
        return len(set(impossible_words))

def translate_to_output(guess, target):
    output = ""
    for i, letter in enumerate(guess):
        if letter in target:
            if target.index(letter) == i:
                output += "c"
            else:
                output += "m"
        else:
            output += "i"
    return output

def recommend_advanced_guess():
    global best_word
    max_words_removed = 0
    best_word = ""
    for word in possible_words:
        specific_permutations = {}
        total_permutations = 0
        for target_word in possible_words:
            if target_word != word:
                output = translate_to_output(word, target_word)
                if output in specific_permutations:
                    specific_permutations[output] += 1
                else:
                    specific_permutations[output] = 1
                total_permutations += 1

        average_words_removed = 0
        for permutation in specific_permutations:
            incorrect_letters, misplaced_letters, misplaced_letters_pos, correct_letters, correct_letters_pos = translate_data(word, permutation)
            average_words_removed += eliminate_words(incorrect_letters, misplaced_letters, misplaced_letters_pos, correct_letters, correct_letters_pos, True) * specific_permutations[permutation]

        if total_permutations != 0:
            average_words_removed /= total_permutations
        else:
            return possible_words[0]
        if average_words_removed > max_words_removed:
            max_words_removed = average_words_removed
            best_word = word
            print(f"new best: {best_word}, {average_words_removed}")

        print(f"{word} completed, {round(possible_words.index(word)/len(possible_words) * 100, 3)}% finished")

    return best_word

    
for i in range(6):
    gather_data()
    start = time.perf_counter()
    eliminate_words(incorrect_letters, misplaced_letters, misplaced_letters_pos, correct_letters, correct_letters_pos, False)

    print(f"\n{possible_words}\n")
    end = time.perf_counter()
    
    if len(possible_words) < 13000:
        arstart = time.perf_counter()
        print(f"ADVANCED Guess: {recommend_advanced_guess()}\n")
        arend = time.perf_counter()
        print(f"Advanced Search took {arend - arstart}s")

    print(f"Eliminated {orig_len - len(possible_words)} words in {end - start}s")
    orig_len = len(possible_words)
    

    

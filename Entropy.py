import os, sys, time, math

with open(r"possible_words.txt", "r") as f: # gets all possible words and stores it in a list
    possible_words = f.read().split("\n")

orig_len = len(possible_words)
last_score = 0

incorrect_letters = []

misplaced_letters = []
misplaced_letters_pos = []

correct_letters = []
correct_letters_pos = []

removed_words = []

def gather_data(): # gets guess and result and translates into list data
    global incorrect_letters, misplaced_letters, misplaced_letters_pos, correct_letters, correct_letters_pos
    guess = input("Enter your guess: ")

    if guess == "exit":
        sys.exit()

    if guess == "rs":
        os.system("cls")
        os.system("cls")
        os.execv(sys.executable, ['python'] + sys.argv)

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
            if letter in incorrect_letters and letter not in misplaced_letters and letter not in correct_letters:
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
            if guess[i] == target[i]:
                output += "c"
            else:
                output += "m"
        else:
            output += "i"
    return output

def recommend_advanced_guess():
    global best_word
    best_score = 0
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

        score = 0
        for permutation in specific_permutations:
            score += math.log2(1/(specific_permutations[permutation]/len(possible_words))) * (specific_permutations[permutation]/len(possible_words))

        if score > best_score:
            best_score = score
            best_word = word
            #print(f"new best: {best_word}, {best_score}")

        #print(f"{word} completed, {round(possible_words.index(word)/len(possible_words) * 100, 3)}% finished")

    return best_word, best_score
    
for i in range(6):
    gather_data()
    start = time.perf_counter()
    eliminate_words(incorrect_letters, misplaced_letters, misplaced_letters_pos, correct_letters, correct_letters_pos, False)

    print("\n----------------------------------")
    print(f"Information Gained: {math.log2(orig_len - len(possible_words) + 1)} bits - {round(math.log2(orig_len - len(possible_words) + 1)/math.log2(orig_len)*100, 2)}%")
    if len(possible_words) <= 20:
        print(f"\nWords Left: {(possible_words)}\n")
    else:
        print(f"\nWords Left: {len(possible_words)}\n")
    end = time.perf_counter()
    
    arstart = time.perf_counter()
    best_word, score = recommend_advanced_guess()
    if best_word == "" and len(possible_words) == 1: best_word = possible_words[0]
    print(f"Guess: {best_word}\n")
    print(f"Uncertainty: {math.log2(len(possible_words))} bits\n")
    print(f"Expected Score: {score} bits\n")
    arend = time.perf_counter()
    print(f"Search took {round((arend - arstart)*1000, 3)}ms")

    print(f"Eliminated {orig_len - len(possible_words)} words in {round((end - start)*1000, 3)}ms")
    print("----------------------------------\n")
    orig_len = len(possible_words)
    last_score = score

    

    

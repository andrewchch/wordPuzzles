
from nltk.corpus import words as nltk_words


def extract_words(puzzle):
    """Extract words from the puzzle."""
    words = []

    # Extracting row words
    for row in puzzle:
        word = ''.join([cell[0] for cell in row if cell[0] != ''])
        if len(word) == 5:
            words.append(word)

    # Extracting column words
    for col in range(len(puzzle[0])):
        word = ''.join([puzzle[row][col][0] for row in range(len(puzzle)) if puzzle[row][col][0] != ''])
        if len(word) == 5:
            words.append(word)

    return words


def evaluate(puzzle):
    """Evaluate the puzzle configuration."""
    green_count = sum([1 for row in puzzle for cell in row if cell[1] == "green"])
    yellow_count = sum([1 for row in puzzle for cell in row if cell[1] == "yellow"])
    score = green_count - yellow_count
    return score


def update_puzzle_state(puzzle, row_column_candidate_words, available_letters):
    """
    Compare each word in the puzzle to the candidate words for that row/column. If a letter matches, set that letter color to green.
    :param puzzle:
    :param row_column_candidate_words:
    :return:
    """

def swap_cells(puzzle, pos1, pos2):
    """Swap two cells in the puzzle."""
    puzzle[pos1[0]][pos1[1]], puzzle[pos2[0]][pos2[1]] = puzzle[pos2[0]][pos2[1]], puzzle[pos1[0]][pos1[1]]


def constrain_word_list(puzzle_word, all_words, puzzle_letters):
    """Constrain the list of potential words based on green letters."""
    green_positions = [i for i, cell in enumerate(puzzle_word) if cell[1] == "green"]

    # Filter the words based on green letters
    constrained_words = set()
    for word in all_words:
        if all(word[i] == puzzle_word[i][0] for i in green_positions):
            # further check whether the candidate word only contains the letters in the puzzle
            # todo: eliminate words that use more of a letter than is available in the puzzle
            if set(word).issubset(puzzle_letters):
                constrained_words.add(word)

    return constrained_words


def get_constrained_word_lists(puzzle, all_words, puzzle_letters):
    """Get constrained word lists for all row/column words in the puzzle."""
    constrained_lists = {}

    # For each row word
    for i, row in enumerate(puzzle):
        word = ''.join([cell[0] for cell in row if cell[0] is not None])
        if len(word) == 5:
            constrained_lists[(i, "row")] = constrain_word_list(row, all_words, puzzle_letters)

    # For each column word
    for j in range(len(puzzle[0])):
        col = [puzzle[i][j] for i in range(len(puzzle))]
        word = ''.join([cell[0] for cell in col if cell[0] != ''])
        if len(word) == 5:
            constrained_lists[(j, "col")] = constrain_word_list(col, all_words, puzzle_letters)

    return constrained_lists


def evaluate_swap(puzzle, swap_pair, constrained_word_lists):
    """Evaluate the resulting increase or decrease in score from swapping two letters."""
    # Get the positions of the two letters to swap
    pos1, pos2 = swap_pair

    # Get the words that will be affected by the swap
    affected_words = []
    if pos1[0] == pos2[0]:
        # If the letters are in the same row, get the row word and the column word that contains the letters
        affected_words.append((''.join([cell[0] for cell in puzzle[pos1[0]] if cell[0] != '']), "row"))
        affected_words.append((''.join([puzzle[row][pos1[1]][0] for row in range(len(puzzle)) if puzzle[row][pos1[1]][0] != '']), "col"))
    else:
        # If the letters are in different rows, get the row words that contain the letters
        affected_words.append((''.join([cell[0] for cell in puzzle[pos1[0]] if cell[0] != '']), "row"))
        affected_words.append((''.join([cell[0] for cell in puzzle[pos2[0]] if cell[0] != '']), "row"))

    # Get the candidate words for the affected words
    candidate_words = []
    for word, word_type in affected_words:
        candidate_words.append(constrained_word_lists[(word, word_type)])

    # Get the set of words that are common to both candidate word lists
    common_words = set.intersection(*candidate_words)

    # Get the score for the current puzzle configuration
    current_score = evaluate(puzzle)

    # Get the score for the puzzle configuration after the swap
    new_score = current_score
    for word, word_type in affected_words:
        # Get the candidate words for the affected word
        candidate_words = constrained_word_lists[(word, word_type)]

        # Get the set of words that are common to both candidate word lists
        common_words = set.intersection(common_words, candidate_words)

        # Get the score for the current puzzle configuration
        current_score = evaluate(puzzle)

        # Get the score for the puzzle configuration after the swap
        new_score = current_score
        for word, word_type in affected_words:
            # Get the candidate words for the affected word
            candidate_words = constrained_word_lists[(word, word_type)]

            # Get the set of words that are common to both candidate word lists
            common_words =

def main():
    # Get all 5-letter words in the NLTK corpus
    five_letter_words = [w for w in nltk_words.words() if len(w) == 5]

    # Initial puzzle configuration
    puzzle = [
        [("S", "green"), ("V", "white"), ("R", "yellow"), ("B", "white"), ("L", "green")],
        [("C", "white"), (None, None), ("E", "white"), (None, None), ("T", "white")],
        [("S", "yellow"), ("T", "white"), ("H", "green"), ("I", "white"), ("U", "yellow")],
        [("A", "yellow"), (None, None), ("O", "green"), (None, None), ("N", "yellow")],
        [("E", "green"), ("N", "white"), ("A", "green"), ("A", "white"), ("H", "green")]
    ]

    # Make all the letters in the puzzle lower case
    puzzle = [[(cell[0].lower(), cell[1]) if cell[0] is not None else (None, None) for cell in row] for row in puzzle]

    # Get the set of all letters in the puzzle
    puzzle_letters = set([cell[0] for row in puzzle for cell in row if cell[0] is not None])

    # Constrain word lists
    # todo: only inspect candidate words from the previous iteration rather than all words
    constrained_word_lists = get_constrained_word_lists(puzzle, five_letter_words, puzzle_letters)

    # Compile a list of possible letter swaps that do not involve swapping a green letter
    possible_swaps = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j][1] in ("yellow", "white"):
                possible_swaps.append((i, j))

    # Create a list of all possible swap pairs
    swap_pairs = []
    for pos1 in possible_swaps:
        for pos2 in possible_swaps:
            if pos1 != pos2:
                swap_pairs.append((pos1, pos2))

    # Iterate through all possible swap pairs, calculating a list of changed row/column words for each swap
    change_word_lists = {}
    swap_scores = {}


    # Create a user input loop that suggests a pair to swap and asks for the resulting puzzle state changes (in the form of the new colors of the swapped letters)
    while True:
        # Propose a pair of letters to swap

        # Split the user input into two letters
        letter1, letter2 = user_input.split()

        # Find the positions of the two letters in the puzzle
        pos1 = None
        pos2 = None
        for i, row in enumerate(puzzle):
            for j, cell in enumerate(row):
                if cell[0] == letter1:
                    pos1 = (i, j)
                if cell[0] == letter2:
                    pos2 = (i, j)

        # Swap the letters in the puzzle
        swap_cells(puzzle, pos1, pos2)

        # Print the puzzle
        for row in puzzle:
            print(row)

        # Get the user input
        user_input = input("Enter the new colors of the swapped letters: ")

        # Split the user input into two colors
        color1, color2 = user_input.split()

        # Update the colors of the swapped letters
        puzzle[pos1[0]][pos1[1]] = (puzzle[pos1[0]][pos1[1]][0], color1)
        puzzle[pos2[0]][pos2[1]] = (puzzle[pos2[0]][pos2[1]][0], color2)

        # Print the puzzle
        for row in puzzle:
            print(row)



if __name__ == "__main__":
    main()


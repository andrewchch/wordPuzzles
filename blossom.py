import itertools
import tqdm

from nltk.corpus import words as nltk_words

# Letters provided
letters = "HIGEANL"
words = set()

# Index the words that only contain the given letters and have the letter 'L'
indexed_words = {word for word in sample_dictionary if set(word).issubset(letters) and 'L' in word}

# Iterate through word lengths from 2 to the length of the letters (7)
for i in tqdm(range(4, len(letters) + 1), desc="Generating words", unit="length"):
    # Generate all possible combinations of words of length i
    for word in itertools.permutations(letters, i):
        # Check if 'L' is in the word
        if 'L' in word:
            words.add(''.join(word))

# Filter words to only keep valid words
valid_words = [word for word in words if word.lower() in nltk_words.words()]

# Sort the valid words by length in descending order and get the top 10
top_10_words = sorted(valid_words, key=len, reverse=True)[:10]
print(top_10_words)
import re
from collections import Counter

import matplotlib.pyplot as plt

# holds what homophones each alphabet maps to
INVERSE_MAPPINGS = {
    "A": ["c3", "d6", "i2", "s3", "s6", "v0", "y2"],
    "B": ["x1"],
    "C": ["a6", "c1"],
    "D": ["a7", "i6", "q0", "r4", "y9"],
    "E": ["a8", "a9", "c7", "m1", "m4", "p5", "t0", "u1"],
    "F": ["g6", "t2"],
    "G": ["h9", "v8"],
    "H": ["j1", "j6", "l1", "o9",],
    "I": ["j4", "q8", "t5", "u2", "v2"],
    "J": ["p2"],
    "L": ["e1", "m6", "o4", "p1", "s2"],
    "M": ["j7", "p3", "x0"],
    "N": ["b0", "g0", "k5"],
    "O": ["b6", "e6", "l8", "m3", "q1", "q2", "r1", "x8"],
    "P": ["c6", "j9"],
    "Q": ["u5"],
    "R": ["c4", "g2", "u4", "y4", "z0", "z7"],
    "S": ["i5", "i8", "o8", "r3", "w1", "w6"],
    "T": ["b3", "c2", "i7", "r2", "r6", "v6"],
    "U": ["m9", "q7", "y3"],
    "V": ["d8"],
    "X": ["x6"],
    "Y": ["q9", "s0"],
    "Z": ["e0"],
}


def inverse_to_mapping(inverse_mappings):
    mapping = {}
    for letter, tokens in inverse_mappings.items():
        for token in tokens:
            mapping[token] = letter
    return mapping

# this function reads the ciphertext from a file and returns it as a list of strings, split by the "|" character
def read_ciphertext(filename):
    with open(filename, "r", encoding="utf-8") as file:
        ciphertext = file.read()

    return ciphertext.split("|")

# this function checks if a given token is a homophone or not
def is_homophone(token):
    return bool(re.fullmatch(r'[a-z][0-9]', token))

# this function counts the frequency of each homophone
def count_homophones(tokens):
    frequencies = Counter()
    for token in tokens:
        if is_homophone(token):
            frequencies[token] += 1

    return frequencies

# this function counts the frequency of bigrams in the list of tokens
def count_bigrams(tokens):
    bigrams = Counter()

    previous = None

    for token in tokens:
        if is_homophone(token):

            if previous is not None:
                bigrams[(previous, token)] += 1

            previous = token

        else:
            # a non-homophonic token breaks the bigram
            previous = None

    return bigrams

# this function counts the frequency of each trigram
def count_trigrams(tokens):
    trigrams = Counter()

    previous_two = None
    previous_one = None

    for token in tokens:
        if is_homophone(token):

            if previous_two is not None and previous_one is not None:
                trigrams[(previous_two, previous_one, token)] += 1

            previous_two = previous_one
            previous_one = token

        else:
            # a non-homophonic token breaks the trigram
            previous_two = None
            previous_one = None

    return trigrams

# this function is responsible for plotting the frequencies of
# homophones, bigrams, and trigrams in a bar graph
def plot_frequencies(frequencies, limit, title):
    sorted_frequencies = frequencies.most_common(limit)
    items = [
        "-".join(item[0]) if isinstance(item[0], tuple) else item[0]
        for item in sorted_frequencies
    ]
    counts = [item[1] for item in sorted_frequencies]

    plt.figure(figsize=(12, 6))
    plt.bar(items, counts)
    plt.title(f"bar graph for{title}")
    plt.xlabel(title)
    plt.ylabel("frequency")
    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.show()


# this function takes a list of tokens and a mapping dict, and returns the translated plaintext
def translate(tokens, mapping):
    result = []
    for token in tokens:
        if token in mapping:
            result.append(mapping[token])
        elif is_homophone(token):
            result.append(token)
        else:
            result.append(token)
    return "".join(result)


# this function writes the plaintext to a file
def write_plaintext(filename, plaintext):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(plaintext)


def main():
    tokens = read_ciphertext("ciphertext.txt")
    homophones = count_homophones(tokens)
    bigrams = count_bigrams(tokens)
    trigrams = count_trigrams(tokens)

    plot_frequencies(homophones, 20, "Homophones")
    plot_frequencies(bigrams, 15, "Bigrams")
    plot_frequencies(trigrams, 10, "Trigrams")

    mapping = inverse_to_mapping(INVERSE_MAPPINGS)
    print("\nMAPPING:")
    for token in sorted(mapping):
        print(f"  {token}: {mapping[token]}")

    plaintext = translate(tokens, mapping)
    write_plaintext("plaintext.txt", plaintext)
    print("\nplaintext written to plaintext.txt")


if __name__ == "__main__":
    main()

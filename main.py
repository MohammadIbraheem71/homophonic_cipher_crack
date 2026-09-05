import re
from collections import Counter

import matplotlib.pyplot as plt

# add token -> letter mappings here as you figure them out
MAPPING = {
    # "x1": "T",
    # "p5": "H",
}


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


def main():
    tokens = read_ciphertext("ciphertext.txt")
    frequencies = count_homophones(tokens)
    bigrams = count_bigrams(tokens)
    trigrams = count_trigrams(tokens)

    plot_frequencies(frequencies, 20, "Homophones")
    plot_frequencies(bigrams, 15, "Bigrams")
    plot_frequencies(trigrams, 10, "Trigrams")

    plaintext = translate(tokens, MAPPING)
    print("\nplaintext:")
    print(plaintext)


if __name__ == "__main__":
    main()

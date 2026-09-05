import random
import re
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


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
    plt.savefig(f"{title.lower().replace(' ', '_')}.png")
    plt.close()


# added: reference english letter frequencies and top n-grams from practicalcryptography.com
ENGLISH_LETTER_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07,
}

TOP_TRIGRAMS = ["THE", "AND", "ING", "HER", "HAT", "HIS", "THA", "ERE", "RES",
               "ENT", "TIO", "TER", "EST", "ERS", "ITH", "VER", "ALL", "ONT",
               "INT", "OTH", "FTH", "STH", "FOR", "NTH", "ETH", "HES", "TIO",
               "ATI", "OFT", "STR"]

TOP_BIGRAMS = ["TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND",
               "TI", "ES", "OR", "TE", "OF", "ED", "IS", "IT", "AL", "AR"]


# added: greedy frequency-based mapping as starting point for optimization
def assign_homophones_to_letters(frequencies, letter_freq=ENGLISH_LETTER_FREQ):
    total = sum(frequencies.values())
    letter_quota = {l: (pct / 100) * total for l, pct in letter_freq.items()}

    symbols_sorted = [s for s, _ in frequencies.most_common()]
    letters_sorted = sorted(letter_quota, key=lambda l: letter_quota[l], reverse=True)

    mapping = {}
    running_total = {l: 0 for l in letter_quota}

    for sym in symbols_sorted:
        count = frequencies[sym]
        placed = False
        for letter in letters_sorted:
            if running_total[letter] + count <= letter_quota[letter] * 1.15:
                mapping[sym] = letter
                running_total[letter] += count
                placed = True
                break
        if not placed:
            letter = min(letters_sorted, key=lambda l: running_total[l] - letter_quota[l])
            mapping[sym] = letter
            running_total[letter] += count

    return mapping


# added: score a mapping by how many translated n-grams match known english patterns
def score_mapping_with_ngrams(bigrams, trigrams, mapping):
    def translate(gram):
        return "".join(mapping.get(sym, "?") for sym in gram)

    bigram_hits = sum(c for g, c in bigrams.items() if translate(g) in TOP_BIGRAMS)
    bigram_total = sum(bigrams.values())

    trigram_hits = sum(c for g, c in trigrams.items() if translate(g) in TOP_TRIGRAMS)
    trigram_total = sum(trigrams.values())

    bigram_score = bigram_hits / bigram_total if bigram_total else 0
    trigram_score = trigram_hits / trigram_total if trigram_total else 0

    return {
        "bigram_match_rate": round(bigram_score, 4),
        "trigram_match_rate": round(trigram_score, 4),
        "bigram_hits": bigram_hits,
        "trigram_hits": trigram_hits,
    }


# added: simple hill climbing to improve the greedy mapping by swapping letter assignments
def optimize_mapping(frequencies, bigrams, trigrams, iterations=5000):
    mapping = assign_homophones_to_letters(frequencies)
    score = score_mapping_with_ngrams(bigrams, trigrams, mapping)
    fitness = 0.4 * score["bigram_match_rate"] + 0.6 * score["trigram_match_rate"]
    best_mapping = dict(mapping)
    best_fitness = fitness

    symbols = list(mapping.keys())

    for _ in range(iterations):
        a, b = random.sample(symbols, 2)
        if mapping[a] == mapping[b]:
            continue

        mapping[a], mapping[b] = mapping[b], mapping[a]

        score = score_mapping_with_ngrams(bigrams, trigrams, mapping)
        new_fitness = 0.4 * score["bigram_match_rate"] + 0.6 * score["trigram_match_rate"]

        if new_fitness > fitness:
            fitness = new_fitness
            if fitness > best_fitness:
                best_fitness = fitness
                best_mapping = dict(mapping)
        else:
            mapping[a], mapping[b] = mapping[b], mapping[a]

    return best_mapping, score_mapping_with_ngrams(bigrams, trigrams, best_mapping)


# added: apply mapping to token list and return plaintext string
def translate_ciphertext(tokens, mapping):
    return "".join(mapping.get(token, token) for token in tokens)


def main():
    random.seed(42)
    tokens = read_ciphertext("ciphertext.txt")
    frequencies = count_homophones(tokens)
    bigrams = count_bigrams(tokens)
    trigrams = count_trigrams(tokens)

    plot_frequencies(frequencies, 20, "Homophones")
    plot_frequencies(bigrams, 15, "Bigrams")
    plot_frequencies(trigrams, 10, "Trigrams")

    best_mapping, best_score = optimize_mapping(frequencies, bigrams, trigrams, iterations = 20000)

    print("optimized mapping:")
    for sym, letter in sorted(best_mapping.items(), key=lambda x: -frequencies[x[0]]):
        print(f"  {sym} -> {letter}  (freq {frequencies[sym]})")

    print("\nfinal score:")
    print(best_score)

    plaintext = translate_ciphertext(tokens, best_mapping)
    with open("plaintext.txt", "w", encoding="utf-8") as f:
        f.write(plaintext)
    print("\nplaintext written to plaintext.txt")


if __name__ == "__main__":
    main()

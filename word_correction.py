import re
import string
from collections import Counter


def words(text):
    pattern = re.compile(r'\w+')
    return pattern.findall(text.lower())

WORDS = Counter(words(open('big.txt').read()))


def probability(word, N=sum(WORDS.values())):
    return float(WORDS[word]) / N


def edit1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edit2(word):
    return (e2 for e1 in edit1(word) for e2 in edit1(e1))


def known(words):
    return set(w for w in words if w in WORDS)


def candidates(word):
    return (known([word]) or known(edit1(word)) or known(edit2(word)) or [word])


def correction(word):
    return max(candidates(word), key=probability)


if __name__ == '__main__':
    print(correction('perpul'))

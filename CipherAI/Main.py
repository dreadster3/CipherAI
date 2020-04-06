import numpy as np
import random
import time

probabilities = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.2, 0.8,  4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1, 2.8, 1.0, 2.4, 0.2, 2.0, 0.1]
probabilities = np.divide(probabilities, 100)
alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_capital = alphabet.upper()

def encodeFile(input, output, shift):
    while True:
        line = input.readline()
        if len(line) == 0:
            break
        output.write(encodeLine(line, shift))
    input.seek(0)
    output.seek(0)


def encodeLine(line, shift):
    encoded_line = ""
    for char in line:
        if char in alphabet_capital:
            encoded_line += alphabet_capital[(alphabet_capital.find(char) + shift) % len(alphabet_capital)]
        elif char not in alphabet:
            encoded_line += char
        else:
            encoded_line += alphabet[(alphabet.find(char) + shift) % len(alphabet)]
    return encoded_line

def countCharacters(file):
    characters = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    while True:
        line = file.readline()
        for char in line.lower():
            if char in alphabet:
                characters[alphabet.find(char)] += 1
        if len(line) == 0:
            break
    file.seek(0)
    return characters

def chi_squared_value(frequencies):
    total_characters = np.sum(frequencies)
    sum = 0
    for i in range(26):
        sum += (((total_characters * probabilities[i]) - frequencies[i]) ** 2) / frequencies[i]
    return sum

def compare_frequencies_probabilities(frequencies):
    frequencies_letters = sorted(list(zip(frequencies, alphabet)))
    frequencies_letters.reverse()

    probabilities_zip = sorted(list(zip(probabilities, alphabet)))
    probabilities_zip.reverse()

    characters_map = []
    for i in range(len(alphabet)):
        characters_map.append((frequencies_letters[i][1], probabilities_zip[i][1]))
    return characters_map

def decode_line_with_map(line, map):
    used, newchar = zip(*map)
    used = list(used)
    newchar = list(newchar)
    decoded_line = ""
    for char in line:
        if char in alphabet:
            decoded_line += newchar[used.index(char, 0, len(used))]
        elif char in alphabet_capital:
            decoded_line += newchar[used.index(char.lower(), 0, len(used))].upper()
        else:
            decoded_line += char
    return decoded_line

def decode_with_map(input, output, map):
    while True:
        line = input.readline()
        if len(line) == 0:
            break
        output.write(decode_line_with_map(line, map))

    input.seek(0)
    output.seek(0)

#MAIN
book = open("data/book.txt", "r")
encoded_book_write = open("data/encoded_book.txt", "w")

encodeFile(book, encoded_book_write, 5)

encoded_book_read = open("data/encoded_book.txt", "r")

frequencies = countCharacters(encoded_book_read)
zipped = compare_frequencies_probabilities(frequencies)

test = open("test.txt", "w")
print(zipped)
decode_with_map(encoded_book_read, test, zipped)

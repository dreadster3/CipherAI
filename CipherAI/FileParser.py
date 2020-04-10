import numpy as np
import string
from Encoder import Encoder


class FileParser:
    def __init__(self, path):
        self.path = path
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.probabilities = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.2, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1,
                 2.8, 1.0, 2.4, 0.2, 2.0, 0.1]

    def encodefile(self, output_path, alphabet_map):
        encoder = Encoder(alphabet_map)
        input_file = open(self.path, "r")
        output_file = open(output_path, "w")
        while True:
            line = input_file.readline()
            if len(line) == 0:
                break
            output_file.write(encoder.encode_line(line))
        input_file.close()
        output_file.close()


    def map_alphabets(self, new_alphabet):
        probabilities_zip = sorted(list(zip(self.probabilities, self.alphabet)))
        probabilities_zip.reverse()
        probabilities_zip = np.array(probabilities_zip)
        probabilities_alphabet = probabilities_zip[:, 1]

        return np.array(list(zip(new_alphabet, probabilities_alphabet)))


    def get_first_n_words(self, number_of_words):
        input_file = open(self.path, "r")
        words = []
        frequencies = []

        while np.sum(frequencies) < number_of_words:
            line = input_file.readline()
            if len(line) == 0:
                break
            words_line = line.split(" ")
            for word in words_line:
                w = word.lower()
                w = w.rstrip()
                w = w.translate(str.maketrans('', '', string.punctuation))
                if len(w) == 0:
                    continue
                if w == "its":
                    if words.count("it") == 0:
                        words.append("it")
                        frequencies.append(1)
                    else:
                        frequencies[words.index("it")] += 1

                    if words.count("is") == 0:
                        words.append("is")
                        frequencies.append(1)
                    else:
                        frequencies[words.index("is")] += 1
                elif w == "im":
                    if words.count("i") == 0:
                        words.append("i")
                        frequencies.append(1)
                    else:
                        frequencies[words.index("i")] += 1
                elif words.count(w) == 0:
                    words.append(w)
                    frequencies.append(1)
                else:
                    frequencies[words.index(w)] += 1
        input_file.close()
        return words, frequencies

    def map_frequencies_probabilities(self, frequencies):
        frequencies_letters = sorted(list(zip(frequencies, self.alphabet)))
        frequencies_letters.reverse()

        probabilities_zip = sorted(list(zip(self.probabilities, self.alphabet)))
        probabilities_zip.reverse()

        characters_map = []
        for i in range(len(self.alphabet)):
            characters_map.append((frequencies_letters[i][1], probabilities_zip[i][1]))
        return characters_map

    def count_characters(self, words, frequencies):
        characters = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for word in words:
            for char in word.lower():
                if char in self.alphabet:
                    characters[self.alphabet.find(char)] += (1 * frequencies[words.index(word)])
        return characters

    def save_progress(self, population_size, number_of_generations, mutation_rate, current_generation, best_score, best_population):
        file = open(self.path, "w")
        file.write(str(number_of_generations) + "\n")
        file.write(str(current_generation) + "\n")
        file.write(str(population_size) + "\n")
        file.write(str(mutation_rate) + "\n")
        file.write(str(best_score) + "\n")
        file.write(str(best_population) + "\n")
        file.close()

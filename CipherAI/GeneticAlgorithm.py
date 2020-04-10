import random
import copy
import numpy as np
from Encoder import Encoder
from FileParser import FileParser


class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.most_used_words = ["the", "be", "to", "of", "and", "a", "in", "is", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "is",
                                "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "up", "get", "which", "make", "just", "next", "quite"]

    def create_starting_population(self, map_alphabet):
        population = []
        population.append(map_alphabet)
        for i in range(self.population_size - 1):
            population.append(self.mutate_map(map_alphabet))
        return np.array(population)

    def mutate_map(self, map_alphabet):
        point1 = random.randint(0, len(map_alphabet) - 1)
        point2 = random.randint(0, len(map_alphabet) - 1)

        return self.swap(map_alphabet, point1, point2)

    def swap(self, map_alphabet, i, j):
        result = copy.deepcopy(map_alphabet)

        aux = (result[i][0], result[j][1])
        result[i] = (result[j][0], result[i][1])
        result[j] = aux

        return result

    def random_mutation_gene(self, population):
        for individual in range(len(population)):
            for i in range(26):
                if random.choices(population=[True, False], weights=[self.mutation_rate, 1 - self.mutation_rate], k=1)[0]:
                    population[individual] = self.mutate_map(population[individual])

        return population

    def get_scores(self, words, frequencies_words, population):
        scores = []
        for individual in population:
            encoder = Encoder(individual)
            encoded_words = encoder.encode_list_words(words)
            scores.append(self.calculate_fitness(encoded_words, frequencies_words))
        return np.array(scores)

    def select_individual_by_tournament(self, population, scores):
        population_size = len(scores)

        fighter_1 = random.randint(0, population_size - 1)
        fighter_2 = random.randint(0, population_size - 1)

        fighter_1_score = scores[fighter_1]
        fighter_2_score = scores[fighter_2]

        if fighter_1_score >= fighter_2_score:
            winner = fighter_1
        else:
            winner = fighter_2

        return population[winner, :]

    def crossover_alphabets(self, alphabet_1, alphabet_2, crossover_point):
        new_alphabet_1 = []
        new_alphabet_2 = []

        alphabet_1 = list(alphabet_1)
        alphabet_2 = list(alphabet_2)

        for i in range(len(alphabet_1)):
            if i >= crossover_point:
                break
            new_alphabet_1.append(alphabet_1[i])

        for j in range(len(alphabet_2)):
            if j >= crossover_point:
                break
            new_alphabet_2.append(alphabet_2[j])

        for char in alphabet_1:
            if new_alphabet_2.count(char) == 0:
                new_alphabet_2.append(char)

        for char in alphabet_2:
            if new_alphabet_1.count(char) == 0:
                new_alphabet_1.append(char)

        return new_alphabet_1, new_alphabet_2

    def breed_crossover(self, parent_1, parent_2):
        parser = FileParser("")
        chromossome_length = len(parent_1)

        crossover_point = random.randint(1, chromossome_length - 2)

        alphabet_1, x = zip(*parent_1)
        alphabet_2, z = zip(*parent_2)

        new_alphabet_1, new_alphabet_2 = self.crossover_alphabets(alphabet_1, alphabet_2, crossover_point)

        return parser.map_alphabets(new_alphabet_1), parser.map_alphabets(new_alphabet_2)

    def calculate_fitness(self, words, frequencies_words):
        # TODO: Use expected number of each word

        frequencies = self.count_common_word(words, frequencies_words)
        mapped = sorted(list(zip(frequencies, self.most_used_words)))
        mapped.reverse()
        mapped = np.array(mapped)
        mapped = mapped[:, 1]

        score = []
        for i in range(len(self.most_used_words)):
            if frequencies[i] == 0:
                score.append(-100)
            elif self.most_used_words[i] == mapped[i]:
                score.append(1)
            else:
                score.append(0)

        return np.sum(score)

    def count_common_word(self, words, frequencies_words):
        frequencies = np.zeros(len(self.most_used_words), dtype=int)
        for word in words:
            for i in range(len(self.most_used_words)):
                if word == "its":
                    frequencies[self.most_used_words.index("it")] += (1 * frequencies_words[words.index("its")])
                    frequencies[self.most_used_words.index("is")] += (1 * frequencies_words[words.index("its")])
                elif word == "im":
                    frequencies[self.most_used_words.index("i")] += (1 * frequencies_words[words.index("im")])
                elif word == self.most_used_words[i]:
                    frequencies[i] += (1 * frequencies_words[words.index(word)])
        return frequencies

    def save_progress(self, path, generation, best_score, best_population):
        parser = FileParser(path)
        parser.save_progress(self.population_size, self.generations, self.mutation_rate, generation, best_score,
                             best_population)

    def run(self, parser):
        number_of_lines = 10000
        words, frequencies_words = parser.get_first_n_words(number_of_lines)
        print(words)
        print(frequencies_words)
        frequencies_characters = parser.count_characters(words, frequencies_words)
        map_alphabet = parser.map_frequencies_probabilities(frequencies_characters)

        population = self.create_starting_population(map_alphabet)

        scores = self.get_scores(words, frequencies_words, population)
        best_score = np.max(scores)
        best_score_progress = [best_score]
        best_population = population[np.argmax(scores)]

        for generation in range(self.generations):
            print(generation)
            new_population = []

            for i in range(int(self.population_size / 2)):
                parent_1 = self.select_individual_by_tournament(population, scores)
                parent_2 = self.select_individual_by_tournament(population, scores)
                child_1, child_2 = self.breed_crossover(parent_1, parent_2)

                new_population.append(child_1)
                new_population.append(child_2)

            population = np.array(new_population)
            population = self.random_mutation_gene(population)

            scores = self.get_scores(words, frequencies_words, population)
            best_score_population = np.max(scores)
            if best_score < best_score_population:
                best_score = best_score_population
                best_population = population[np.argmax(scores)]
                best_score_progress.append(best_score)
            self.save_progress("data/progress.txt", generation, best_score, best_population)
        print(best_score_progress)
        return best_score, best_population

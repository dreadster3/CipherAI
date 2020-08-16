import random
import copy
import numpy as np
from CipherAI.Encoder import Encoder
from CipherAI.FileParser import FileParser


# Auxiliary method to swap 2 letters in an alphabet_map
# @param map_alphabet that needs to be altered
# @param i index of element 1
# @param j index of element 2
# return alphabet_map after the swap
def swap(map_alphabet, i, j):
    result = copy.deepcopy(map_alphabet)

    aux = (result[i][0], result[j][1])
    result[i] = (result[j][0], result[i][1])
    result[j] = aux

    return result


# Method that mutates a map by swapping 2 letters at random
# @param map_alphabet to be mutated
# return mutated map
def mutate_map(map_alphabet):
    point1 = random.randint(0, len(map_alphabet) - 1)
    point2 = random.randint(0, len(map_alphabet) - 1)

    return swap(map_alphabet, point1, point2)


# Method to select two elements at random and then pick the best one
# @param population to pick the elements from
# @param array containing the scores of each element
# return the map of the element that is the best
def select_individual_by_tournament(population, scores):
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


# Method the crossover 2 alphabets in order to create a child alphabet
# @param alphabet_1
# @param alphabet_2
# @param crossover_point point at which the two alphabets start using the letters of the other alphabet
# return 2 alphabets that are similar to both alphabets
def crossover_alphabets(alphabet_1, alphabet_2, crossover_point):
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


# Method to create two children alphabets out of 2 parent alphabets
# @param parent_1 to be used to create the children
# @param parent_2 to be used to create the children
def breed_crossover(parent_1, parent_2):
    parser = FileParser("")
    chromosome_length = len(parent_1)

    crossover_point = random.randint(1, chromosome_length - 2)

    alphabet_1, x = zip(*parent_1)
    alphabet_2, z = zip(*parent_2)

    new_alphabet_1, new_alphabet_2 = crossover_alphabets(alphabet_1, alphabet_2, crossover_point)

    return parser.map_alphabets(new_alphabet_1), parser.map_alphabets(new_alphabet_2)


class GeneticAlgorithm:
    # Constructor
    # @param population_size of the genetic algorithm
    # @param number_of_generations of the genetic algorithm
    # @param mutation_rate probability of mutation for genetic algorithm
    def __init__(self, population_size, generations, mutation_rate):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.most_used_words = ["the", "be", "to", "of", "and", "a", "in", "is", "that", "have", "i", "it",
                                "for", "not", "on", "with", "he", "as", "you", "do", "is",
                                "at", "this", "but", "his", "by", "from", "they", "we", "say",
                                "her", "she", "or", "an", "will", "up", "get", "which", "make", "just", "next", "quite"]

    # Method to create the starting population
    # @param map_alphabet starting alphabet map to be mutated
    # return array containing the full starting population
    def create_starting_population(self, map_alphabet):
        population = [map_alphabet]
        for i in range(self.population_size - 1):
            population.append(mutate_map(map_alphabet))
        return np.array(population)

    # Method to mutate the population
    # @param population to be mutated
    # return population after mutation
    def random_mutation_gene(self, population):
        for individual in range(len(population)):
            for i in range(26):
                if random.choices(population=[True, False],
                                  weights=[self.mutation_rate, 1 - self.mutation_rate], k=1)[0]:
                    population[individual] = mutate_map(population[individual])

        return population

    # Calculate the scores for the current population
    # @param words to be used for calculation
    # @param frequencies_words frequency of each word
    # @param population to be analyzed
    # return array with containing the score for each element of the population
    def get_scores(self, words, frequencies_words, population):
        scores = []
        for individual in population:
            encoder = Encoder(individual)
            encoded_words = encoder.encode_list_words(words)
            scores.append(self.calculate_fitness(encoded_words, frequencies_words))
        return np.array(scores)

    # Calculate the fitness for a given encoding
    # @param words encoded words to be assessed
    # @param frequencies_words how many times each word appears
    def calculate_fitness(self, words, frequencies_words):
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

    # Method to count occurrences of the most common words of the english alphabet
    # @param words words to be checked
    # @param frequencies_words how many times each words appears
    # return array containing how many times each most common word appears
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

    # Save the progress of the genetic algorithm onto a file
    # @param path of file to save the progress
    # @param current_generation being iterated in the genetic algorithm
    # @param best_score achieved so far
    # @param best_population population that generated the best_score
    def save_progress(self, path, generation, best_score, best_population):
        parser = FileParser(path)
        parser.save_progress(self.population_size, self.generations, self.mutation_rate, generation, best_score,
                             best_population)

    # Main method of the genetic algorithm
    # @param parser of the file that needs to be decoded
    # return the best_score and the alphabet that achieved the best score
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
                parent_1 = select_individual_by_tournament(population, scores)
                parent_2 = select_individual_by_tournament(population, scores)
                child_1, child_2 = breed_crossover(parent_1, parent_2)

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

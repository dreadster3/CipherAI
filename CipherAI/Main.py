import numpy as np
import random
import time
import copy

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

def map_frequencies_probabilities(frequencies):
    frequencies_letters = sorted(list(zip(frequencies, alphabet)))
    frequencies_letters.reverse()

    probabilities_zip = sorted(list(zip(probabilities, alphabet)))
    probabilities_zip.reverse()

    characters_map = []
    for i in range(len(alphabet)):
        characters_map.append((frequencies_letters[i][1], probabilities_zip[i][1]))
    return characters_map

def map_alphabets(new_alphabet):
    probabilities_zip = sorted(list(zip(probabilities, alphabet)))
    probabilities_zip.reverse()
    probabilities_zip = np.array(probabilities_zip)
    probabilities_alphabet = probabilities_zip[:, 1]

    return np.array(list(zip(new_alphabet, probabilities_alphabet)))

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

def mutate_map(map_alphabet):
    point1 = random.randint(0, len(map_alphabet) - 1)
    point2 = random.randint(0, len(map_alphabet) - 1)

    return swap(map_alphabet, point1, point2)

def swap(map_alphabet, i, j):
    result = copy.deepcopy(map_alphabet)

    aux = (result[i][0], result[j][1])
    result[i] = (result[j][0], result[i][1])
    result[j] = aux

    return result

def create_starting_population(individuals, map_alphabet):
    population = []
    population.append(map_alphabet)
    for i in range(individuals - 1):
        population.append(mutate_map(map_alphabet))
    return np.array(population)

def get_scores(input, population):
    output = open("data/output_ga.txt", "w")
    scores = []
    for individual in population:
        decode_with_map(input, output, individual)
        output_read = open(output.name, "r")
        scores.append(calculate_fitness(output_read))
    return np.array(scores)


def calculate_fitness(file):
    #TODO: Work on the fitness function, needs to reflect how close it is to english
    frequencies = countCharacters(file)
    return chi_squared_value(frequencies)

def select_individual_by_tournament(population, scores):
    population_size = len(scores)

    fighter_1 = random.randint(0, population_size - 1)
    fighter_2 = random.randint(0, population_size - 1)

    fighter_1_score = scores[fighter_1]
    fighter_2_score = scores[fighter_2]

    if fighter_1_score <= fighter_2_score:
        winner = fighter_1
    else:
        winner = fighter_2

    return population[winner, :]

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

def random_mutation_gene(population, probability):
    for individual in range(len(population)):
        if random.choices(population=[True, False], weights=[probability, 1 - probability], k=1)[0]:
            population[individual] = mutate_map(population[individual])

    return population

def breed_crossover(parent_1, parent_2):
    chromossome_length = len(parent_1)

    crossover_point = random.randint(1, chromossome_length - 2)

    alphabet_1, x = zip(*parent_1)
    alphabet_2, z = zip(*parent_2)

    new_alphabet_1, new_alphabet_2 = crossover_alphabets(alphabet_1, alphabet_2, crossover_point)

    return map_alphabets(new_alphabet_1), map_alphabets(new_alphabet_2)




#MAIN
book = open("data/book.txt", "r")
encoded_book_write = open("data/encoded_book.txt", "w")


encodeFile(book, encoded_book_write, 5)

encoded_book_read = open("data/encoded_book.txt", "r")

generations = 10
population_size = 50
mutation_rate = 0.05

frequencies = countCharacters(encoded_book_read)
map_alphabet = map_frequencies_probabilities(frequencies)

population = create_starting_population(population_size, map_alphabet)

scores = get_scores(encoded_book_read, population)
best_score = np.min(scores)
best_score_progress = [best_score]

for generation in range(generations):
    new_population = []

    for i in range(int(population_size / 2)):
        parent_1 = select_individual_by_tournament(population, scores)
        parent_2 = select_individual_by_tournament(population, scores)
        child_1, child_2 = breed_crossover(parent_1, parent_2)

        new_population.append(child_1)
        new_population.append(child_2)

    population = np.array(new_population)
    population = random_mutation_gene(population, mutation_rate)

    scores = get_scores(encoded_book_read, population)
    best_score = min(best_score, np.min(scores))
    best_score_progress.append(best_score)

import numpy as np
import random
import time
import copy
import string

probabilities = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.2, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1,
                 2.8, 1.0, 2.4, 0.2, 2.0, 0.1]
probabilities = np.divide(probabilities, 100)
alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_capital = alphabet.upper()

most_used_words = ["the", "of", "and", "to", "a", "in", "is", "i", "that", "it", "for", "you", "was", "with", "on",
                   "as", "have", "but", "be", "they"]


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
    characters = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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


def count_common_word(file):
    frequencies = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while True:
        line = file.readline()
        words = line.split(" ")
        for word in words:
            w = word.lower()
            w = w.rstrip()
            w = w.translate(str.maketrans('', '', string.punctuation))
            if len(w) == 0:
                continue
            for i in range(len(most_used_words)):
                if w == "its":
                    frequencies[most_used_words.index("it")] += 1
                    frequencies[most_used_words.index("is")] += 1
                elif w == "im":
                    frequencies[most_used_words.index("i")] += 1
                elif w == most_used_words[i]:
                    frequencies[i] += 1

        if len(line) == 0:
            break
    file.seek(0)
    return frequencies


def calculate_fitness(file):
    # TODO: Use expected number of each word
    # frequencies = countCharacters(file)
    # chi_squared = chi_squared_value(frequencies)
    # total_characters = np.sum(frequencies)

    frequencies = count_common_word(file)
    mapped = sorted(list(zip(frequencies, most_used_words)))
    mapped.reverse()
    mapped = np.array(mapped)
    mapped = mapped[:, 1]

    # expected = []
    # for i in range(len(frequencies)):
    #     expected.append(frequencies[0]/(i+1))
    #
    # print(expected)
    # print(frequencies)
    score = []
    for i in range(len(most_used_words)):
        if frequencies[i] == 0:
            score.append(-100)
        elif most_used_words[i] == mapped[i]:
            score.append(1)
        else:
            score.append(0)

    # print(chi_squared, total_characters)

    return np.sum(score)


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

def save_progress(file, population, number_of_generations, mutation_rate, current_generation):
    file.write(str(number_of_generations) + "\n")
    file.write(str(current_generation) + "\n")
    file.write(str(len(population)) + "\n")
    file.write(str(mutation_rate) + "\n")
    file.write(str(population) + "\n")
    file.seek(0)



# MAIN
book = open("data/book.txt", "r")
progress = open("data/progress", "w")
# encoded_book_write = open("data/encoded_book.txt", "w")

print(calculate_fitness(book))

# encodeFile(book, encoded_book_write, 5)

encoded_book_read = open("data/encoded_book.txt", "r")

generations = 200
population_size = 500
mutation_rate = 0.10

frequencies = countCharacters(encoded_book_read)
map_alphabet = map_frequencies_probabilities(frequencies)

population = create_starting_population(population_size, map_alphabet)

scores = get_scores(encoded_book_read, population)
best_score = np.max(scores)
best_score_progress = [best_score]
best_population = population[np.argmax(scores)]

for generation in range(generations):
    print(generation)
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
    best_score_population = np.max(scores)
    if best_score < best_score_population:
        best_score = best_score_population
        best_population = population[np.argmax(scores)]
        best_score_progress.append(best_score)
    save_progress(progress, population, generations, mutation_rate, generation)

print(best_population)
print(scores)
print(best_score)
print(best_score_progress)

solution = open("data/solution.txt", "w")

decode_with_map(encoded_book_read, solution, best_population)

solution_read = open("data/solution.txt", "r")

print(count_common_word(solution_read))

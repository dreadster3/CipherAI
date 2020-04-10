from FileParser import FileParser
from GeneticAlgorithm import GeneticAlgorithm
import time

if __name__ == "__main__":
    start = time.time()
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_alphabet = "qwertyuiopasdfghjklzxcvbnm"
    encode = FileParser("data/book.txt")
    encode.encodefile("data/encoded_book.txt", list(zip(alphabet, new_alphabet)))

    solution = FileParser("data/encoded_book.txt")

    ga = GeneticAlgorithm(500, 200, 0.01)

    best_score, best_population = ga.run(solution)

    solution.encodefile("data/solution_new.txt", best_population)

    print(best_population)
    print(best_score)
    print(time.time() - start)
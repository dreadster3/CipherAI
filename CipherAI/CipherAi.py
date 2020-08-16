from CipherAI.FileParser import FileParser
from CipherAI.GeneticAlgorithm import GeneticAlgorithm

if __name__ == "__main__":
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_alphabet = "qwertyuiopasdfghjklzxcvbnm"
    encode = FileParser("data/book.txt")
    encode.encode_file("data/encoded_book.txt", list(zip(alphabet, new_alphabet)))

    solution = FileParser("data/encoded_book.txt")

    ga = GeneticAlgorithm(500, 200, 0.01)

    best_score, best_population = ga.run(solution)

    solution.encode_file("data/solution_new.txt", best_population)

class Encoder:
    def __init__(self, alphabet_map):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.alphabet_map = alphabet_map

    def encode_line(self, line):
        used_alphabet, new_alphabet = zip(*self.alphabet_map)
        used_alphabet = list(used_alphabet)
        new_alphabet = list(new_alphabet)
        newline = ""
        for char in line:
            if char in self.alphabet:
                newline += new_alphabet[used_alphabet.index(char)]
            elif char in self.alphabet.upper():
                newline += new_alphabet[used_alphabet.index(char.lower())].upper()
            else:
                newline += char
        return newline

    def encode_list_words(self, words):
        encoded = []
        for word in words:
            encoded.append(self.encode_line(word))
        return encoded

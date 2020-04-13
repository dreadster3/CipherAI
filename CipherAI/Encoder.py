#Class to encode and decode files
class Encoder:
    #Constructor
    #@param alphabet_map a map that maps the used alphabet to the new alphabet to encode the file
    def __init__(self, alphabet_map):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.alphabet_map = alphabet_map

    #Method to encode a single string.
    #@param line string to be encoded.
    #return the encoded string
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

    #Encode a list of words
    #@param words to be decoded
    #return a list with each word encoded
    def encode_list_words(self, words):
        encoded = []
        for word in words:
            encoded.append(self.encode_line(word))
        return encoded

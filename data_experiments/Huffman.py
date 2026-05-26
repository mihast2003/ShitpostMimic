from collections import Counter
import heapq


russian_freq = {
    ' ': 175,

    'о': 109,
    'е': 84,
    'а': 80,
    'и': 73,
    'н': 67,
    'т': 63,
    'с': 54,
    'р': 47,
    'в': 45,
    'л': 44,
    'к': 35,
    'м': 32,
    'д': 30,
    'п': 28,
    'у': 26,
    'я': 20,
    'ы': 19,
    'ь': 18,
    'г': 17,
    'з': 16,
    'б': 15,
    'ч': 14,
    'й': 12,
    'х': 10,
    'ж': 9,
    'ш': 8,
    'ю': 7,
    'ц': 6,
    'щ': 4,
    'э': 3,
    'ф': 3,
    'ъ': 1,
    'ё': 2,

    '.': 15,
    ',': 14,
    '!': 3,
    '?': 3,
    ':': 4,
    ';': 2,
    '-': 6,
    '—': 3,
    '(': 2,
    ')': 2,
    '"': 3,
    '\'': 2,

    '\n': 1,

    '0': 1,
    '1': 1,
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    '6': 1,
    '7': 1,
    '8': 1,
    '9': 1
}

english_freq = {
    ' ': 130,

    'e': 127,
    't': 91,
    'a': 82,
    'o': 75,
    'i': 70,
    'n': 67,
    's': 63,
    'h': 61,
    'r': 60,
    'd': 43,
    'l': 40,
    'c': 28,
    'u': 28,
    'm': 24,
    'w': 24,
    'f': 22,
    'g': 20,
    'y': 20,
    'p': 19,
    'b': 15,
    'v': 10,
    'k': 8,
    'x': 2,
    'j': 2,
    'q': 1,
    'z': 1,

    '.': 12,
    ',': 11,
    '!': 2,
    '?': 2,
    ':': 3,
    ';': 2,
    '-': 4,
    '\'': 3,
    '"': 2,

    '\n': 1,

    '0': 1,
    '1': 1,
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    '6': 1,
    '7': 1,
    '8': 1,
    '9': 1,
}


class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Required for heapq
    def __lt__(self, other):
        return self.freq < other.freq


class Huffman:
    def __init__(self, mode: str, DEBUG=True):
        self.codes = {}
        self.reverse_codes = {}
        self.debug = DEBUG

        frequencies = russian_freq if mode == "rus" else english_freq
        self.root = self._build_tree(frequencies)

        self._generate_codes(self.root)

        # print("Codes:", self.codes)

    def _build_tree(self, frequencies):
        freq = frequencies

        heap = []

        # Create leaf nodes
        for char, frequency in freq.items():
            heapq.heappush(heap, Node(char, frequency))

        # Merge nodes until one tree remains
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = Node(freq=left.freq + right.freq)
            merged.left = left
            merged.right = right

            heapq.heappush(heap, merged)

        return heap[0]

    def _generate_codes(self, node, current_code=""):
        if node is None:
            return

        # Leaf node
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char
            return

        self._generate_codes(node.left, current_code + "0")
        self._generate_codes(node.right, current_code + "1")

    def encode(self, text):
        encoded = ''.join(self.codes[char] for char in text.lower()) 

        if self.debug:
            print("\nEncoded length:", len(encoded))
            encoded_with_spaces = ' '.join(self.codes[char] for char in text.lower()) 
            print(encoded_with_spaces)
            print(f"Bits per symbol: {len(encoded.replace(' ', ''))/len(text)} \nSize reduced to: {(len(encoded.replace(' ', ''))/len(text))/8*100} %\n")

        return encoded

    def decode(self, encoded_text):
        current_code = ""

        decoded = ""

        for bit in encoded_text:
            current_code += bit

            if current_code in self.reverse_codes:
                decoded += self.reverse_codes[current_code]
                current_code = ""

        if self.debug:
            print("\nDecoded:", decoded)

        return decoded


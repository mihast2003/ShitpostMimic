from Huffman import Huffman

huffman = Huffman(mode="rus", DEBUG=True)

input_text = "это очень секретное собщение: ты лох"

encoded = huffman.encode(input_text)

decoded = huffman.decode(encoded)
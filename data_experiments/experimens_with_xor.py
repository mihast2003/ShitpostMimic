from Huffman import Huffman
from run_length_encoder import Laugh_Encoder_RunLength

huffman = Huffman(mode="rus", DEBUG=True)
laugh_encoder = Laugh_Encoder_RunLength(DEBUG=True)

input_text = "могу попробовать более длинный текст, что скажешь uwu так нечестно наверное но я не знаю как иначе"
# input_text = input_text * 10

encoded = huffman.encode(input_text)
laugh_coded = laugh_encoder.encode(encoded)
print(laugh_coded)

laugh_decoded = laugh_encoder.decode(laugh_coded)
decoded = huffman.decode(laugh_decoded)
print(decoded)

# laugh_decoded = laugh_encoder.decode(laugh_coded)
# decoded = huffman.decode(laugh_decoded)
# print(decoded)

# for shift in [0, 1, 2, 4, 6, 8, 16]:

#     encoded = huffman.encode(input_text)
#     laugh_coded = laugh_encoder.encode(encoded, shift)
#     print(laugh_coded)

#     laugh_decoded = laugh_encoder.decode(laugh_coded, shift)
#     decoded = huffman.decode(laugh_decoded)
#     print(decoded)

#     print()
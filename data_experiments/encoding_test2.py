from Huffman import Huffman

huffman = Huffman(mode="rus", DEBUG=True)


bit_to_char = {
    "00": "В",
    "11": "А",
    "01": "П",
    "10": "Х",

    # "000": "В",
    # "001": "Д",
    # "010": "Р",
    # "011": "Э",

    # "100": "Ъ",
    # "101": "У",
    # "110": "Е",
    # "111": "И",
}

char_to_bit = {}
for key in bit_to_char:
        value = bit_to_char[key]
        char_to_bit[value] = key

repeat_rate = {
    "К": 3,
    "Ж": 4,
}

chunk = 3

def encode(bits: str, bit_to_char: dict = bit_to_char) -> str:
    out = []
    i = 0

    while i < len(bits):
        # try longest first
        if i + chunk <= len(bits) and bits[i:i+chunk] in bit_to_char:
            out.append(bit_to_char[bits[i:i+chunk]])
            i += chunk

        # fallback to 2-bit
        elif i < len(bits):

            # print(bits[i:])

            if i+2 >= len(bits):
                pad = (len(bits) - i) % 2
                bits += "0" * pad

            # print(bits[i:i+2])

            out.append(bit_to_char[bits[i:i+2]])
            i += 2

        else:
            rest = bits[i:]
            raise ValueError(f"No match at position {i}")

    return "".join(out)

def encode_with_repeat_rate(text: str, repeat_rate: dict = repeat_rate):
    if not text:
        return ""

    out = []
    i = 0

    while i < len(text):
        j = i

        # count run length
        while j < len(text) and text[j] == text[i]:
            j += 1

        run_length = j - i
        symbol = text[i]

        # find best repeat token
        token = None
        for k, v in repeat_rate.items():
            if v == run_length:
                token = k
                break

        if token:
            out.append(symbol + token)
        else:
            # fallback: literal repetition
            out.append(symbol * run_length)

        i = j

    return "".join(out)

def decode(text: str) -> str:
    return "".join(char_to_bit[c] for c in text)

def decode_with_repeat_rate(text: str, repeat_rate: dict = repeat_rate):
    out = []
    i = 0

    # invert dictionary: token → repeat length
    token_to_len = {k: v for k, v in repeat_rate.items()}

    while i < len(text):
        c = text[i]

        # check if next char is a repeat token
        if i + 1 < len(text) and text[i + 1] in token_to_len:
            repeat_count = token_to_len[text[i + 1]]
            out.append(c * repeat_count)
            i += 2
        else:
            out.append(c)
            i += 1

    return "".join(out)


input_text = "кто же выиграет мне даже интересно потому что это такое дело непонтяное же"

#--- ENCODING ----
encoded = huffman.encode(input_text)
# print(encoded)

laugh_coded = encode(encoded)
print(f"Laugh coded length: {len(laugh_coded)} (Bits per symbol: {len(encoded)/len(laugh_coded)})\n{laugh_coded}")

laugh_comp = encode_with_repeat_rate(laugh_coded)
print(f"Laugh comp length: {len(laugh_comp)} (Bits per symbol: {len(encoded)/len(laugh_comp)})\n {laugh_comp}")

#--- DECODING---
laugh_decomp = decode_with_repeat_rate(laugh_comp)
laugh_decoded = decode(laugh_coded)

decoded = huffman.decode(laugh_decoded)
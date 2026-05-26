from Huffman import Huffman

huffman = Huffman(mode="rus", DEBUG=True)


triples_to_bits = {
    "АХХ": "111111",
    "АХП": "011111",
    "АХА": "010111",
    "АХК": "100111",
    "АХВ": "111101",
    "АХЖ": "011101",
    "АХР": "010101",
    "АХУ": "100101",

    "АПХ": "111011",
    "АПЗ": "011011",
    "АПЖ": "010011",
    "АПД": "100011",
    "АПА": "111001",
    "АПР": "011001",
    "АПК": "010001",
    "АПВ": "100001",

    "ХАХ": "101111",
    "ХАП": "110111",
    "ХАА": "001111",
    "ХАК": "000111",
    "ХАВ": "101101",
    "ХАЖ": "110101",
    "ХАД": "001101",
    "ХАЗ": "000101",

    "ХПА": "101011",
    "ХПЖ": "110011",
    "ХПЗ": "001011",
    "ХПЪ": "000011",
    "ХПЭ": "101001",
    "ХПК": "110001",
    "ХПП": "001001",
    "ХПВ": "000001",
# second half
    "ПХА": "111110",
    "ПХЗ": "011110",
    "ПХЪ": "010110",
    "ПХК": "100110",
    "ПХВ": "111100",
    "ПХИ": "011100",
    "ПХУ": "010100",
    "ПХР": "100100",

    "ВХР": "101110",
    "ВХП": "110110",
    "ВХВ": "001110",
    "ВХМ": "000110",
    "ВХК": "101100",
    "ВХУ": "110100",
    "ВХЕ": "001100",
    "ВХИ": "000100",

    "КХП": "111010",
    "КХА": "011010",
    "КХВ": "010010",
    "КХР": "100010",
    "КХУ": "111000",
    "КХК": "011000",
    "КХЕ": "010000",
    "КХИ": "100000",

    "ХКЗ": "101010",
    "ХКЖ": "110010",
    "ХКД": "001010",
    "ХКЪ": "000010",
    "ХКЭ": "101000",
    "ХКЕ": "110000",
    "ХКП": "001000",
    "ХКА": "000000",
}

letter_chunk = 3
binary_chunk = 6

repeat_rate = {
    "С": 3,
    " ": 4,
}


def encode(bits: str, pair_to_bits: dict = triples_to_bits) -> str:
    # invert mapping
    bits_to_pair = {v: k for k, v in pair_to_bits.items()}

    i = 0
    out = []

    while i < len(bits):
        # try match fixed chunk lengths (assuming all same length)
        matched = False

        if i+binary_chunk > len(bits):
            pad = binary_chunk - (len(bits) - i)
            bits += "0" * pad

        for bit, pair in bits_to_pair.items():
            if bits.startswith(bit, i):
                out.append(pair)
                i += len(bit)
                matched = True
                break

        if not matched:
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

def decode(text: str, pair_to_bits: dict = triples_to_bits) -> str:
    return "".join(pair_to_bits[text[i:i+letter_chunk]] for i in range(0, len(text), letter_chunk))

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
print(f"Length: {len(laugh_coded)}\n{laugh_coded}")

laugh_comp = encode_with_repeat_rate(laugh_coded)
print(f"Laugh comp length: {len(laugh_comp)} (Bits per symbol: {len(encoded)/len(laugh_comp)})\n {laugh_comp}")

#--- DECODING---
laugh_decomp = decode_with_repeat_rate(laugh_comp)
laugh_decoded = decode(laugh_coded)

decoded = huffman.decode(laugh_decoded)
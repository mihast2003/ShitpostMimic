from Huffman import Huffman

huffman = Huffman(mode="rus", DEBUG=True)


bit_to_char = {
    "00": "Х",
    "11": "П",
    "01": "К",
    "10": "А",

    "11111": "У",
    "11110": "Д",
    "01111": "Ж",
    "11100": "Э",

    "10101": "З",
    "01010": "В",
    "10111": "Р",
    "11101": "Е",

    # "00110": "У",
    # "00111": "Д",
    # "00011": "Ж",
    # "00011": "Э",

    # "11000": "З",
    # "11101": "В",
    # "00100": "Р",
    # "01001": "Е",
}

char_to_bit = {}
for key in bit_to_char:
        value = bit_to_char[key]
        char_to_bit[value] = key

repeat_rate = {
    # "И": (1, 2),
    "Ы": (2, 1),
    # "С": (2, 2),
}

chunk = 5

def encode(bits: str, bit_to_char: dict = bit_to_char) -> str:
    out = []
    i = 0

    while i < len(bits):
        # try longest first
        if i + chunk <= len(bits) and bits[i:i+chunk] in bit_to_char:
            out.append(bit_to_char[bits[i:i+chunk]])
            i += chunk

        # fallback to 2-bit
        elif i <= len(bits):
            if i+2 > len(bits):
                pad = (len(bits) - i) % 2
                bits += "0" * pad

            # print(bits[i:i+2])

            out.append(bit_to_char[bits[i:i+2]])
            i += 2

        else:
            raise ValueError(f"No match at position {i}")

    return "".join(out)

def encode_with_repeat_rate(text: str, repeat_rate: dict = repeat_rate):
    out = []
    i = 0

    # sort tokens by strongest compression first
    rules = sorted(
        repeat_rate.items(),
        key=lambda x: x[1][0] * x[1][1],
        reverse=True
    )

    while i < len(text):
        matched = False

        for token, (take, repeat) in rules:
            total_len = take * (repeat + 1)

            if i + total_len > len(text):
                continue

            chunk = text[i:i+take]

            expected = chunk * (repeat + 1)

            if text[i:i+total_len] == expected:
                out.append(chunk)
                out.append(token)

                i += total_len
                matched = True
                break

        if not matched:
            out.append(text[i])
            i += 1

    return "".join(out)

def decode(text: str) -> str:
    return "".join(char_to_bit[c] for c in text)

def decode_with_repeat_rate(text: str, repeat_rate: dict = repeat_rate):
    out = []

    for c in text:
        # repeat token
        if c in repeat_rate:
            take, repeat = repeat_rate[c]

            if len(out) < take:
                raise ValueError(f"Not enough previous characters for {c}")

            chunk = out[-take:]

            for _ in range(repeat):
                out.extend(chunk)

        # normal character
        else:
            out.append(c)

    return "".join(out)


input_text = "кто же выиграет мне даже интересно потому что это такое дело непонтяное же"

#--- ENCODING ----
encoded = huffman.encode(input_text)
# print(encoded)

laugh_coded = encode(encoded)
print(laugh_coded)

laugh_comp = encode_with_repeat_rate(laugh_coded)
print(f"Laugh comp length: {len(laugh_comp)} (Bits per symbol: {len(encoded)/len(laugh_comp)})\n {laugh_comp}")

#--- DECODING---
laugh_decomp = decode_with_repeat_rate(laugh_comp)
laugh_decoded = decode(laugh_coded)

decoded = huffman.decode(laugh_decoded)
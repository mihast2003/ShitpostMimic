from Huffman import Huffman

huffman = Huffman(mode="rus", DEBUG=True)


bit_to_char = {
    "00": "З",
    "11": "П",
    "01": "А",
    "10": "К",

    "11111": "В",
    "11110": "Д",
    "01111": "Ж",
    "11001": "Э",

    "00111": "Ъ",
    "11000": "У",
    "00011": "Е",
    "00000": "И",
}

char_to_bit = {}
for key in bit_to_char:
        value = bit_to_char[key]
        char_to_bit[value] = key

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
        elif i <= len(bits) and bits[i:i+2] in bit_to_char:
            if i+2 > len(bits):
                pad = (len(bits) - i) % 2
                bits += "0" * pad

            # print(bits[i:i+2])

            out.append(bit_to_char[bits[i:i+2]])
            i += 2

        else:
            raise ValueError(f"No match at position {i}")

    return "".join(out)

def encode_with_repeat(text: str) -> str:
    if not text:
        return ""

    out = []
    prev = text[0]
    count = 1

    for c in text[1:]:
        if c == prev:
            count += 1
        else:
            out.append(prev + "Х" * (count - 1))
            prev = c
            count = 1

    # flush last run
    out.append(prev + "Х" * (count - 1))

    return "".join(out)

def decode(text: str) -> str:
    return "".join(char_to_bit[c] for c in text)

def decode_with_repeat(text: str) -> str:
    out = []
    prev = None

    for c in text:
        if c == "Х":
            if prev is None:
                raise ValueError("Х cannot appear first")

            out.append(prev)
        else:
            out.append(c)
            prev = c

    return "".join(out)


input_text = "это очень секретное сообщение: ты лох"

#--- ENCODING ----
encoded = huffman.encode(input_text)
# print(encoded)

laugh_coded = encode(encoded)
print(laugh_coded)

laugh_comp = encode_with_repeat(laugh_coded)
print(f"Laugh comp length: {len(laugh_comp)} \n {laugh_comp}")

#--- DECODING---
laugh_decomp = decode_with_repeat(laugh_comp)
laugh_decoded = decode(laugh_coded)

decoded = huffman.decode(laugh_decoded)
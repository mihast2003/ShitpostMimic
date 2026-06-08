from XOR_shift import XOR_Shifter

xor_shifter = XOR_Shifter(DEBUG=False)

shift_indicators = {
    0: "АА",
    1: "АХ",
    2: "ХА",
    3: "ПХ",
    4: "ХП",
    5: "ПА",
    6: "АП",
    7: "ВХ",
    8: "ХВ",
}

reverse_shift_indicators = {}
for key in shift_indicators:
        value = shift_indicators[key]
        reverse_shift_indicators[value] = key

num_to_char = {
        1: "П",
        2: "А",
        3: "Х",
        4: "В",
        5: "К",
    }

char_to_num = {}
for key in num_to_char:
        value = num_to_char[key]
        char_to_num[value] = key

repeat_rate = {
    "Ж": (1, 2),
    "Д": (1, 3),
    "С": (2, 1),
    " ": (3, 1),
}

def encode_laugh(binary: str) -> str:
    if not binary:
        return ""

    result = []

    # start symbol
    if binary[0] == "1":
        result.append("АХ@")
    else:
        result.append("ХА@")

    # split into runs
    runs = []

    current = binary[0]
    count = 1

    for bit in binary[1:]:
        if bit == current:
            count += 1
        else:
            runs.append(count)
            current = bit
            count = 1

    runs.append(count)

    # encode one number recursively
    def encode_number(n: int) -> str:

        # direct encoding
        if n in num_to_char:
            return num_to_char[n]

        # even => reverse *2
        if n % 2 == 0:
            return encode_number(n // 2) + "У"

        # odd => reverse *2+1
        return encode_number((n - 1) // 2) + "З"

    # encode runs
    for run in runs:
        result.append(encode_number(run))

    return "".join(result)

def decode_laugh(encoded: str) -> str:
    if not encoded:
        return ""

    # start mode
    if encoded[0:2] == "АХ":
        current_bit = "1"
    elif encoded[0:2] == "ХА":
        current_bit = "0"
    else:
        raise ValueError("Must start with АХ or ХА")

    pos = 4

    result = []

    while pos < len(encoded):

        if encoded[pos] not in char_to_num:
            raise ValueError(f"Expected base symbol at {pos}")

        value = char_to_num[encoded[pos]]
        pos += 1

        # apply operators
        while pos < len(encoded) and encoded[pos] in ("У", "З"):

            if encoded[pos] == "У":
                value = value * 2

            elif encoded[pos] == "З":
                value = value * 2 + 1

            pos += 1

        result.append(current_bit * value)

        # alternate bit mode
        current_bit = "0" if current_bit == "1" else "1"

    return "".join(result)


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


class Laugh_Encoder_RunLength():
    def __init__(self, DEBUG) -> None:
        self.debug = DEBUG

    def find_best_shift(self, input_binary: str) -> int:
        best_shift = 0
        base_score =  len(self.simple_encode(input_binary, 0))   # finding the length of regular text w/o shifting
        best_score = base_score

        for shift in shift_indicators.keys():
            encoded = self.simple_encode(input_binary, shift)

            score = len(encoded)

            if score < best_score:
                best_score = score
                best_shift = shift

        print(f"Found best shift of {best_shift}, which reduced length by {(base_score-best_score)/base_score*100} %")
        return best_shift
    

    def simple_encode(self, input_binary: str, shift: int) -> str:
        transformed = xor_shifter.xor_shift_encode(input_binary, shift)
        laugh_coded = encode_laugh(transformed)
        laugh_optimised = laugh_coded.replace("ПППП","Э").replace("ППП","Ъ").replace("ПП","Е")
        laugh_comp = encode_with_repeat_rate(laugh_optimised)
        laugh_output = laugh_comp

        return laugh_output


    def encode(self, input_binary: str) -> str:
        """
        Encodes given binary string into a laugh string
        
        :return: laugh output
        """

        shift = self.find_best_shift(input_binary)

        transformed = xor_shifter.xor_shift_encode(input_binary, shift)
        if self.debug:
            print(f"shift={shift}")

        laugh_coded = encode_laugh(transformed)
        if self.debug:
            print(f"Laugh coded length: {len(laugh_coded)} (Bits per symbol: {len(input_binary)/len(laugh_coded)})\n{laugh_coded}")

        laugh_optimised = laugh_coded.replace("ПППП","Э").replace("ППП","Ъ").replace("ПП","Е")
        if self.debug:
            print(f"Laugh optimised length: {len(laugh_optimised)} (Bits per symbol: {len(input_binary)/len(laugh_optimised)})\n{laugh_optimised}")

        laugh_comp = encode_with_repeat_rate(laugh_optimised)
        if self.debug:
            print(f"Laugh comp length: {len(laugh_comp)} (Bits per symbol: {len(input_binary)/len(laugh_comp)})\n {laugh_comp}")

        laugh_output = laugh_comp

        laugh_output = laugh_output.replace("@", shift_indicators[shift])

        return laugh_output


    def decode(self, laugh: str) -> str:
        """
        Decodes given laugh string into a binary string
        
        :return: binary output
        """
        shift = reverse_shift_indicators[laugh[2:4]]
        print("I GOT IT YOU MEAN SHIFT IS ", shift)

        laugh_decomp = decode_with_repeat_rate(laugh)
        laugh_deoptimised = laugh_decomp.replace("Е","ПП").replace("Ъ","ППП").replace("Э","ПППП")
        laugh_decoded = decode_laugh(laugh_deoptimised)

        binary_output = laugh_decoded

        if shift:
            binary_output = xor_shifter.xor_shift_decode(binary_output, shift)
            if self.debug:
                print(f"shift={shift}")

        return binary_output


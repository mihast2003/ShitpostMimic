from XOR_shift import XOR_Shifter

from collections import Counter

def split_runs(s: str):
    runs = []
    current = s[0]

    for c in s[1:]:
        if c == current[-1]:
            current += c
        else:
            runs.append(current)
            current = c

    runs.append(current)
    return runs

def find_average_runlength(s: str) -> float:
    runs = split_runs(s)
    average_length = len(runs[0])
    for run in runs:
        length = len(run)
        average_length = (average_length + length) / 2
    
    return average_length


s = "001011100001100111100011011111011111001111000011100010011001000101000000010011111100111010011100101100111010011101100010110011110111001011110111000010110010100101111101011100101101000100101010000001101000001001111111010010001110010001110010011"

xor_shifter = XOR_Shifter(DEBUG=False)
shifted = xor_shifter.xor_shift_encode(binary=s, shift=5)
print("after shifting", shifted)

runs = split_runs(shifted)

average_length = find_average_runlength(shifted)
print("average run length:", average_length)


num_to_char = {
    1: "A",
    2: "B",
    3: "C",
}

code_string = ""

if runs[0][0] == 0:
    code_string+="E"
else: code_string+="F"

for run in runs:
    length = len(run)

    modificators = ""

    original_length = length

    while length > 3:
        if length % 2:
            length -= 1
            length = int(length/2)
            modificators += "F"
        else:
            length = int(length/2)
            modificators += "E"

    code_string += num_to_char[length] + modificators

    # print(f"length {original_length} was coded as {num_to_char[length] + modificators}")


print(code_string)
counts = Counter(code_string)
print("counts of each letter: ", counts)

code_runs = split_runs(code_string)

count = 0
count_single = 0
for i in range(len(code_runs)-1):
    if code_runs[i + 1][0] == "A":
        count += 1
        if len(code_runs[i + 1]) == 1:
            count_single += 1

print(f"{count} out of {len(code_runs)} end in an A, {count_single} are single") 

# print(code_runs)

# compressed_code = ""

# for run in code_runs:
#     length = len(run)
#     modificators = ""

#     while length > 1:
#         if length % 2:
#             length -= 1
#             length = int(length/2)
#             modificators += "F"
#         else:
#             length = int(length/2)
#             modificators += "E"

#     compressed_code += run[0]*length + modificators

#     # print(f"run {run} compressed as {run[0]*length + modificators}")

# print("compressed:", compressed_code)

# bits_per_letter = {
#     "A": 2,
#     "B": 3,
#     "C": 3,
#     "E": 2,
#     "F": 3,
# }

# collective_length = sum(bits_per_letter[c] for c in compressed_code)

# print(f"binary string would be {collective_length}, while original is {len(s)}")

# counts2 = Counter(compressed_code)
# print("counts of each code letter: \n", counts2)





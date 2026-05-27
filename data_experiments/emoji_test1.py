# print("\U0001F604")  # 😄
# print("\U0001F525")  # 🔥
# print("Hello 😄🔥")

# print(ord("😄"))  # gives 128293
# print(hex(ord("😄")))  # 0x1f525

# print(text.encode("unicode-escape"))  # print out b'\\U0001f525'

# emoji = "🔥"
# print(emoji)
# b = emoji.encode("utf-8")
# print(b)

# bits = "".join(f"{byte:08b}" for byte in b)
# print(bits)

# # bits = "111100000001111111000100010100111"

# chunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
# print(chunks)
# byte_values = [int(b, 2) for b in chunks]
# print(byte_values)
# b = bytes(byte_values)
# emoji = b.decode("utf-8")
# print(emoji)


print("\u2196")
print(chr(0x2198))

start = 0x1f7f0
end = 0x1faff

for codepoint in range(start, end + 1):
    print(chr(codepoint), hex(codepoint))
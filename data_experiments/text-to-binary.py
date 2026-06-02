input = "ну ты и лох конечно"
print("input:", input)

# String -> bytes
data = input.encode("utf-8")

# Convert every byte to 8-bit binary
bits = ' '.join(format(byte, '08b') for byte in data)

print("bits:", bits)
print("bits length:", len(bits))


binary = bits

# Split by spaces
chunks = binary.split()
print("chunks:", chunks)

# Convert each binary chunk into an integer byte
data = bytes(int(chunk, 2) for chunk in chunks)

# Decode bytes into text
text = data.decode("utf-8")
print("text:", text)
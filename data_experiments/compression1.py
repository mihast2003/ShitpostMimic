import zlib

text = "why is it why is it why isit why is it"
print("input:", text)

# String -> bytes
data = text.encode("utf-8")
print("raw data length:", len(data))

compressed = zlib.compress(data)
print("compressed length:", len(compressed))

input = data if data >= compressed else compressed

# Convert every byte to 8-bit binary
bits = ' '.join(format(byte, '08b') for byte in compressed)

print("bits:", bits)


binary = bits

# Split by spaces
chunks = binary.split()
print("chunks:", chunks)

# Convert each binary chunk into an integer byte
data = bytes(int(chunk, 2) for chunk in chunks)

original = zlib.decompress(data)

# Decode bytes into text
text = original.decode("utf-8")
print("text:", text)
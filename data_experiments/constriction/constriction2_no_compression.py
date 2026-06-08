import constriction
import numpy as np

text = "теперь работает что ли"

# UTF-8 bytes
data = text.encode("utf-8")

# Convert bytes -> integers
message = np.array(list(data), dtype=np.int32)

# Equal probabilities for all 256 byte values
probs = np.ones(256, dtype=np.float32) / 256.0

entropy_model = constriction.stream.model.Categorical(probs, perfect = False) #type: ignore

# Encoder
encoder = constriction.stream.stack.AnsCoder() #type: ignore

encoder.encode_reverse(message, entropy_model)

compressed = encoder.get_compressed()

print("Compressed:")
print(compressed)

print("\nBinary:")
print([bin(x) for x in compressed])

# -------------------
# Decode
# -------------------

decoder = constriction.stream.stack.AnsCoder(compressed) #type: ignore

decoded = decoder.decode(entropy_model, len(message))

# decoded = decoded[::-1]

# IMPORTANT
decoded_bytes = bytes(decoded.tolist())

decoded_text = decoded_bytes.decode("utf-8")

print(decoded_text)
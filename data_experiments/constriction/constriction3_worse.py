import constriction
import numpy as np

text = "теперь работает что ли"

# Level 1: Unicode codepoints (not UTF-8 bytes)
message = np.array([ord(c) for c in text], dtype=np.int32)

# Simple model (still weak, but valid)
probs = np.ones(0x110000, dtype=np.float32)
probs /= probs.sum()

entropy_model = constriction.stream.model.Categorical(probs, perfect = False) #type: ignore

encoder = constriction.stream.stack.AnsCoder() #type: ignore
encoder.encode_reverse(message, entropy_model)

compressed = encoder.get_compressed()

print("Compressed:")
print(compressed)

print("\nBinary:")
print([bin(x) for x in compressed])

decoder = constriction.stream.stack.AnsCoder(compressed) #type: ignore
decoded = decoder.decode(entropy_model, len(message))

decoded_text = ''.join(chr(x) for x in decoded)

print(decoded_text)
import constriction
import numpy as np

text = "hello world"

# Convert text -> integers
message = np.array([ord(c) for c in text], dtype=np.int32)


# Model for byte values
model = constriction.stream.model.Uniform(255) #type: ignore

encoder = constriction.stream.stack.AnsCoder() #type: ignore

encoder.encode_reverse(message, model)

compressed = encoder.get_compressed()

print("compressed:\n",compressed)



# Decode
decoder = constriction.stream.stack.AnsCoder(compressed) #type: ignore

decoded = decoder.decode(model, len(message))

# Convert integers back -> text
decoded_text = ''.join(chr(x) for x in decoded)

print("decoded text:", decoded_text)
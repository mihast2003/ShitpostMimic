import constriction
import numpy as np
from collections import defaultdict

# -----------------------------
# 1. INPUT TEXT → BYTES
# -----------------------------
text = "закодируй-ка этот текст 😀"

data = text.encode("utf-8")
print(data)
message = np.frombuffer(data, dtype=np.uint8)

V = 256  # byte alphabet

# -----------------------------
# 2. TRAIN BYTE BIGRAM MODEL
# -----------------------------
counts = defaultdict(lambda: np.zeros(V, dtype=np.float32))

for i in range(1, len(message)):
    prev = message[i - 1]
    curr = message[i]
    counts[prev][curr] += 1

# -----------------------------
# 3. BUILD MODELS PER CONTEXT BYTE
# -----------------------------
models = {}

for prev, arr in counts.items():
    probs = arr + 1.0  # smoothing
    probs /= probs.sum()

    models[prev] = constriction.stream.model.Categorical(
        probs.astype(np.float32),
        perfect = False
    )

# fallback model (VERY important)
uniform_model = constriction.stream.model.Categorical(
    np.ones(V, dtype=np.float32) / V,
    perfect = False
)

# -----------------------------
# 4. ENCODE
# -----------------------------
encoder = constriction.stream.stack.AnsCoder()

for i in range(len(message)):
    prev = message[i - 1] if i > 0 else None
    model_i = models.get(prev, uniform_model)

    encoder.encode_reverse(
        np.array([message[i]], dtype=np.int32),
        model_i
    )

compressed = encoder.get_compressed()

# -----------------------------
# 5. DECODE (CRITICAL FIXED PATTERN)
# -----------------------------
decoder = constriction.stream.stack.AnsCoder(compressed)

decoded = np.zeros(len(message), dtype=np.uint8)

for i in reversed(range(len(message))):
    prev = decoded[i - 1] if i > 0 else None
    model_i = models.get(prev, uniform_model)

    decoded[i] = decoder.decode(model_i, 1)[0]

# -----------------------------
# 6. BYTES → TEXT
# -----------------------------
# decoded_text = bytes(decoded).decode("utf-8")

# print(decoded_text)

decoded_bytes = bytes(decoded)

# DO NOT assume UTF-8 is valid
print(decoded_bytes)

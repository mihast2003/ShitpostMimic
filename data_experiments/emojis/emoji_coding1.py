
def recursive_xor_stack(pattern: str, repeats: int, shift: int):
    current = [int(b) for b in pattern]

    for _ in range(repeats - 1):

        shifted = [0] * shift + current

        # pad
        max_len = max(len(current), len(shifted))

        current += [0] * (max_len - len(current))
        shifted += [0] * (max_len - len(shifted))

        # XOR merge
        current = [
            a ^ b
            for a, b in zip(current, shifted)
        ]

    return "".join(map(str, current))


def visualize_stack(pattern, repeats, shift):
    lines = []

    for r in range(repeats):
        lines.append(" " * (r * shift) + pattern)

    print("\n".join(lines))

for i in range(32):
    out = recursive_xor_stack(
        pattern=bin(i)[2:],
        repeats=4,
        shift=1)

    print(out)
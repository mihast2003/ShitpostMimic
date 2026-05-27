class XOR_Shifter():
    def __init__(self, DEBUG) -> None:
        self.debug = DEBUG
        
    def xor_delta_encode(self, binary: str, shift: int = 0) -> str:
        if not binary:
            return ""
        if not shift:
            return binary

        result = []

        # preserve first shift bits
        result.extend(binary[:shift])

        for i in range(shift, len(binary)):

            a = int(binary[i - shift])
            b = int(binary[i])

            result.append(str(a ^ b))

        return "".join(result)
    

    def xor_delta_decode(self, encoded: str, shift: int = 0) -> str:
        if not encoded:
            return ""
        if not shift:
            return encoded

        result = list(encoded[:shift])

        for i in range(shift, len(encoded)):

            prev = int(result[i - shift])
            curr = int(encoded[i])

            original = prev ^ curr

            result.append(str(original))

        return "".join(result)
from collections import Counter, defaultdict
import math

class BitWriter:
    def __init__(self):
        self.buffer = 0
        self.nbits = 0
        self.out = bytearray()
        self.string = 0

    def write_bit(self, bit):
        self.string = (self.string << 1) | bit
        self.buffer = (self.buffer << 1) | bit
        self.nbits += 1

        if self.nbits == 8:
            self.out.append(self.buffer)
            self.buffer = 0
            self.nbits = 0

    def flush(self):
        if self.nbits:
            self.buffer <<= (8 - self.nbits)
            self.out.append(self.buffer)

    def get_bytes(self):
        return bytes(self.out)

class EntropyAnalyser:
    def __init__(self) -> None:
        pass

    def entropy_unigram(self, text, uni_counts, uni_total):
        counts = uni_counts
        total = uni_total

        H = 0.0

        for sym, c in counts.items():
            p = c / total
            H -= p * math.log2(p)

        return H

    def entropy_bigram(self, text, bi_counts, bi_total):
        H = 0.0

        for i in range(1, len(text)):
            prev = text[i - 1]
            sym = text[i]

            if bi_total[prev] > 0:
                count = bi_counts[prev][sym]
                total = bi_total[prev]

                if count == 0:
                    continue

                p = count / total
            else:
                continue

            H -= math.log2(p)

        return H / (len(text) - 1)


class RangeCoder:
    def __init__(self, txt):
        EOF = "\x03"
        text = txt + EOF
        self.symbols = sorted(set(text))

        # =====================================================
        # 1. UNIGRAM COUNTS (ground truth)
        # =====================================================
        self.uni_counts = Counter(text)
        self.uni_total = sum(self.uni_counts.values())



        # unigram cumulative (for range coding)
        self.uni_cum = {}
        cum = 0
        for s in self.symbols:
            self.uni_cum[s] = cum
            cum += self.uni_counts[s]

        # =====================================================
        # 2. BIGRAM COUNTS (ground truth)
        # =====================================================
        self.bi_counts = defaultdict(Counter)

        for a, b in zip(text[:-1], text[1:]):
            self.bi_counts[a][b] += 1

        # ensure all contexts exist
        for a in self.symbols:
            _ = self.bi_counts[a]

        # =====================================================
        # 3. BIGRAM TOTALS
        # =====================================================
        self.bi_total = {}
        for a in self.symbols:
            self.bi_total[a] = sum(self.bi_counts[a].values())

        # =====================================================
        # 4. BIGRAM CUMULATIVE TABLE (encoding ONLY)
        # =====================================================
        self.bi_cum = {}

        for a in self.symbols:
            self.bi_cum[a] = {}

            cum = 0
            for b in self.symbols:
                self.bi_cum[a][b] = cum
                cum += self.bi_counts[a][b]

        # =====================================================
        # 5. ESCAPE MODEL (simple, stable version)
        # =====================================================
        self.escape = {
            s: max(1, len(self.symbols) // 20)
            for s in self.symbols
        }

        # print(self.uni_counts["\x03"])
        print("EOF interval:", self.uni_cum["\x03"], self.uni_cum["\x03"] + self.uni_counts["\x03"])
        print("space interval:", self.uni_cum[" "], self.uni_cum[" "] + self.uni_counts[" "])
        # print(self.bi_counts["э"])
        # print(self.bi_total)
        # print("\x03" in self.symbols)
        # print(self.uni_counts["\x03"]) 
        # assert sorted(self.symbols) == self.symbols
        # assert "\x03" in self.symbols
        # assert self.uni_cum[self.symbols[0]] == 0

    def encode(self, txt):
        print("symbol 0 is ", ord(self.symbols[0]))

        EOF = "\x03"
        text = txt + EOF

        print("Text to encode", text)

        bw = BitWriter()

        ea = EntropyAnalyser()
        uni_entropy = ea.entropy_unigram(text, self.uni_counts, self.uni_total)
        bi_entropy = ea.entropy_bigram(text, self.bi_counts, self.bi_total)
        print(f"Estimated entropy:\n Unigram: {uni_entropy}, Bigram: {bi_entropy}")

        low = 0
        high = 0xFFFFFFFF

        pending = 0

        HALF = 0x80000000
        QUARTER = 0x40000000
        THREEQ = 0xC0000000

        print("encode start")

        def output_bit(bit):
            nonlocal pending

            bw.write_bit(bit)

            while pending:
                bw.write_bit(1 - bit)
                pending -= 1

        for i, ch in enumerate(text):
            prev = text[i - 1] if i else None

            if prev is not None and self.bi_counts[prev][ch] > 0:
                total = self.bi_total[prev]

                freq = self.bi_counts[prev][ch]

                sym_low = self.bi_cum[prev][ch]
                sym_high = sym_low + freq

                print("usin bi")


            else:
                total = self.uni_total

                freq = self.uni_counts[ch]

                sym_low = self.uni_cum[ch]
                sym_high = sym_low + freq

                print("usin uni")

            r = high - low + 1

            print("encoder STEP", i, "prev:", prev, " CHARACTER:", ch, " ord:", ord(ch))

            high = low + (r * sym_high // total) - 1
            low = low + (r * sym_low // total)

            while True:
                if high < HALF:

                    output_bit(0)

                elif low >= HALF:

                    output_bit(1)

                    low -= HALF
                    high -= HALF

                elif low >= QUARTER and high < THREEQ:

                    pending += 1

                    low -= QUARTER
                    high -= QUARTER

                else:
                    break

                low <<= 1
                high = (high << 1) | 1

                low &= 0xFFFFFFFF
                high &= 0xFFFFFFFF

            progress = bin(bw.string)
            a = list(progress)
            # Insert character at a specific position
            a.insert(2, " ")
            a.insert(11, " ")
            a.insert(20, " ")
            a.insert(29, " ")
            a.insert(38, " ")
            r1 = "".join(a)
            print(f"character {ch} encoded as {r1}")

        pending += 1

        if low < QUARTER:
            output_bit(0)
        else:
            output_bit(1)

        bw.flush()

        return bw.get_bytes()
    

    def decode(self, reader, max_symbols=200):
        print("symbol 0 is ", ord(self.symbols[0]))
        low = 0
        high = 0xFFFFFFFF

        value = 0
        for _ in range(32):
            value = (value << 1) | reader.read_bit()

        print("Initialisation complete, value is", value)

        out = []

        for _ in range(max_symbols):
            r = high - low + 1
            prev = out[-1] if out else None

            # =========================
            # SELECT MODEL
            # =========================
            use_bigram = prev is not None and self.bi_total.get(prev, 0) > 0

            print(f"Chose {use_bigram} because for ch {prev} count is {self.bi_total.get(prev, 0)}")

            if use_bigram:
                total_table = self.bi_total[prev]
                cum_table = self.bi_cum[prev]
                freq_table = self.bi_counts[prev]
            else:
                total_table = self.uni_total
                cum_table = self.uni_cum
                freq_table = self.uni_counts

            total = total_table

            # =========================
            # FIND SYMBOL
            # =========================
            ch = None
            sym_low = 0
            sym_high = 0

            for sym in self.symbols:
                freq = freq_table[sym]
                if freq == 0:
                    continue

                lo = cum_table[sym]
                hi = lo + freq

                scaled_lo = low + (r * lo) // total
                scaled_hi = low + (r * hi) // total - 1

                if scaled_lo <= value <= scaled_hi:
                    ch = sym
                    sym_low = lo
                    sym_high = hi
                    break

            if ch is None:
                raise ValueError("Decoding failed: no symbol matched interval")

            # =========================
            # EOF
            # =========================
            
            if ch == "\x03":
                print("Reached EOF")
                break

            print("DEcoder STEP", len(out), "prev:", prev, "ch:", ch, "ord:", ord(ch))
            mode = "BI" if use_bigram else "UNI"
            print("Using ", mode)

            out.append(ch)

            # =========================
            # UPDATE RANGE (SINGLE SOURCE OF TRUTH)
            # =========================
            high = low + (r * sym_high) // total - 1
            low = low + (r * sym_low) // total

            # =========================
            # RENORMALIZATION (SYMMETRIC)
            # =========================
            while True:
                if high < 0x80000000:
                    pass

                elif low >= 0x80000000:
                    value -= 0x80000000
                    low -= 0x80000000
                    high -= 0x80000000

                elif low >= 0x40000000 and high < 0xC0000000:
                    value -= 0x40000000
                    low -= 0x40000000
                    high -= 0x40000000

                else:
                    break

                low = (low << 1) & 0xFFFFFFFF
                high = ((high << 1) | 1) & 0xFFFFFFFF
                value = ((value << 1) | reader.read_bit()) & 0xFFFFFFFF

        return ''.join(out)
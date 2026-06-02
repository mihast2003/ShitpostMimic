from collections import Counter, defaultdict

class BitWriter:
    def __init__(self):
        self.buffer = 0
        self.nbits = 0
        self.out = bytearray()

    def write_bit(self, bit: int):
        self.buffer = (self.buffer << 1) | (bit & 1)
        self.nbits += 1

        if self.nbits == 8:
            self.out.append(self.buffer)
            self.buffer = 0
            self.nbits = 0

    def flush(self):
        if self.nbits > 0:
            self.buffer <<= (8 - self.nbits)
            self.out.append(self.buffer)
            self.buffer = 0
            self.nbits = 0

    def get_bytes(self):
        return bytes(self.out)

bw = BitWriter()


class RangeCoder:
    def __init__(self, text, alpha=0.01):
        self.symbols = sorted(set(text))
        self.N = len(self.symbols)
        self.alpha = alpha

        # =====================================================
        # UNIGRAM COUNTS
        # =====================================================

        self.uni_count = Counter(text)
        self.uni_total = sum(self.uni_count.values())

        # Smoothed unigram totals
        self.uni_smoothed_total = self.uni_total + alpha * self.N

        self.uni_cum = {}
        cum = 0.0

        for s in self.symbols:
            self.uni_cum[s] = cum
            cum += self.uni_count[s] + alpha

        # =====================================================
        # BIGRAM COUNTS
        # =====================================================

        self.bi_count = defaultdict(Counter)

        for a, b in zip(text[:-1], text[1:]):
            self.bi_count[a][b] += 1

        # =====================================================
        # BIGRAM TABLES
        # =====================================================

        self.bi_total = {}
        self.bi_smoothed_total = {}
        self.bi_cum = {}

        for prev in self.symbols:

            row = self.bi_count[prev]
            total = sum(row.values())

            self.bi_total[prev] = total
            self.bi_smoothed_total[prev] = total + alpha * self.N

            self.bi_cum[prev] = {}

            cum = 0.0

            for sym in self.symbols:
                self.bi_cum[prev][sym] = cum
                cum += row[sym] + alpha

    # =====================================================
    # DEBUG HELPERS
    # =====================================================

    def print_bigram(self, prev):
        row = self.bi_count[prev]
        total = self.bi_smoothed_total[prev]

        print(f"Context: {repr(prev)}")

        for sym, count in row.most_common():
            p = (count + self.alpha) / total
            print(f"{repr(sym):4s} count={count:3d} p={p:.4f}")


    def encode(self, text):
            low = 0
            high = 255
            out = []
            print("encoding text", text)

            def renorm():
                nonlocal low, high, out
                while True:
                    if high < 128:
                        bw.write_bit(0)
                        # print("append 0")
                        low <<= 1
                        high = (high << 1) | 1

                    elif low >= 128:
                        # print("append 1")
                        bw.write_bit(1)
                        low = (low - 128) << 1
                        high = ((high - 128) << 1) | 1

                    else:
                        # print("break")
                        break

                    low &= 0xFF
                    high &= 0xFF

            for i, ch in enumerate(text):
                prev = text[i - 1] if i > 0 else None
                r = high - low + 1

                # -------------------
                # choose model ONCE
                # -------------------
                use_bigram = (
                    prev is not None and
                    self.bi_total.get(prev, 0) > 0
                )

                if use_bigram:
                    total = self.bi_total[prev] + self.escape[prev]

                    # check if seen in bigram
                    if self.bi_cum[prev][ch] < self.bi_cum[prev].get(ch, 0) + 1:
                        # bigram path
                        s_low = self.bi_cum[prev][ch]
                        s_high = s_low + 1  # simplified frequency=1 step

                    else:
                        # ESCAPE
                        esc_low = self.bi_total[prev]
                        esc_high = total

                        high = low + (r * esc_high // total) - 1
                        low = low + (r * esc_low // total)
                        renorm()

                        # fallback to unigram
                        total = self.uni_total
                        s_low = self.uni_cum[ch]
                        s_high = s_low + self.uni_counts[ch]

                else:
                    total = self.uni_total
                    s_low = self.uni_cum[ch]
                    s_high = s_low + self.uni_counts[ch]

                high = low + (r * s_high // total) - 1
                low = low + (r * s_low // total)

                renorm()

            # out.append(low >> 56)
            bw.flush()
            compressed = bw.get_bytes()
            return bytes(compressed)
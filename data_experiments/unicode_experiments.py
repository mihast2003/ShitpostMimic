import unicodedata

# import emoji

# 😀 Emoticons block
# U+1F600 → U+1F64F

# 👍 Common symbols & objects
# U+1F300 → U+1F5FF

# 🟡 Colored circles/squares
# U+1F7E0 → U+1F7EB


start = 0x1F6B0
end = 0x1F7Ef

for cp in range(start, end + 1):
    char = chr(cp)
    name = unicodedata.name(char, "UNKNOWN")
    code = hex(cp)

    if name != "UNKNOWN":
        print(code, char, name)
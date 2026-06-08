import regex

ALL_EMOJIS="""‼️⏩⏪⏫⏬⏰⏳☔☕☝♈♉♊♋♌♍♎♏♐♑♒♓♿⚡⚪⚫⚽⚾⛄⛅⛔☠️☘️ℹ️↔️↕️↖️
↗️↘️↙️↩️↪️⌨️⚡⚠️⚒️⚓️⚔️⚕️⚖️⚗️⚙️⚛️⚜️♠️♣️♥️♦️♨️⚰️⚱️⛄️⛅️⛈️⛎️⛑️⛏️⛓️⛩️⛪️⛰️⛱️⛲️⛳️⛴️⛵️⛷️⛸️⛹️⛺️⛽️
✂️✅️✈️✉️✊️✋️✌️✍️✏️✒️✔️✖️✝️✨️❄️❇️❌️❎️❓️❔️❕️❗️
❣️❤️⭐️🌀🌁🌂🌃🌄🌅🌆🌇🌈🌉🌊🌋🌌🌍🌎🌏🌐🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜🌝🌞🌟🌠🌭🌮🌯🌰
🌱🌲🌳🌴🌵🌶🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞
🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼🍽🍾🍿🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏
🎐🎑🎒🎓🎠🎡🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴🎵🎶🎷🎸🎹🎺🎻🎼🎽🎾🎿🏀🏁🏂🏃🏄🏅🏆🏇🏈🏉🏊🏋
🏌🏍🏎🏏🏐🏑🏒🏓🏔🏕🏖🏗🏘🏙🏚🏛🏜🏝🏞🏟🏠🏡🏢🏣🏤🏥🏦🏧🏨🏩🏪🏫🏬🏭
🕠🕡🕢🕣🕤🕥🕦🕧🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛🕜🕝🕞🕟🔰🔱🔲🔳🔴🔵🔶🔷🔸🔹🔺🔻🔼🔽🏯🏰🏳🏴🏵🏷🏸🏹🏺
🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛🐜🐝
🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾🐿👀👁👂👃👄👅👆👇
👈👉👊👋👌👍👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢👣👤👥👦👧👨👩👪👫👬👭👮👯👰👱👲👳👴
👵👶👷👸👹👺👻👼👽👾👿💀💁💂💃💄💅💆💇💈💉💊💋💌💍💎💏💐💑💒💓💔💕💖💗💘💙💚💛💜💝
💞💟💠💡💢💣💤💥💦💧💨💩💪💫💬💭💮💯💰💱💲💳💴💵💶💷💸💹💺💻💼💽💾💿📀📁📂📃📄📅📆📇📈📉📊📋
📌📍📎📏📐📑📒📓📔📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧📨📩📪📫📬📮📯📰📱📲📳📴📵📶📷📸📹📺📻📼📽📾📿
🗺️🗻🗼🗽🗾🗿😀😁😂😃😄😅😆😇😈😉😊😋😌😍😎😏😐😑😒😓😔😕😖😗😘😙😚😛😜😝😞😟😠😡😢😣😤😥😦😧😨😩😪😫
😬😭😮😯😰😱😲😳😴😵😶😷😸😹😺😻😼😽😾😿🙀🙁🙂🙃🙄🙅🙆🙇🙈🙉🙊🙋🙌🙍🙎🚀🚁🚂🚃🚄🚅🚆🚇🚈🚉🚊
🚋🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚙🚚🚛🚜🚝🚞🚟🚠🚡🚢🚣🚤🚥🚦🚧🚨🚩🚪🚫🚬🚭🚮🚯🚰🚱🚲🚳🚴🚵🚶🚷
🚸🚹🚺🚻🚼🚽🚾🚿🛀🛁🛂🛃🛄🛅🛌🛍🛎🛏🤏🤐🤑🤒🤓🤔🤕🤖🤗🤘🤙🤚🤛🤜🤝🤞🤟🤠🤡🤢🤣🤤🤥🤦🤧🤨🤩🤪🤫🤬🤭
🤮🤯🤰🤱🤲🤳🤴🤵🤶🤷🤸🤹🤺🤻🤼🤽🤾🤿🥀🥁🥂🥃🥄🥅🥇🥈🥉🥊🥋🥌🥍🥎🥏🥐🥑🥒🥓🥔🥕🥖🥗🥘🥙🥚🥛🥜🥝🥞
🥠🥡🥢🥣🥤🥥🥦🥧🥨🥩🥪🥫🥬🥭🥮🥯🥰🥱🥲🥳🥴🥵🥶🥺🥻🥼🥽🥾🥿🦀🦁🦂🦃🦄🦅🦆🦇🦈🦉🦊🦋🦌🦍🦎🦏🦐🦑
🦒🦓🦔🦕🦖🦗🦘🦙🦚🦛🦜🦝🦞🦟🦠🦡🦢🦥🦦🦧🦨🦩🦪🦮🦯🦰🦱🦲🦳🦴🦵🦶🦷🦸🦹🦺🦻🦼🦽🦾🦿🧀🧁🧂🧃🧄🧅🧆🧇
🧈🧉🧊🧍🧎🧏🧐🧑🧒🧓🧔🧕🧖🧗🧘🧙🧚🧛🧜🧝🧞🧟🧠🧡🧢🧣🧤🧥🧦🧧🧨🧩🧪🧫🧬🧭🧮🧯🧰🧱🧲🧳🧴🧵🧶🧷🧸🧹🧺
🧻🧼🧽🧿🩰🩱🩲🩳🩸🩹🩺🪀🪁🪂🪐🪑🪒🪓🪔🪕
"""


# now to select 512
RAW_STRING = ALL_EMOJIS

EMOJIS_LIST= regex.findall(r"\X", RAW_STRING.replace("\n", "").replace(" ", ""))

print(len(EMOJIS_LIST))
# print(EMOJIS_LIST)

EMOJI_TO_VALUE = {emoji: i for i, emoji in enumerate(EMOJIS_LIST)}

def emojis_to_binary(emojis):
    """
    Convert a list of emojis into a binary string.
    Each emoji represents a 6-bit value.
    """
    return "".join(
        format(EMOJI_TO_VALUE[e], "010b")
        for e in emojis
    )

def binary_to_emoji(binary):
    if len(binary) % 10 != 0:
        raise ValueError("Binary string length must be a multiple of 10")

    return "".join(
        EMOJIS_LIST[int(binary[i:i+10], 2)]
        for i in range(0, len(binary), 10)
    )



binary = "11101011111110011110000010111011010011001101011000"

print("binary length", len(binary))

encoded = binary_to_emoji(binary=binary)
print(encoded)

data = regex.findall(r"\X", encoded)
binary = emojis_to_binary(data)

print(binary)

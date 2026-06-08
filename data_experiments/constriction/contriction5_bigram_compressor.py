import constriction
import numpy as np
from collections import Counter
from collections import defaultdict
import math

# -------------------
# Reference text (training data)
# -------------------
ref_text = """вот я использую русский язык чтобы как дела привет я ни разу не использовал букву м например мороженое и можно пойти сделать что-то другое то у 
тебя да так. лол ниче особенного сижу себе а ты что делаешь а я ниче особенного: вот это 
вот циферки 1234567890 да я не знаю ваще- = + _ . , съешь ещё этих французских булочек да выпей чаю? / да. а я уже почти всё доделал тебе осталось только подключить наверное...
Я могу попробовать сделать более таймлапсное, типа чтоб карандаши кто-то подвигал, кофе налил, бумагу положил и написал что-то
это единственное что я нашëл uwu типа листики двигаются и их тени тоже двигаются но я вообще считаю что идея так себе нужно что-то со светом 
сделал треугольник разобрал как делать треугольник перекрасил треугольник, поменял размеры и т.д. сделал квадрат разобрал как делать квадрат и почему это 2 треугольникасделал из квадрата градиент от синего к красномуразобрал как это работает сделал чëткую границу медлу синим и красным
по принципу типа: x пикселя < 0 - значит красный, если нет то синий посмотрел как это работает сделал синий круг из пикселей внутри красного квадратавсë же
Что тебе надо пойти и попросить иишку показать тебе как отрендерить треугольник на экране с помощью, посмотреть работает оно или нет, а потом час допрашивать  расспрашивать про каждый кусочек кода
О господи, я такое вспомнил Я когда-то давно, лет 7 назад пробовал программирование и я сделал увутор Это питон был? Я не помню даже xddd
Типа вставляешь текст а он знаки препинания меняет на uwu и owo, а потом ещё и где в мловах есть owo добавляет о тожеэто мод
ну для рендера чтобы шейдеры включать так-то тоже мод нужен блин, он только на 1.21.1 походу капяо кажется это какая-то жопа
как обычно куда я лезу постоянно :D как я постоянно оказываюсь в крутых комьюнити состоящих из полтора человека
Ты забыл в шахматах походить , _ , Мне уведомление пришло что я выиграл я не особо хотел ты замок там строил город ну или кого там
ну да странновато выглядит дана сказала что ей эстетически не нравится что кофе оставили настолько
xd Я могу попробовать сделать более таймлапсное, типа чтоб карандаши кто-то подвигал, кофе налил, бумагу положил и написал что-то
ну не знаю, не знаю попробуй Попробую А то оно неживое какое-то Тебе написать скрипт падения листика?
Я делаю портфолио, собираю рефы концептиков персонажей и в свободное время кодю фигню Сижу с ума схожу uwu owo
Это оказалось сложнее чем я думал Я домоооой Я значит сижу в паспортном эээ столе? Почемуто мне кажется оно так называется
И тут штука которую мы печатали ":D Прикол Дап Я таво :,) Как мне себе верить Я андрею подписала 25 шт вешалок с вырезом А надо 10 было хддд Блэп Он хотябы порезать все не успел и я много с заказчика взяла :_3 Вот так вот Бывает, ниче страшного Мгм  В стемльках довольно чух Пока что по крайней мере
А еще помнишь у меня шишка на ноге там где у мизинца у плюсневой кости бугорок такой Мы с подологом
Выяснили что это скорее всего из-за того что я сижу по турецки часто М :( Как делааа Нас это Мать покормит Мямсой
Я забыла сказать Вот Добровое Я в кафешке рядом с работой сижу Выдержка из моего дневн; ка: Я приехала к 9 в паспортный стол
И я бвла хз чо делать узнавала у людей чо делоть Оказывается нужно было брать талончик, а чтобы его взять надо было код знать с приложения госуслуг
Я об этом не знала а мобильного нету >:') Я психанула включила тот который 50 рэ но почемуто не работало ММужик раздал мне инет , п,Первое:
Нужно увеличить какой-либо элемент, лиьо уменьшить, чтобы был контраст размеров. Например картинка очень большая а текст небольшой.
Можно уменьшить текст " савиньон" и "белое сухое", а вот арман и тбд можно увеличить, для акцента на назвонии Товарищи зацените дизайн
Это тестовое упаковка вина Первое премиальный классичесткий стиль, второе лаконичное современное Мне очень нравится концовка, и я пытаюсь понять почему не нравится начало
Правое которое? Все прикольно выглядят, но левое верхнее плохо читается из за разрыва, а левое нижнее немного скушное(его можно улучшить, если увеличить фирменный знак - это если тебе понадобится строчный вариант). А так класстка побеждает.
"""

ref_text = ref_text.lower()
ref_text = " ".join(ref_text.splitlines())
print(ref_text)

counts = Counter(ref_text)
print(counts)

# -------------------
# Build alphabet
# -------------------
alphabet = sorted(set(ref_text))
char_to_id = {c: i for i, c in enumerate(alphabet)}
id_to_char = {i: c for i, c in enumerate(alphabet)}

ref_msg = np.array([char_to_id[c] for c in ref_text], dtype=np.int32)

# -------------------
# Learn probabilities
# -------------------
counts = np.bincount(ref_msg, minlength=len(alphabet))
global_probs = counts / counts.sum()

global_model = constriction.stream.model.Categorical(global_probs.astype(np.float32), perfect = False) #type: ignore

# -------------------
# Message to compress
# -------------------
text = "могу попробовать более длинный текст, что скажешь uwu так нечестно наверное но я не знаю как иначе"
# text = text * 10
text = text.lower()

entropy = -np.sum(global_probs * np.log2(global_probs))
print(entropy)
theoretical_bits = entropy * len(text)
print("theoretical_bits:", theoretical_bits)

# convert text to id
message = np.array([char_to_id[c] for c in text], dtype=np.int32)


# -----------------------
# 3. Build bigram counts
# -----------------------
num_symbols = len(alphabet)
counts = np.zeros((num_symbols, num_symbols), dtype=np.int32)


for prev, curr in zip(ref_msg[:-1], ref_msg[1:]):
    if prev < 0 or curr < 0:
        continue
    if prev >= num_symbols or curr >= num_symbols:
        continue
    counts[prev, curr] += 1

alpha = 1e-1

probs = (counts + alpha) / (counts.sum(axis=1, keepdims=True) + alpha * num_symbols)
# probs = counts / counts.sum(axis=1, keepdims=True)

for i in range(num_symbols):
    p = probs[i]
    
    print(
        id_to_char[i],
        "max:", np.max(p),
        "min:", np.min(p),
        "sum:", np.sum(p)
    )

probs_test = probs
# for prev in range(num_symbols):
#     probss = probs_test[prev]

#     top = np.argsort(-probss)[:10]  # top 10 most likely next symbols

#     print("\nPrev symbol:", id_to_char[prev])
#     print("Top transitions:")
    
#     for j in top:
#         print(f"  {id_to_char[j]}: {probss[j]:.3f}")

# idx = char_to_id['ё']
# print("row sum:", counts[idx].sum())
# print("row:", counts[idx])
# -----------------------
# 5. Build per-context ANS models
# -----------------------
models = []

for prev in range(num_symbols):
    model = constriction.stream.model.Categorical(  #type: ignore
        probs[prev].astype(np.float32),
        perfect=False
    )
    models.append(model)

# -------------------
# Encode
# -------------------
encoder = constriction.stream.stack.AnsCoder() #type: ignore

# Encode backwards (ANS requirement)

# last symbol uses global model (no context)
encoder.encode_reverse(message[-1], global_model)

# remaining symbols
for i in range(len(message) - 2, -1, -1):
    if i == 0:
        # first symbol has no previous context → fallback
        encoder.encode_reverse(message[i], models[message[i]])
    else:
        prev = message[i + 1]
        encoder.encode_reverse(message[i], models[prev])


compressed = encoder.get_compressed()


print("Compressed:\n", compressed)

for x in compressed:
    print(f"{x:032b}")

bits = 0
for i in range(len(message)):
    if i == 0:
        p = global_probs[message[i]]
    else:
        p = probs[message[i-1], message[i]]

    bits += -math.log2(p)

print("bits CAN BE ", bits)

byte_stream = np.asarray(compressed, dtype=np.uint32).tobytes()

total_bits = len(byte_stream) * 8

print("\nBinary length:", total_bits)
# print([bin(x) for x in compressed])



# # -------------------
# # Decode
# # -------------------
# decoder = constriction.stream.stack.AnsCoder(compressed) #type: ignore
# decoded = decoder.decode(entropy_model, len(message))

# decoded_text = ''.join(id_to_char[i] for i in decoded)

# print(decoded_text)
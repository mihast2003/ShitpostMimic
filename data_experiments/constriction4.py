import constriction
import numpy as np

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
Ты забыл в шахматах походить , _ , Мне уведомление пришло что я выиграл я не особо хотел ты замок там строил город ну или кого там"""
ref_text = ref_text.lower()
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
probs = counts / counts.sum()

entropy_model = constriction.stream.model.Categorical(probs.astype(np.float32), perfect = False) #type: ignore

# -------------------
# Message to compress
# -------------------
text = "закодируй-ка этот текст а если я его изменю что будет"

text = text.lower()
message = np.array([char_to_id[c] for c in text], dtype=np.int32)

# -------------------
# Encode
# -------------------
encoder = constriction.stream.stack.AnsCoder() #type: ignore
encoder.encode_reverse(message, entropy_model)

compressed = encoder.get_compressed()


print("Compressed:")
print(compressed)

compressed_bytes = np.asarray(compressed, dtype=np.uint32).view(np.uint8)
print(len(compressed_bytes) * 8)

total_bits = total_bits = len(compressed) * 32

print("\nBinary length:", total_bits)
print([bin(x) for x in compressed])

# -------------------
# Decode
# -------------------
decoder = constriction.stream.stack.AnsCoder(compressed) #type: ignore
decoded = decoder.decode(entropy_model, len(message))

decoded_text = ''.join(id_to_char[i] for i in decoded)

print(decoded_text)
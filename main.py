import telebot
from telebot import types, apihelper
import threading
import re
import time
import html
import random
import json
import os

bot = telebot.TeleBot('8420646631:AAHs-SwPeJMUz9CUQikEP9E8TKC4eWw0NkY')

try:
    BOT_ID = bot.get_me().id
except apihelper.ApiTelegramException as e:
    print("[ERROR] Can't connect to Telegram. Check WIFI or VPN connection.")


food_words = ["Яблоко", "Молоко", "Хлеб", "Сыр", "Масло", "Яйцо", "Рис", "Макароны", "Картофель", 
            "Морковь", "Огурец", "Помидор", "Банан", "Апельсин", "Груша", "Курица", "Говядина", "Свинина", "Рыба", 
            "Креветка", "Колбаса", "Ветчина", "Йогурт", "Сметана", "Творог", "Каша", "Овсянка", "Гречка", "Пшено", 
            "Мед", "Сахар", "Соль", "Перец", "Шоколад", "Печенье", "Торт", "Пирог", "Булочка", "Мороженое", "Суп", 
            "Борщ", "Пельмени", "Вареники", "Пицца", "Бургер", "Салат", "Капуста", "Свекла", "Чеснок", "Лук", "Клубника", 
            "Малина", "Черника", "Арбуз", "Дыня", "Манго", "Ананас", "Киви", "Авокадо", "Лимон", "Лайм", "Гранат", "Финик", 
            "Инжир", "Изюм", "Орех", "Миндаль", "Фундук", "Фисташки", "Арахис", "Грибы", "Шампиньоны", "Лосось", "Тунец", 
            "Икра", "Кальмар", "Мидии", "Осьминог", "Краб", "Сосиски", "Бекон", "Шаурма", "Хот-дог", "Лазанья", "Равиоли", 
            "Роллы", "Суши", "Тофу", "Соевый соус", "Кетчуп", "Майонез", "Горчица", "Хумус", "Фалафель", "Кускус", "Булгур", 
            "Нут", "Чечевица", "Фасоль", "Горошек", "Ячмень", "Соя", "Кукуруза", "Чечевица", "Фасоль", "Горох", "Овсянка", "Гречка", "Пшеница", "Рис",
            "Тыква", "Баклажан", "Кабачок", "Перец", "Помидор", "Огурец", "Морковь", "Свекла", "Капуста", "Лук",
            "Чеснок", "Шпинат", "Руккола", "Салат", "Базилик", "Кинза", "Укроп", "Петрушка", "Мята", "Лавровый лист",
            "Яблоко", "Груша", "Банан", "Апельсин", "Мандарин", "Лимон", "Лайм", "Киви", "Ананас", "Манго",
            "Арбуз", "Дыня", "Клубника", "Малина", "Черника", "Смородина", "Вишня", "Черешня", "Слива", "Абрикос",
            "Персик", "Нектарин", "Гранат", "Финик", "Инжир", "Кокос", "Авокадо", "Фундук", "Миндаль", "Арахис",
            "Фисташка", "Кешью", "Пекан", "Кедровый орех", "Семена тыквы", "Семена подсолнечника", "Семена льна", "Какао", "Шоколад", "Мёд",
            "Молоко", "Сметана", "Йогурт", "Творог", "Кефир", "Ряженка", "Масло", "Сыр", "Моцарелла", "Пармезан",
            "Бри", "Чеддер", "Рикотта", "Тофу", "Яйцо", "Курица", "Говядина", "Свинина", "Баранина", "Индейка",
            "Рыба", "Лосось", "Тунец", "Скумбрия", "Креветка", "Краб", "Мидии", "Кальмар", "Осьминог", "Икра",
            "Булгур", "Кускус", "Мюсли", "Гранола", "Киноа", "Паста", "Хлеб", "Багет", "Круассан", "Рогалик"]

not_food_words = ["Стол", "Стул", "Дом", "Окно", "Дверь", "Телефон", "Компьютер", "Книга", "Тетрадь", "Ручка", 
                "Карандаш", "Часы", "Сумка", "Ключ", "Замок", "Машина", "Дорога", "Улица", "Мост", "Парк", "Школа", 
                "Работа", "Офис", "Комната", "Кровать", "Шкаф", "Полка", "Зеркало", "Лампа", "Розетка", "Провод", "Экран", 
                "Кнопка", "Мышь", "Клавиатура", "Наушники", "Рюкзак", "Кошелек", "Одежда", "Куртка", "Обувь", "Носок", 
                "Шапка", "Погода", "Время", "День", "Ночь", "Утро", "Вечер", "Город", "Село", "Квартира", "Подъезд", 
                "Лифт", "Лестница", "Балкон", "Потолок", "Пол", "Стена", "Крыша", "Почта", "Письмо", "Конверт", "Марка", 
                "Паспорт", "Документ", "Подпись", "Очередь", "Светофор", "Остановка", "Автобус", "Трамвай", "Метро", "Билет", 
                "Расписание", "Карта", "Навигатор", "Интернет", "Сайт", "Пароль", "Аккаунт", "Сообщение", "Звонок", "Камера", 
                "Фотография", "Видео", "Музыка", "Фильм", "Сериал", "Игра", "Уровень", "Настройка", "Обновление", "Ошибка", 
                "Проект", "Задача", "План", "Отчёт", "Результат", "Ручка", "Карандаш", "Тетрадь", "Книга", "Стол", "Стул", "Кресло", "Шкаф", "Полка", "Диван",
                "Кровать", "Подушка", "Одеяло", "Лампа", "Светильник", "Люстра", "Зеркало", "Картина", "Фотография", "Часы",
                "Телефон", "Компьютер", "Ноутбук", "Планшет", "Мышь", "Клавиатура", "Экран", "Принтер", "Наушники", "Колонки",
                "Камера", "Фотоаппарат", "Видеокамера", "Проектор", "Телевизор", "Радио", "Кондиционер", "Обогреватель", "Вентилятор", "Пылесос",
                "Дверь", "Окно", "Балкон", "Крыша", "Лестница", "Лифт", "Перила", "Пол", "Потолок", "Стена",
                "Ключ", "Замок", "Карта", "Навигатор", "Билет", "Проездной", "Паспорт", "Документ", "Подпись", "Сумка",
                "Рюкзак", "Кошелек", "Зонт", "Чехол", "Очки", "Очки солнцезащитные", "Часы наручные", "Браслет", "Кольцо", "Серьги",
                "Обувь", "Кроссовки", "Ботинки", "Туфли", "Сапоги", "Шапка", "Шарф", "Перчатки", "Носки", "Ремень",
                "Одежда", "Куртка", "Пальто", "Платье", "Юбка", "Рубашка", "Футболка", "Блузка", "Кофта", "Свитер",
                "Мяч", "Велосипед", "Самокат", "Автомобиль", "Мотоцикл", "Скейтборд", "Коньки", "Лыжи", "Сноуборд", "Лодка"]

RUS_ALPHABET = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")

#region translation tables
rus_to_eng = str.maketrans({
    "А": "F",
    "Б": "<",
    "В": "D",
    "Г": "U",
    "Д": "L",
    "Е": "T",
    "Ё": "~",
    "Ж": ":",
    "З": "P",
    "И": "B",
    "Й": "Q",
    "К": "R",
    "Л": "K",
    "М": "V",
    "Н": "Y",
    "О": "J",
    "П": "G",
    "Р": "H",
    "С": "C",
    "Т": "N",
    "У": "E",
    "Ф": "A",
    "Х": "{",
    "Ц": "W",
    "Ч": "X",
    "Ш": "I",
    "Щ": "O",
    "Ъ": "}",
    "Ы": "S",
    "Ь": "M",
    "Э": '"',
    "Ю": ">",
    "Я": "Z",
    "а": "f",
    "б": ",",
    "в": "d",
    "г": "u",
    "д": "l",
    "е": "t",
    "ё": "`",
    "ж": ";",
    "з": "p",
    "и": "b",
    "й": "q",
    "к": "r",
    "л": "k",
    "м": "v",
    "н": "y",
    "о": "j",
    "п": "g",
    "р": "h",
    "с": "c",
    "т": "n",
    "у": "e",
    "ф": "a",
    "х": "[",
    "ц": "w",
    "ч": "x",
    "ш": "i",
    "щ": "o",
    "ъ": "]",
    "ы": "s",
    "ь": "m",
    "э": "'",
    "ю": ".",
    "я": "z",
    "!": "!",
    '"': "@",
    "№": "#",
    ";": "$",
    "%": "%",
    ":": "^",
    "?": "&",
    "*": "*",
    "(": "(",
    ")": ")",
    "_": "_",
    "+": "+",
    ",": "?",
    ".": "/",
})

eng_to_rus = str.maketrans({
    "F": "А",
    "<": "Б",
    "D": "В",
    "U": "Г",
    "L": "Д",
    "T": "Е",
    "~": "Ё",
    ":": "Ж",
    "P": "З",
    "B": "И",
    "Q": "Й",
    "R": "К",
    "K": "Л",
    "V": "М",
    "Y": "Н",
    "J": "О",
    "G": "П",
    "H": "Р",
    "C": "С",
    "N": "Т",
    "E": "У",
    "A": "Ф",
    "{": "Х",
    "W": "Ц",
    "X": "Ч",
    "I": "Ш",
    "O": "Щ",
    "}": "Ъ",
    "S": "Ы",
    "M": "Ь",
    '"': "Э",
    ">": "Ю",
    "Z": "Я",
    "f": "а",
    ",": "б",
    "d": "в",
    "u": "г",
    "l": "д",
    "t": "е",
    "`": "ё",
    ";": "ж",
    "p": "з",
    "b": "и",
    "q": "й",
    "r": "к",
    "k": "л",
    "v": "м",
    "y": "н",
    "j": "о",
    "g": "п",
    "h": "р",
    "c": "с",
    "n": "т",
    "e": "у",
    "a": "ф",
    "[": "х",
    "w": "ц",
    "x": "ч",
    "i": "ш",
    "o": "щ",
    "]": "ъ",
    "s": "ы",
    "m": "ь",
    "'": "э",
    ".": "ю",
    "z": "я",
    " ": " ",
    "!": "!",
    "@": '"',
    "#": "№",
    "$": ";",
    "%": "%",
    "^": ":",
    "&": "?",
    "*": "*",
    "(": "(",
    ")": ")",
    "_": "_",
    "+": "+",
    "?": ",",
    "/": ".",
})

#endregion

#region --- HELPERS ---
def update_highscore(game_name: str, user_id: int, value):
    highscores.setdefault(user_id, {})
    highscores[user_id].setdefault(game_name, {})
        
    highscores[user_id][game_name] = value

    save_highscores()
    
def get_leaderboard(game_name):
    leaderboard = []

    for user_id_str, games_dict in highscores.items():
        score = games_dict.get(game_name)
        if score is not None:
            leaderboard.append((int(user_id_str), score))

    # Sort by score descending
    leaderboard.sort(key=lambda x: x[1], reverse=True)

    # Return top 3
    return leaderboard[:3]

def save_highscores():
    with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(highscores, f, ensure_ascii=False, indent=2)

def load_highscores():
    """Load highscores from file, create file if missing or corrupted."""
    if not os.path.exists(HIGHSCORES_FILE):
        print("highscores.json not found. Creating a new one.")
        with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}

    try:
        with open(HIGHSCORES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Convert user_id keys back to int
            converted = {int(user_id): value for user_id, value in data.items()}
            print("Highscores loaded successfully.")
            return converted
    except json.JSONDecodeError:
        print("Warning: highscores.json is corrupted! Starting fresh.")
        with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}

def contains_russian(text):
    return re.search(r"[А-Яа-яЁё]", text) is not None

def delete_later(chat_id, message_id, delay):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print("Delete error:", e)

def safe(text: str) -> str:
    return html.escape(text)

def remove_first_line(text: str) -> str:
    lines = text.splitlines()

    if len(lines) > 1:
        new_text = "\n".join(lines[1:])
    else:
        new_text = ""

    return new_text

def remove_buttons(message):
    bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=None  # Remove all buttons
    )

def safe_call(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        except apihelper.ApiTelegramException as e:
            if e.error_code == 429:
                try:
                    retry_after = int(e.description.split(':')[-1].strip())
                except ValueError:
                    retry_after = 30
                print(f"[429] Retrying in {retry_after}s...")
                time.sleep(retry_after)
            else:
                raise
#endregion

#region --- FOR CHARACTER TRANSLATION---

def encode_message(text: str):
    return text.translate(rus_to_eng)

def decode_message(text: str):
    return text.translate(eng_to_rus)


def generate_translation_tables_from_strings(keys: str, values: str):
    """
    Generates encode and decode dictionaries from two strings.
    Each character in `keys` maps to the character at the same position in `values`.
    """
    if len(keys) != len(values):
        raise ValueError("Keys and values must have the same length")
    
    encode_dict = {k: v for k, v in zip(keys, values)}
    decode_dict = {v: k for k, v in zip(keys, values)}

    # Pretty print for easy copy-paste
    def pretty_print(d, name="dict"):
        print(f"{name}")
        for k, v in d.items():
            print(f'    "{k}": "{v}",')
        print("}\n")
    
    pretty_print(encode_dict, "encode_dict")
    pretty_print(decode_dict, "decode_dict")
    
    return encode_dict, decode_dict


# keys = """!"№;%:?*()_+,."""
# values = """!@#$%^&*()_+?/"""
# encode_dict, decode_dict = generate_translation_tables_from_strings(keys, values)

#endregion

settings = {"no_russian": False, "force_translate": False, "translate_when_asked": True}

GAME_DURATION = 60  # seconds
CHANCE_OF_UPPERCASE_LETTER = 0.2

games = {}  # user_id -> game state
HIGHSCORES_FILE = "highscores.json"
highscores = load_highscores()

previous_game = {}

#region COMMANDS handlers
@bot.message_handler(commands=["help", "?", "commands"])
def help(message):
    bot.send_message(message.chat.id, "<i>List of all commands:</i>\n", parse_mode="html")
    bot.send_message(message.chat.id, "/settings - shows you your settings.\n")
    bot.send_message(message.chat.id, "/norus - filters out messages with russian characters.\n")
    bot.send_message(message.chat.id, "/force - force translates all russian messages.\n")
    bot.send_message(message.chat.id, "/translate - allows translations when asked.\n")

@bot.message_handler(commands=["norussian", "no_russian", "no russian", "norus", "no rus"])
def norussian_toggle(message):
    settings["no_russian"] = not settings["no_russian"]
    bot.send_message(message.chat.id, f"NO RUSSIAN SET TO <i>{settings["no_russian"]}</i>", parse_mode="html")

@bot.message_handler(commands=["start", "main", "hello"])
def main(message):
    bot.send_message(message.chat.id, "Ghbdtn!")

@bot.message_handler(commands=["settings",])
def show_settings(message):
    bot.send_message(message.chat.id, f"Settings \n {settings}")

@bot.message_handler(commands=["force",])
def force_translate_toggle(message):
    settings["force_translate"] = not settings["force_translate"]
    settings["no_russian"] = settings["force_translate"]

    bot.send_message(message.chat.id, f"FORCE TRANSLATE SET TO <i>{settings["force_translate"]}</i>", parse_mode="html")

@bot.message_handler(commands=["translate_when_asked", "translate"])
def translate_when_asked_toggle(message):
    settings["translate_when_asked"] = not settings["translate_when_asked"]

    bot.send_message(message.chat.id, f'"TRANSLATE WHEN ASKED" SET TO <i>{settings["translate_when_asked"]}</i>', parse_mode="html")

@bot.message_handler(commands=['highscore', "hs"])
def show_highscore(message):
    user_id = message.from_user.id
    user_scores = highscores.get(user_id)

    if not user_scores:
        bot.reply_to(message, "You don't have any highscores yet. Wanna /play?")
        return

    lines = "\n".join(
        f"In {game} your highscore is {score}! 🏆"
        for game, score in user_scores.items()
    )

    bot.reply_to(message, lines)

@bot.message_handler(commands=['leaderboard', "lb", 'leaderboards'])
def show_leaderboard(message):

    lines = "🏆 <b>Leaderboard:</b>\n──────────────\n\n"

    for game_name in ["Food/notFood", "Alphabet"]:  # update list when you add games

        lines += f"<b>{game_name}</b>:\n"

        top_players = get_leaderboard(game_name)

        if not top_players:
            lines += "No scores yet.\n"
        else:
            for i, (player_id, score) in enumerate(top_players, start=1):
                try:
                    chat = bot.get_chat(player_id)
                    username = chat.username
                    if username:
                        name = f"@{username}"
                    else:
                        name = chat.first_name
                except:
                    name = "Unknown"

                medals = ["🥇", "🥈", "🥉"]
                medal = medals[i-1] if i <= 3 else f"{i}."

                lines += f"{medal} {name}: <b>{score}</b>\n"

        lines += "──────────────\n\n"

    bot.send_message(chat_id=message.chat.id, text=lines, parse_mode="HTML")

#endregion


# region WORDS game code
def start_words_game(chat_id, user_id):

    games[user_id] = {
    "game_name": "words",
    "current_word": None,
    "used_words": set(),
    "player_turn": True,
    }

    word_pool = food_words + not_food_words
    first_word = random.choice(word_pool)

    return
    # acceptable_words = 

    # next_word = random.choice()

def words_game_turn():
    pass

def bot_choose_word(current_word, word_pool, used_words):
    candidates = [w for w in word_pool 
                  if w[0].lower() == current_word[-1].lower() 
                  and w.lower() not in used_words]
    if not candidates:
        return None  # Bot cannot continue → player wins
    return random.choice(candidates)

def is_valid_word(user_word, current_word, used_words):
    if not user_word:
        return False
    if user_word[0].lower() != current_word[-1].lower():
        return False
    if user_word.lower() in used_words:
        return False
    return True
#endregion


#region ALPHABET game code
def start_alphabet_game(user_id, chat_id):
    letters = RUS_ALPHABET.copy()
    random.shuffle(letters)

    msg_id = bot.send_message(chat_id, f"Loading game...").id

    games[user_id] = {
        "game_name": "Alphabet",
        "letters": letters,
        "current_index": 0,
        "streak": 0,
        "level": 0,
        "msg_id": msg_id,
        "num_options": int(2),
        "correct": ""
    }
    send_next_letters(user_id, chat_id)

def next_level_alphabet(user_id, chat_id):
    game = games[user_id]
    level = game["level"]

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Yes", callback_data=f"next_level_yes")
    btn2 = types.InlineKeyboardButton(text="No", callback_data=f"next_level_no")
    markup.row(btn1, btn2)

    bot.edit_message_text(chat_id=chat_id, message_id=game["msg_id"], text=f"🏆 You finished all letters on level {level}!\nYour streak: {game['streak']}.\nContinue?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("next_level_"))
def handle_alphabet_level_change(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id

    if user_id not in games:
        bot.answer_callback_query(call.id, "Game not active!")
        return
    
    chat_id = call.message.chat.id

    game = games[user_id]

    if call.data == "next_level_yes":
        letters = RUS_ALPHABET.copy()
        random.shuffle(letters)
        game["current_index"] = 0
        game["num_options"] += 2
        game["level"] += 1
        send_next_letters(user_id, chat_id)
    elif call.data == "next_level_no":
        end_alphabet_game(user_id=user_id, chat_id=chat_id)


def send_next_letters(user_id, chat_id):
    game = games[user_id]

    if game["current_index"] >= len(game["letters"]):
        next_level_alphabet(user_id=user_id, chat_id=chat_id)
        return

    correct_letter: str = game["letters"][game["current_index"]]

    if random.random() > CHANCE_OF_UPPERCASE_LETTER:
        correct_letter = correct_letter.lower()

    game["correct_letter"] = correct_letter

    encrypted = encode_message(correct_letter)

    options = generate_options(game, correct_letter)

    markup = types.InlineKeyboardMarkup()
    btns = []
    for letter in options:
        btn = types.InlineKeyboardButton(
                text=safe(letter),
                callback_data=f"alpha_{letter}"
            )
        btns.append(btn)
    
    markup.row(*btns)
    

    text = f"⬆️ <i>Level: {game['level']}</i>    🔥 <i>Streak: {game['streak']}</i>\n\n    What is this letter?\n\n<b>                    {safe(encrypted)}</b>\n_____________________"


    delay = 0.1 if bot.get_chat(chat_id).type == "private" else 0.4
    time.sleep(delay)

    try:
        bot.edit_message_text(
            text,
            chat_id,
            game["msg_id"],
            reply_markup=markup,
            parse_mode="HTML"
        )
    except: bot.send_message(chat_id, f"Something broke...")


def generate_options(game, correct_letter: str):
    options = [correct_letter]
    num_of_options = game["num_options"]

    while len(options) < num_of_options:
        letter = random.choice(RUS_ALPHABET)
        if correct_letter.islower(): # if the answer is lowercase, the options are lowercase too
            letter = letter.lower()
        if letter not in options:
            options.append(letter)

    random.shuffle(options)
    return options


@bot.callback_query_handler(func=lambda call: call.data.startswith("alpha_"))
def handle_alphabet_answer(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id

    if user_id not in games:
        bot.answer_callback_query(call.id, "Game not active!")
        return

    game = games[user_id]

    chosen = call.data.split("_")[1]
    correct = game["correct_letter"]

    if chosen == correct:
        game["streak"] += 1
        game["current_index"] += 1

        send_next_letters(
            user_id,
            call.message.chat.id
        )

    else: 
        game["correct"] = correct
        end_alphabet_game(user_id=user_id, chat_id=call.message.chat.id)


def end_alphabet_game(user_id, chat_id):
    game = games[user_id]
    correct = game["correct"]

    streak = game["streak"]

    if streak > highscores.get(user_id, {}).get(game["game_name"], 0):
        update_highscore(game_name=game["game_name"], user_id=user_id, value=streak)
        msg_body = f"🎉 New highscore of <b>{streak}!</b> Congratulations! 🎉"
    else:
        msg_body = f"Final streak: <b>{streak}</b>"

    bot.edit_message_text(
            f"💀 Game Over!\n\n{msg_body}\nCorrect answer was: {safe(encode_message(correct))} = {safe(correct)}\n\n<i>Play again? y/n</i>",
            chat_id,
            game["msg_id"],
            parse_mode="html"
        )
    del games[user_id]
    previous_game[user_id] = game["game_name"]

#endregion


#region FOOD NOT FOOD game code

def format_food_message(word, score, time_remaining):
    highlighted_word = f"<b>{safe(word)}</b>"
    message_text = (
        f"🏆  <i>Score: {score}</i>     ⏰ <i>Time: {time_remaining}s</i>\n"
        f"──────────────\n"
        f"              {highlighted_word}\n"
        f"──────────────"
    )
    return message_text

def start_foodnotfood_game(chat_id, user_id):
    msg_id = bot.send_message(chat_id, "Loading game...").id

    time.sleep(0.3)

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🍎 Food", callback_data="food")
    btn2 = types.InlineKeyboardButton("❌ Not Food", callback_data="notfood")
    markup.row(btn1, btn2)

    games[user_id] = {
        "game_name": "Food/notFood",
        "score": 0,
        "time_left": GAME_DURATION,
        "msg_id": msg_id,
        "markup": markup,
    }

    bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg_id, reply_markup=markup)

    send_new_round(chat_id, user_id)

    # Start background timer updater
    timer_thread = threading.Thread(target=update_timer_loop, args=(chat_id, user_id), daemon=True)
    timer_thread.start()

# Background thread to update timer every second in the last message.
def update_timer_loop(chat_id, user_id):
    while user_id in games:
        game = games[user_id]

        if game.get("processing"):
            delay = 0.1 if bot.get_chat(chat_id).type == "private" else 0.4
            time.sleep(delay)
            continue

        remaining = game["time_left"]

        if remaining <= 0:
            end_foodnotfood_game(chat_id, user_id)
            break

        if bot.get_chat(chat_id=chat_id).type == "private" and "msg_id" in game: # if not in private, then no update text
            try:
                bot.edit_message_text(
                    format_food_message(game["current_word"], game["score"], remaining),
                    chat_id=chat_id,
                    message_id=game["msg_id"],
                    parse_mode="HTML",
                    reply_markup=game["markup"]
                )
            except:
                pass  # ignore errors like message deleted

        game["time_left"] -= 1 # decrementing time
        time.sleep(1)



def send_new_round(chat_id, user_id):
    if user_id not in games:
        return  # game ended

    game = games[user_id]

    is_food = random.choice([True, False])

    words = food_words if is_food else not_food_words

    new_word = random.choice(words)
    while new_word == game.get("current_word", ""):
        new_word = random.choice(words)

    new_word = encode_message(new_word)

    game["current_word"] = new_word
    game["is_food"] = is_food

    bot.edit_message_text(format_food_message(new_word, game["score"], game["time_left"]), chat_id, game["msg_id"], parse_mode="html", reply_markup=game["markup"])

@bot.callback_query_handler(func=lambda call: call.data in ["food", "notfood"])
def handle_food_game(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if user_id not in games:
        return

    game = games[user_id]
    if game["game_name"] != "Food/notFood":
        return
    
    game["processing"] = True


    correct = (
        (call.data == "food" and game["is_food"]) or
        (call.data == "notfood" and not game["is_food"])
    )

    if correct:
        game["score"] += 1
        send_new_round(chat_id, user_id)        
    else:
        end_foodnotfood_game(chat_id, user_id)

    game["processing"] = False

def end_foodnotfood_game(chat_id, user_id):
    if user_id not in games:
        return

    game = games[user_id]
    game["processing"] = True
    score = game["score"]

    if game["time_left"] <= 0:
        msg_upper = f"⏰ Time's up!"
    else:
        word = decode_message(game["current_word"])
        if game["is_food"]:
            msg_upper = f"❌ WRONG! {word} <b>IS</b> food!"
        else:
            msg_upper = f"❌ WRONG! {word} <b>IS NOT</b> food!"

    
    if score > highscores.get(user_id, {}).get(game["game_name"], 0):
        update_highscore(game["game_name"], user_id, score)
        msg_body = f"🎉 New highscore of <b>{score}!</b> Congratulations! 🎉"
    else:
        msg_body = f"Final score: <b>{score}</b>"

    del games[user_id]
    
    previous_game[user_id] = game["game_name"]
    bot.edit_message_text(chat_id=chat_id, message_id=game["msg_id"], text=f"{msg_upper}\n──────────────\n{msg_body}\n──────────────\n <i>Play again? y/n</i>", parse_mode="html")
#endregion

#region GAMES main

@bot.message_handler(commands=['play'])
def play_menu(message):
    # if message.chat.type != "private":
    #     bot.send_message(message.chat.id, "Sorry! Only in private")
    #     return
    
    user_id = message.from_user.id
    if user_id in games:
        del games[user_id]

    if user_id not in highscores:
        highscores[user_id] = {}
    
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("Алфавит", callback_data="game_alphabet")
    btn2 = types.InlineKeyboardButton("Съедобное/несъедобное", callback_data="game_foodnotfood")
    btn3 = types.InlineKeyboardButton("Wordle", callback_data="game_game_wordle")

    markup.add(btn1)
    markup.add(btn2)
    # markup.add(btn3)

    bot.send_message(
        message.chat.id,
        "🎮 Choose a game:",
        reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("game_"))
def callback_handler(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == "game_foodnotfood":
        bot.send_message(call.message.chat.id, "Давай играть в Съедобное/несъедобное!")
        start_foodnotfood_game(chat_id=call.message.chat.id, user_id=call.from_user.id)

    elif call.data == "game_alphabet":
        bot.send_message(call.message.chat.id, "Давай выучим Алфавит!")
        start_alphabet_game(chat_id=call.message.chat.id, user_id=call.from_user.id)

    elif call.data == "game_wordle":
        bot.send_message(call.message.chat.id, "Давай играть в Wordle!")
        games[call.from_user.id] = {
            "game": "wordle",
            "time": 60,
            }
    
#endregion


@bot.message_handler(content_types=['text'])
def check_message(message):

    if previous_game.get(message.from_user.id):   # catching if you wanna play again
        if message.text.lower() in ["y", "1", "yes", "да"]:
            match previous_game[message.from_user.id]:
                case "Food/notFood":
                    start_foodnotfood_game(message.chat.id, message.from_user.id)
                case "Alphabet":
                    start_alphabet_game(chat_id=message.chat.id, user_id=message.from_user.id)
        else:
            previous_game[message.from_user.id] = None


    if not message.chat.type in ["group", "supergroup"] and contains_russian(message.text):
        if settings["force_translate"]:
            translated_message = encode_message(message.text)
            bot.send_message(message.chat.id, f"Ds [jntkb crfpfnm: \n {translated_message}?")
        bot.send_message(message.chat.id, "THIS IS A PRIVATE CHAT, I CANT DO <i><b>SHIT</b></i>!", parse_mode="html")
        return
    
    if settings["no_russian"] and contains_russian(message.text):
        bot.delete_message(message.chat.id, message.message_id)

        if settings["force_translate"]:
            translated_message = encode_message(message.text)
            name = message.from_user.first_name
            bot.send_message(message.chat.id, f"""<i>{name}:</i>\n{(translated_message)}""", parse_mode="html")
        else: 
            reply_message = "[NO RUSSIAN ALLOWED]"
            sent = bot.send_message(message.chat.id, reply_message)
            threading.Thread(
                target=delete_later,
                args=(sent.chat.id, sent.message_id, 3)).start()


    if settings["translate_when_asked"] and message.reply_to_message and message.text in ["?", "??", "???", "what", "huh", "bruh"]:  # if this message is a reply to something else
        original_text = message.reply_to_message.text
        # if contains_russian(original_text): 
        #     sent1 = bot.reply_to(message, f"Там уже на русском, ты тупой?")
        #     threading.Thread(
        #         target=delete_later,
        #         args=(sent1.chat.id, sent1.message_id, 4)).start()
        #     return # dont translate if its already in russian

        if message.reply_to_message.from_user.id == BOT_ID:
            cleaned_text = remove_first_line(original_text)
        else: cleaned_text = original_text

        translated_text = cleaned_text.translate(eng_to_rus)
        sent = bot.reply_to(message.reply_to_message, f"<i>Перевод:</i> {safe(translated_text)}", parse_mode="html")
        threading.Thread(
                target=delete_later,
                args=(sent.chat.id, sent.message_id, 5)).start()
        threading.Thread(
                target=delete_later,
                args=(message.chat.id, message.message_id, 5)).start()



bot.polling(none_stop=True)
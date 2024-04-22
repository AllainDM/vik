import sqlite3
from datetime import datetime
import pickle
import json
import os

from flask import Flask, render_template, request, flash, g, redirect, url_for, jsonify
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, current_user, login_user, LoginManager, logout_user
import redis

import maindb
# TODO файл БД еще не создан
import config
import mod
import world
from FDataBase import FDataBase
from world import FirstWorld
from province import Province
from UserLogin import UserLogin
from cities import Cities
from goods import Goods
from buildings import Buildings
from dynasty import Dynasty

# import postgreTables


Debug = True
SECRET_KEY = config.SECRET_KEY

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Необходимо авторизоваться"
login_manager.login_message_category = 'error'

# Настройка Redis для хранения глобальной переменной Game
rediska = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    # password='qwerty',
    charset="utf-8",
    decode_responses=True
)

print(rediska)

menu = [{"name": "Авторизация", "url": "login"},
        {"name": "Feedback", "url": "contact"}]

menu_auth = [
    {"name": "Профиль", "url": "profile"},
    {"name": "Игра", "url": "game"},
    {"name": "Выбор игры", "url": "choose-game"},
    {"name": "Игроки", "url": "players"},
    {"name": "Лог", "url": "log"},
    # {"name": "Feedback", "url": "contact"}
]

menu_admin = [
    {"name": "Профиль", "url": "profile"},
    {"name": "Игры", "url": "games"},
    {"name": "Создать игру", "url": "create-game"},
    {"name": "Игроки", "url": "players"},
    {"name": "Лог", "url": "log"},
    # {"name": "Feedback", "url": "contact"}
]

# menu_party = [
#
# ]

# Временный глобальный список поселений, будет использоваться для быстрого создания партии
# Так же создадим запас названий для других поселений с простыми названиями
# Временно, условно отделяю названия поселений игроков от названия ИИ поселений.
# Дания = "Ольборг", "Орхус", "Хедебю", "Рибе", "Эсбьерг"
manual_settlements_names_rus = ["Хедебю", "Ольборг", "Орхус", "Рибе", "Эсбьерг", ]
auto_settlements_names_rus = [f"Settlement_{s}" for s in range(1000)]
# settlements_names_rus = manual_settlements_names_rus + auto_settlements_names_rus
settlements_names_rus = auto_settlements_names_rus

manual_settlements_names_eng = ["Hedeby", "Aalborg", "Aarhus", "Ribe", "Esbjerg"]
auto_settlements_names_eng = [f"Settlement_{s}" for s in range(1000)]
# settlements_names_eng = manual_settlements_names_eng + auto_settlements_names_eng
settlements_names_eng = auto_settlements_names_eng

# Временный глобальный список провинций, будет использоваться для быстрого создания партии
# Так же создадим запас названий для других провинций с простыми названиями
manual_provinces_names_rus = ["Хедебюгия", "Ольборгия", "Орхусия", "Рибения", "Эсбьергия", ]
auto_provinces_names_rus = [f"Provinces_{s}" for s in range(100)]
# provinces_names_rus = manual_provinces_names_rus + auto_provinces_names_rus
provinces_names_rus = auto_provinces_names_rus

manual_provinces_names_eng = ["Hedebys", "Aalborgs", "Aarhuss", "Ribes", "Esbjergs"]
auto_provinces_names_eng = [f"Provinces_{s}" for s in range(100)]
# provinces_names_eng = manual_provinces_names_eng + auto_provinces_names_eng
provinces_names_eng = auto_provinces_names_eng


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        # print("Соединение не было создано")
    # print("Соединение не было создано и мы его создали")
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    # Закрываем соединение с БД, если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None


@app.before_request
def before_request():
    # Database connection, before query
    global dbase
    db = maindb.get_db()
    dbase = FDataBase(db)


@login_manager.user_loader
def load_user(user_id):
    # print(f"Load user. ID: {user_id}")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    connect = psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )
    return connect


@app.route("/")
@app.route("/main")
@login_required
def index():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("index.html", title="Main", menu=menu_admin)
    return render_template('index.html', title="Main", menu=menu_auth)


# TODO Что это за функция??????????????
@app.route("/create-game")
@login_required
def admin_create_new_game():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin2")
        return render_template("create-game.html", title="Main", menu=menu_admin)
    return render_template('index.html', title="Main", menu=menu_auth)


@app.route("/game")  # Функция перенаправляет игрока на страницу смой игры, откуда уже происходит запрос параметров
@login_required
def play():
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    player = int(current_user.get_id())
    if user_admin == 1:
        # Интересно, что открывается game-admin.html, но путь в адресной строке висит как "game"
        return render_template("game-admin.html", title=user_name, menu=menu_admin)
    else:
        # Извлекаем активную игру из Редиски
        # active_game = rediska.get(f'playerID_{player}_active_gameID')
        my_game_arr = dbase.get_all_active_games()
        if len(my_game_arr) == 0:
            return render_template("choose-game.html", title=user_name, menu=menu_auth)
        # if active_game == 0:
        #     return render_template("new-game.html", title=user_name, menu=menu_auth)
        else:
            return render_template("game.html", title=user_name, menu=menu_auth)


@app.route("/choose-game")  # Перенаправление на страничку выбора "активно" игры
@login_required
def choose_game_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("choose-game.html", title=user_name, menu=menu_admin)
    else:
        return render_template("choose-game.html", title=user_name, menu=menu_auth)


@app.route("/games")  # Перенаправление на страничку со списком всех игр. ТОЛЬКО ДЛЯ АДМИНА
@login_required
def all_games_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("games.html", title=user_name, menu=menu_admin)
    else:
        return render_template("game.html", title=user_name, menu=menu_auth)


# Страничка с логом изменений, а так же планом
@app.route("/log")
@login_required
def log():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("log.html", title="Main", menu=menu_admin)
    return render_template('log.html', title="Main", menu=menu_auth)


@app.route("/load_all_games")  # Посмотреть список все игр с возможностью их удаления. ТОЛЬКО ДЛЯ АДМИНА
@login_required
def load_all_games():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    # global game_arr
    # Прочитаем файл со списком игр
    game_arr = dbase.get_all_active_games()
    # Выше мы получили кортеж с данными страны, под 5 индексом список ИД игроков
    # Нужно перебрать список ИД игроков и вынести имена игроков
    print(f"game_arr: {game_arr}")
    games_list = []  # Это список игр для отправки админу
    # players_list = []  # Это список игр для отправки админу
    for game in game_arr:
        games_list.append(game[0])
    return jsonify(games_list)


@app.route("/load_all_new_games")  # Посмотреть список все игр к которым можно присоединиться
@login_required
def load_all_new_games():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    # Получим ид игрока, выборка должна быть где игрок не участвует
    player_id = int(current_user.get_id())
    # Прочитаем файл со списком игр
    game_arr = dbase.get_all_not_full_games(player_id)  # Список игр, где еще есть места
    # Выше мы получили кортеж с данными страны, под 5 индексом список ИД игроков
    # Нужно перебрать список ИД игроков и вынести имена игроков
    print(f"Список новых игр: {game_arr}")
    games_list = []  # Это список игр для отправки админу game_arr,
    # players_list = []  # Это список игр для отправки админу
    for game in game_arr:
        if player_id in game[5]:  # Если игрок уже есть в партии она не выводится
            continue
        else:
            pls_in_game = []
            for pl in game[5]:
                pls_in_game.append(dbase.get_user(pl)[3])
            game_and_players = [game, pls_in_game]
            games_list.append(game_and_players)
    return jsonify(games_list)


@app.route("/add_player_to_game")  # Посмотреть список все игр к которым можно присоединиться
@login_required
def add_player_to_game():
    game_id = int(request.args.get('id'))
    player_id = int(current_user.get_id())
    player_info = dbase.get_user(player_id)  # TODO тут возврат всей записи о пользователе?
    print(f"player_info: {player_info}")
    dbase.add_player(game_id, player_id)
    add_dynasty(game_id, player_info)
    return "ok"


@app.route("/delete_game")  # Удалить игру (сделать неактивной)
@login_required
def delete_game():
    user_admin = current_user.get_admin()
    game_id = int(request.args.get('id'))
    if user_admin == 1:
        # list_games = dbase.get_all_games()  # Запросим список игр для теста
        # print(f"list_games: {list_games}")
        dbase.delete_game(game_id)  # Удалим из БД выбранную игру
        # list_games = dbase.get_all_games()  # Запросим список игр для теста
        # print(f"list_games: {list_games}")
    return ""


@app.route("/load_all_my_game")  # Посмотреть список всех игр для игрока
@login_required
def load_all_my_game():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    # global game_arr
    # Прочитаем список игр из БД
    game_arr = dbase.get_all_active_games()
    player = int(current_user.get_id())
    games_list = []  # Это список игр для отправки игроку для выбора
    print(f"Список моих игр: {game_arr}")
    for my_g in game_arr:
        if player in my_g[5]:
            pl_in_game = []
            for pl in my_g[5]:
                pl_in_game.append(dbase.get_user(pl)[3])
            # print(f"Игрок есть в игре номер: {my_g[0]}")
            # Аналог двух append
            one_game = [my_g[0], pl_in_game]
            # games_list.append(f"{my_g[0]} Игроки: {pl_in_game}")
            games_list.append(one_game)
    return jsonify(games_list)


@app.route("/set_active_game")  # Выбор "активной" игры для пользователя, параметры которой будут загружаться
@login_required
def set_active_games():
    game_id = request.args.get('id')
    active_game = int(game_id)
    player = int(current_user.get_id())
    user_name = current_user.get_name()
    # Теперь сохраняем в редиску, можно так и оставить, если будет норм работать
    rediska.set(f"playerID_{player}_active_gameID", active_game)
    print(f"Игрок {user_name} сделал активной игру номер: {active_game}")
    return ""


@app.route("/players")  # Отображение странички со всеми зарегистрированными игроками
@login_required
def players_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("players.html", title=user_name, menu=menu_admin)
    else:
        return render_template("players.html", title=user_name, menu=menu_auth)


@app.route("/req_list_players")  # Отображение всех зарегистрированных игроков
@login_required
def req_list_players():
    # Поиск игрока по участию в игре. В БД у пользователей планируется запись со списком игр с участием этого игрока
    # Проверка или в тексте запроса к БД. Тут нужен доп аргумент в виде ИД игры
    # Или проверка тут, через цикл по списку каждого пользователя.
    # Подходящие уже тогда добавляются на отправки на фронт
    # who = request.args.get('who')
    list_users_to_front = []
    users = dbase.get_all_user()
    # print(f"users: {users}")
    # games = dbase.get_all_active_games()
    # print(f"games: {games}")
    for user in users:
        # Возвращаем имя пользователя(не логин) и ИД пользователя(для админа)
        # Так же добавим количество побед [5], Имя династии под игрока [6]
        list_users_to_front.append([user[0], user[3], user[5], user[6]])
    return jsonify(list_users_to_front)


@app.route("/req_cities_for_trade")  # Запрос списка городов для торговли
@login_required
def req_cities_for_trade():
    pass


# Создать каждому по одиночной игре
# @app.route("/create_new_single_game")
# @login_required
# def create_new_single_game():
#     user_admin = current_user.get_admin()
#     if user_admin == 1:
#         print("this is admin4")
#         users = dbase.get_all_user()
#         # print(f"users: {users}")
#         for user in users:
#             # print(f"user {user[0]}")
#             player = int(user[0])
#             # [{'playerId': 3, 'nameEng': 'Magonid', 'nameRus': 'Магониды'}]
#             players_dynasty = [{'playerId': player, 'nameEng': 'Magonid', 'nameRus': 'Магониды'}]
#             # print(players_dynasty)
#             create_game(players_dynasty)
#         return jsonify("Ответ от Python: Игра создалась")
#     else:
#         return ""


# Админская версия создания партии
@app.route("/create_new_game_admin", methods=["POST"])  # Создать настроенную игру получив параметры с фронта
@login_required
def create_new_game_admin():
    # Создать вариант, где пользователь не админ, что перекидывало куда-нибудь в другое место
    if request.method == "POST":
        # global game_arr  # Зачем?
        user_admin = current_user.get_admin()
        if user_admin == 1:
            print("this is admin")
            post = request.get_json()
            print(f"post: {post}")
            info_to_front = create_game(post)
            print(f"Ответ от Python: Игра создалась")
            # return jsonify("Ответ от Python: Игра создалась")
            return jsonify(info_to_front)
    else:
        return ""


@app.route("/create_new_game", methods=["POST"])  # Создать настроенную игру получив параметры с фронта
@login_required
def create_new_game():
    if request.method == "POST":
        # Соберем инфу о пользоветеле создавшем игру, его данные будут записаны под первой страной
        player_id = int(current_user.get_id())
        player_info = dbase.get_user(player_id)
        post = request.get_json()
        print(f"post: {post}")
        print(f"player_info: {player_info}")
        # Передаем макс количество игроков и параметры первого игрока, остальные добавляются потом
        setting_for_create_game = [
            {"maxPlayers": post["maxPlayers"]},  # post[0]
            {"playerId": player_info[0], "nameEng": player_info[6], "nameRus": player_info[6]}
        ]
        print(f"setting_for_create_game {setting_for_create_game}")
        info_to_front = create_game(setting_for_create_game)
        print(f"Ответ от Python: Игра создалась")
        return jsonify(info_to_front)
    else:
        return ""


def create_game(setting):  # Получаем только список игроков
    # !!!!!!!!!!!!! Новый функционал создания партии
    # TODO удалить старый код после проверки

    """
    Создание партии.\n
    1. Определение текущей даты.
    2. Вычисление id партии, через запрос к БД.
    3. Создание папок для сохранения файлов игры.
    4. Создание экземпляра игры.
    5. Создание первой провинции для первых поселений.
    6. Создание поселения игрока.
    7. Создание ИИ поселений.
    8. Сохранение списка провинций и самого файла провинции.
    9. Сохранение игры в файл.

    """

    # 1. Определение текущей даты.
    date_now = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты

    # 2. Вычисление id партии, через запрос к БД.
    # print("Добавляем игру в БД")
    # Делаем стартовую запись в БД. В списке игроков только создавший партию
    # Номер хода, Стартовый год, ид первого игрока, тек. количество игроков, макс. количество игроков
    # setting можно посмотреть в функции выше
    last_game_row_id = dbase.add_game(1, 800, [setting[1]["playerId"]], 1, setting[0]["maxPlayers"])
    # print("Тестим добавление в игру юнита.")
    # # id_for_new_unit = dbase.add_unit(1, "name1")
    # print("Конец теста.")
    # 3. Создание папок для сохранения файлов игры.
    # Создадим папки игры для сохранений
    if not os.path.exists(f"games"):
        os.makedirs(f"games")
    if not os.path.exists(f"games/{last_game_row_id}"):
        os.makedirs(f"games/{last_game_row_id}")
    if not os.path.exists(f"games/{last_game_row_id}/acts"):
        os.makedirs(f"games/{last_game_row_id}/acts")

    # 4. Создание экземпляра игры.
    # Создадим экземпляр игры, а так же поселения и династии для первого игрока.
    this_game = FirstWorld(last_game_row_id, date_now, setting[0]["maxPlayers"])

    # 5. Создание первой провинции для первых поселений.
    # Создадим провинцию для первых поселений
    new_province_id = 0
    new_province = this_game.create_province(last_game_row_id, new_province_id,
                                             provinces_names_rus[0], provinces_names_eng[0])

    # 6. Создание поселения игрока.
    # TODO Имя поселения временно первое из списка.
    # Запишем в БД, получим row_id, его используем при сохранении поселения в файл.
    player_settlement_id = dbase.add_settlement(last_game_row_id, settlements_names_eng[0],
                                                settlements_names_rus[0], setting[1]["playerId"])
    # Нет === Ид поселение теперь берется по количеству поселений из списка в конкретно этой игре
    # Нет === В данной функции нет смысла вычислять ид, он всегда 0
    # real_settlement_id = len(this_game.settlements_list)  # Старое
    # print(f"Реальный ид поселения {real_settlement_id}")  # Старое
    # id игры
    # id поселения(получаем выше из бд)
    # ссылка на провинцию
    # id игрока владельца
    # имя поселения на английском
    # имя поселения на русском
    # игрок на поселении
    list_settlements_in_province = {}  # Список поселений в провинции
    this_game.create_settlement(dbase, last_game_row_id, new_province, player_settlement_id,
                                setting[1]["playerId"],
                                manual_settlements_names_rus[0],
                                manual_settlements_names_eng[0], player=True)
    # list_settlements_in_province.append(settlements_names_eng[0])
    # Был список названий, создаем словарь. Ключ ид, значение название
    list_settlements_in_province[player_settlement_id] = manual_settlements_names_eng[0]
    # Так же добавим в список
    new_province.list_settlements.append(manual_settlements_names_eng[0])
    # Так же передадим ид только что созданного поселения
    this_game.create_dynasty(last_game_row_id, setting[1]["playerId"],
                             setting[1]["nameEng"], setting[1]["nameRus"],
                             player_settlement_id, new_province_id, 100)

    # 7. Создание ИИ поселений.
    # Создадим еще поселения в провинции игрока
    # TODO выяснить верно ли присваивается ид для поселения
    # Цикл по количеству базовых поселений в провинции, сохраняется как модификатор
    for sett in range(1, mod.SETT_IN_PROVINCE + 1):
        print("############################################")
        # real_settlement_id = len(this_game.settlements_list)  # Старое
        # print(f"Реальный ид поселения {real_settlement_id}")  # Старое
        # print(f"Создаем поселение с ид: {last_settlement_row_id + 1}")
        # last_settlement_row_id = dbase.add_settlement(last_game_row_id, f"settlements_{last_settlement_row_id + 1}",
        #                                               f"settlements_{last_settlement_row_id + 1}", 0)
        # TODO отключаю добавление в БД, пока не используется
        settlement_row_id = dbase.add_settlement(last_game_row_id, f"settlements_{player_settlement_id+sett}",
                                                 f"settlements_{player_settlement_id+sett}", 0)
        this_game.create_settlement(dbase, last_game_row_id, new_province, settlement_row_id, 0,
                                    f"settlements_{settlement_row_id}",
                                    f"settlements_{settlement_row_id}", player=False)
        print(f"Создано поселение с ид: {settlement_row_id}")
        # Добавим в список поселений, необходимо для восстановлений
        # list_settlements_in_province.append(f"settlements_{real_settlement_id}")
        # Создаем словарь, ключ ид, значение название.
        # TODO В данный момент все ИИ поселения имею базовое название + ид
        list_settlements_in_province[settlement_row_id] = f"settlements_{settlement_row_id}"
        # Так же добавим в список
        new_province.list_settlements.append(f"settlements_{settlement_row_id}")

    # 8. Сохранение списка провинций и самого файла провинции.
    # Сохраним список поселений в экземпляре класса провинции.
    print(f"Список добавляемых поселений в провинцию: {list_settlements_in_province}")
    new_province.dict_settlements = list_settlements_in_province  # Словарь
    print(f"Список добавляемых поселений в провинцию: {new_province.dict_settlements}")
    new_province.save_to_file()

    # Нет необходимости после полного переноса юнитов в БД.
    # Посчитаем стартовых юнитов по поселениям.
    # Необходимо распределить юнитов группами по игрокам
    # print(f"При создании игры, после создания всех поселений запускаем функцию поиска юнитов.")
    # for i in this_game.dynasty:
    #     this_game.dynasty[i].search_our_units()
    #     this_game.dynasty[i].save_to_file()

    # 9. Сохранение игры в файл.
    this_game.save_to_file()

    print("Игра создана")
    print(this_game.dynasty_list)
    return f"Game create {setting[1]}"


# Присоединение к игре.
def add_dynasty(game_id, player):
    """
    Добавление нового игрока в партию.
    1. Создать экземпляр класса мир и загрузить данные из файла по id партии.
    2. Создать новую провинцию под игрока.
    3. Создать поселение игроку.
    4. Создать Династию игроку.
    5. Создать остальные поселения в новой провинции.
    6. Создать пустую армию.
    """
    print("Добавление нового игрока.")
    # Пункт 1. Создать экземпляр класса мир и загрузить данные из файла по id партии.
    game = FirstWorld(game_id)  # Восстановим саму игру.
    game.load_from_file(game_id)  # Запустим метод считающий данные из файла.

    # Пункт 2. Создать новую провинцию под игрока.
    new_province_id = len(game.provinces_list)
    print(f"Ид новой провинции: {new_province_id}")
    new_province = game.create_province(game_id=game_id, row_id=new_province_id,
                                        name_rus=provinces_names_rus[new_province_id],
                                        name_eng=provinces_names_eng[new_province_id])

    # Пункт 3. Создать поселение игроку.
    list_settlements_in_province = {}  # Список поселений в провинции. Словарь?

    # Ид поселение теперь берется по количеству поселений из списка в конкретно этой игре.
    real_settlement_id = len(game.settlements_list)
    print(f"Реальный ид поселения {real_settlement_id}")
    # Имя поселения берем из прописного списка индексом по ид провинции.
    game.create_settlement(dbase, game_id=game_id, province=new_province,
                           row_id=real_settlement_id, ruler=player[0],
                           name_rus=manual_settlements_names_rus[new_province_id],
                           name_eng=manual_settlements_names_eng[new_province_id],
                           player=True)

    # Добавляем в словарь. Ключ ид, значение название.
    list_settlements_in_province[real_settlement_id] = manual_settlements_names_eng[new_province_id]
    # Так же добавим в список
    new_province.list_settlements.append(manual_settlements_names_eng[new_province_id])

    # Старый код добавления поселения в БД. Не удалять.
    # Добавим запись о поселении для игрока в БД заодно получив его row_id для сохранения.
    # last_settlement_row_id = dbase.add_settlement(game_id=game_id, name_eng=settlements_names_eng[0],
    #                                               name_rus=settlements_names_rus[0], ruler=player[0])

    # Пункт 4. Создать Династию игроку.
    # Последний аргумент количество золота, у него есть дефолтное значение.
    game.create_dynasty(game_id, player_id=player[0],
                        name_eng=player[6], name_rus=player[6],
                        main_settlement=real_settlement_id,
                        province_id=new_province_id)

    # Пункт 5. Создать остальные поселения в новой провинции.
    for sett in range(mod.SETT_IN_PROVINCE):
        # print("############################################")
        real_settlement_id = len(game.settlements_list)
        # print(f"Ид нового ИИ поселения {real_settlement_id}")
        # Старый код добавления поселения в БД. Не удалять.
        # last_settlement_row_id = dbase.add_settlement(game_id, f"settlements_{real_settlement_id}",
        #                                               f"settlements_{real_settlement_id}", 0)
        game.create_settlement(dbase, game_id=game_id, province=new_province,
                               row_id=real_settlement_id, ruler=0,
                               name_rus=f"settlements_{real_settlement_id}",
                               name_eng=f"settlements_{real_settlement_id}",
                               player=False)
        print(f"Создано поселение с ид: {real_settlement_id}")
        # Добавляем в словарь. Ключ ид, значение название.
        list_settlements_in_province[real_settlement_id] = settlements_names_eng[real_settlement_id]
        # Добавим так же и в список поселений в записи провинции
        new_province.list_settlements.append(settlements_names_eng[real_settlement_id])

    # Пункт 6. Создание армии, пустой.

    # Обновим словарь с поселениями в классе провинции.
    new_province.dict_settlements = list_settlements_in_province  # Словарь

    # Сохраним новые данные
    new_province.save_to_file()
    game.save_to_file()


# !!!!!!!!!! Отменять надо у Активной игры. Или нет?
@app.route("/cancel_act")  # Отменить акт(действие). Все или последний. !!! Доработать возможность выбора любого
def cancel_act():
    what = request.args.get('what')
    # response = dbase.read_router_comment(id_router)
    player = int(current_user.get_id())
    # Получим ИД партии !!!!!!!!!!!! Обязательно проверку
    game_id = request.args.get('gameId')
    try:  # Блок на случай отсутствия файла
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'r') as f:
            data = json.load(f)
            if what == "all":
                data["acts"] = []
            elif what == "last":
                data["acts"].pop(-1)
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'w') as new_f:
                json.dump(data, new_f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
        return "ok"
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.viking' не найден")
        return ""


# Отображение в меню дипломатии всех игроков с основными параметрами(золото, имя, готовность хода)
@app.route("/req_status_all_player", methods=["GET"])
@login_required
def req_status_all_player():
    game_id = request.args.get('gameId')
    return_data = []
    try:
        with open(f"games/{game_id}/gameID_{game_id}.viking", 'r') as f:
            data_players = json.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}.viking' не найден")
        return ""
    for player_id in data_players["player_list"]:
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player_id}.viking", 'r') as f:
                data_one_player = json.load(f)
                one_player = {
                    "name_rus": data_one_player["name_rus"],
                    "gold": data_one_player["gold"],
                    # "donate_sum": data_one_player["donate_sum"],
                    # "title": data_one_player["title"],
                    "end_turn": data_one_player["end_turn"],
                    "win_points": data_one_player["win_points"],
                    # "body_points": data_one_player["body_points"],
                }
                return_data.append(one_player)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player_id}.viking' не найден")
            return ""
    return jsonify(return_data)


# Запрос всех параметров нашего игрока
@app.route("/req_status_game_player", methods=["GET"])  # Запрос параметров страны игрока
@login_required
def req_status_game_player():
    player = int(current_user.get_id())
    game_id = rediska.get(f'playerID_{player}_active_gameID')
    # Выходит что нам не нужно обращаться к классу Династии запуская ее метод
    try:
        # Запросим династию игрока
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'r') as f:
            data_dynasty = json.load(f)
            # print(f"1Информация о династии {data_dynasty}")
        # Вариант с выводом всех поселений нашей провинции
        # list_settlements =
        # Определим нашу провинцию, она хранится в записи династии
        with open(f"games/{game_id}/gameID_{game_id}_provinceID_{data_dynasty['main_province']}.viking", 'r') as f:
            data_province = json.load(f)
            print(f'Выведем инфу о нашей провинции: {data_province}')
            dict_settlements = data_province["dict_settlements"]
            print(f'Выведем инфу о нашей провинции: {dict_settlements}')
            data_settlements = []
            for i in dict_settlements:
                with open(f"games/{game_id}/gameID_{game_id}_settlementID_{i}.viking", 'r') as f:
                    data_settlement = json.load(f)
                    data_settlements.append(data_settlement)

        print(f'Запросим инфу о юнитах для отправки на фронт')
        print(data_dynasty)

        # Необходимо новое подключение, ибо в 20% случаев выдает ошибку, что курсор закрыт.
        db = maindb.get_db()
        dbase2 = FDataBase(db)
        units = dbase2.get_all_our_units(data_dynasty["our_settlements"])

        # # TODO Внимание костыль
        # for i in range(15):
        #     print(f"Попытка номер: {i+1}")
        #     units = dbase2.get_all_our_units(data_dynasty["our_settlements"])
        #     if units:
        #         break

        # Юниты берем из БД. Для начала возьмем в записи игрока его поселения.
        list_our_settlements = data_dynasty["our_settlements"]
        # TODO реализовать на фронте вариант при котором у игрока нет поселения
        # TODO Возможно просто возвращая специальное пустое поселение с ид 0
        # else:  # Если у игрока нет поселения
        #     data_settlement = []
        all_data = [data_dynasty, data_settlements, units]
        # print(f"3Информация об игроке и поселении {all_data}")
        return jsonify(all_data)
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.viking' не найден 1")
        return ""


@app.route("/req_status_game", methods=["GET"])  # Запрос общих параметров партии
@login_required
def req_status_game():
    player = int(current_user.get_id())
    user_name = current_user.get_name()
    game_id = rediska.get(f'playerID_{player}_active_gameID')
    # print(f"ИД игры при запросе статуса династии: {game_id}")
    # TODO !!!!!!!!! Тут еще нужна проверка на существование самой партии
    try:
        with open(f"games/{game_id}/gameID_{game_id}.viking", 'r') as f:
            my_world = json.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}.viking' не найден")
        return ""
    print(f"Моя игра, информация о классе World: {my_world}")
    # Так же загрузим список городов для торговли

    data = {
        # Об игроках
        "max_players": my_world["max_players"],
        "dynasty_list": my_world["dynasty_list"],
        "winners": my_world["winners"],  # need_win_points_for_win
        "need_win_points_for_win": my_world["need_win_points_for_win"],
        "year": my_world["year"],
        "turn": my_world["turn"],
        "all_logs": my_world["all_logs"],
        "all_logs_party": my_world["all_logs_party"],
        "game_id": my_world["row_id"],
        "date_create": my_world["date_create"],
        "user_name": user_name,
    }
    print(f"4Информация о партии {data}")
    return jsonify(data)


# Чат
@app.route("/post_chat", methods=["POST"])  # Внутриигровой чат. TODO !!! не доделан
@login_required
def post_chat():
    if request.method == "POST":
        # print('Запрос с js')
        # Определим игрока, чтоб понять от кого получен запрос
        player_id = int(current_user.get_id())
        player_info = dbase.get_user(player_id)
        date_now = datetime.strftime(datetime.now(), "%H:%M:%S")  # Дата: часы, минуты, секунды
        post = request.get_json()
        chat_redis = rediska.get("chat")
        # chat_redis.append("nsadaf")
        # TODO проверка на пустое сообщение, возможно еще на фронте сделать
        mes = f"\n{player_info[3]} {date_now}: {post}"
        chat_redis += mes
        rediska.set("chat", chat_redis)
        print(chat_redis)
        print(type(chat_redis))
        return jsonify(chat_redis)


# !!!!!!!!!!!!! Запустить функцию подсчета хода
@app.route("/post_turn", methods=["POST"])  # Подтверждение готовности хода
@login_required
def post_turn():
    if request.method == "POST":
        # print('Запрос с js')
        # Определим игрока, чтоб понять от кого получен ход и куда его записать
        player = int(current_user.get_id())
        # Получим ИД партии, ей будем присваивать ход !!!!!!!!!!!! после проверки
        # !!!!!!!!! Нужна проверка участвует ли игрок в этой игре!!!!!!!!!!!!!!!!!!!!!!!!!!
        game_id = request.args.get('gameID')
        # print(f"ИД партии которой передается ход: {game_id}")
        # Получаем список с действиями игрока
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.viking' не найден")
            return ""
        # Присвоим ход игроку
        data["end_turn"] = True
        # Снова запишем ход
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'w') as f:
            json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
        world.check_readiness(game_id)
    # Временно возвращаем пустую строку
    return ""


@app.route("/post_act", methods=["POST"])  # Отправка одного акта(действия) игрока
@login_required
def post_act():
    """
        Отдельная функция получения одного действия.
        Необходима для отображения актуального списка действий,
        который не будет пропадать и сбиваться при обновлении странички.
        Ход при этом не считается отправленным.
    """
    if request.method == "POST":
        # print('Запрос с js')
        # Определим игрока, чтоб понять от кого получен ход и куда его записать
        player = int(current_user.get_id())
        # Получим ИД партии, ей будем присваивать акт !!!!!!!!!!!! после проверки
        game_id = request.args.get('gameID')
        # !!!!!!!!! Нужна проверка участвует ли игрок в этой игре!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Получаем список с действиями игрока
        post = request.get_json()
        # Прочитаем файл игрока
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.viking' не найден")
            return ""
        # Присвоим ход игроку
        data["acts"] = post
        # Снова запишем ход
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'w') as f:
            json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
    # Временно возвращаем пустую строку
    return ""


@app.route("/confirm_rec_turn", methods=["GET"])  # Подтверждение готовности хода
@login_required
def confirm_rec_turn():
    # print('Запрос с js')
    # Определим игрока, чтоб понять от кого получен запрос и куда его записать
    player = int(current_user.get_id())
    # Получим ИД партии, ей будем присваивать запрос !!!!!!!!!!!! после проверки
    # !!!!!!!!! TODO Нужна проверка участвует ли игрок в этой игре!!!!!!!!!!!!!!!!!!!!!!!!!!
    game_id = request.args.get('gameID')
    # print(f"ИД партии которой передается ход: {game_id}")
    # Получаем список с действиями игрока
    try:
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.viking' не найден")
        return "Игра не найдена"  # Фронту пофиг на это сообщение. TODO сделать лог на фронте для всякого
    # Присвоим изменения игроку
    data["end_turn_know"] = True
    # Снова запишем в файл
    with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.viking", 'w') as f:
        json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
    world.check_readiness(game_id)
    return "ok"


@app.route("/contact", methods=["POST", "GET"])  # Обратная связь
@login_required
def contact():
    if request.method == "POST":
        # Feedback is available only to authorized users
        if len(request.form['message']) > 3:
            flash('Message sent', category="success")
            # Неправильна форма глагола send, sent прошедшее время в утвердительной форме
            user_id = int(current_user.get_id())  # Определим id Юзера
            user = current_user.get_name()  # Определим имя Юзера
            dbase.add_feedback(request.form['message'], user_id, user)
        else:
            flash('Error send. Message text must be longer than 3 characters.', category="error")
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("contact.html", title="Feedback", menu=menu_admin)
    return render_template('contact.html', title="Feedback", menu=menu_auth)


@app.route("/login", methods=["POST", "GET"])  # Авторизация
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        user = dbase.get_user_by_login(request.form['login'].lower())
        # user = user
        if user and check_password_hash(user[2], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            print(f"Текущий пользователь:", current_user.get_id())
            return redirect(request.args.get("next") or url_for("profile"))
        flash("Wrong login/password", category="error")
        print("Ошибка авторизации")

    return render_template('login.html', title="Авторизация", menu=menu)


@app.route('/logout')  # Выход из профиля
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')  # Отображение странички профиля
@login_required
def profile():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("profile.html", title="Профиль", menu=menu_admin)
    return render_template("profile.html", title="Профиль", menu=menu_auth)


if __name__ == '__main__':
    app.run(debug=True)
    # Установим чат
    chat = ""
    rediska.set("chat", chat)

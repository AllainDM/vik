import pickle  # Модуль для сохранения параметров(классов) в файлы
import json     # Вместо pickle продуем сохранять в json

# Что-то связанное с рандомом.
# Используется для перетасовки игроков каждую итерацию обработки хода.
from random import sample

from dynasty import Dynasty
from settlement import Settlement
from cities import cities
from buildings import buildings
# from events import events
from FDataBase import FDataBase

# Попробуем импортировать main для доступа к БД
# Нельзя, получается цикл
import maindb


class FirstWorld:
    def __init__(self, row_id, date_create="0:0:0", max_players=8, is_active=1, the_end=0):
        # Основные параметры
        self.row_id = row_id  # Номер игры
        self.is_active = 1  # Флаг идущей игры. Не активная игра считается как завершенная.
        self.year = 800     # Стартовый год
        self.turn = 1       # Стартовый ход

        # Определение победителя
        self.need_win_points_for_win = 8  # Количество баллов для победы
        self.winners = []       # Список победителей, может быть не один
        self.winners_ID = []    # Список ID победителей, может быть не один
        self.game_the_end = False  # Игра завершена, можно делать ходы, но победитель уже определен

        # Игроки
        self.dynasty = {}  # Основной объект с династиями
        self.dynasty_list = []  # Список стран, для перебора при обсчете хода
        self.player_list = []   # Список ид игроков
        self.max_players = max_players  # Максимальное количество игроков

        # Сюда сохраняется поселение при создании
        self.settlements = {}  # Тут экземпляр класса
        self.settlements_list = []  # Тут просто список названий

        # Логи
        # Общий лог событий. Сюда будут записываться все выполненные действия всех "игроков"
        self.all_logs = []
        self.all_logs_party = []  # Лог всей партии
        self.date_create = date_create  # Дата создания партии

    def save_to_file(self):
        data = {
            # Основные параметры
            "row_id": self.row_id,
            "is_active": self.is_active,
            "year": self.year,
            "turn": self.turn,

            # Определение победителя
            "need_win_points_for_win": self.need_win_points_for_win,
            "winners": self.winners,
            "winners_ID": self.winners_ID,
            "game_the_end": self.game_the_end,

            # Игроки
            # "dynasty": self.dynasty,  # TODO объект с экземплярами класса, в сохранении не нуждается
            "dynasty_list": self.dynasty_list,
            "player_list": self.player_list,
            "max_players": self.max_players,

            # Управляемые поселения
            # "settlements": self.settlements,  # TODO объект с экземплярами класса, в сохранении не нуждается
            "settlements_list": self.settlements_list,

            # Логи
            "all_logs": self.all_logs,
            "all_logs_party": self.all_logs_party,
            "date_create": self.date_create,
        }
        print(f"save_to_file{data}")
        # Пишем в json
        try:
            with open(f"games/{self.row_id}/gameID_{self.row_id}.viking", 'w') as f:
                json.dump(data, f)
        except FileNotFoundError:
            print(f"Файл 'games/{self.row_id}/gameID_{self.row_id}.viking' не найден")
            return ""
        # Пишем в pickle
        # try:
        #     with open(f"games/{self.row_id}/gameID_{self.row_id}.viking", 'wb') as f:
        #         pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        # except FileNotFoundError:
        #     print(f"Файл 'games/{self.row_id}/gameID_{self.row_id}.viking' не найден")
        #     return ""

    def load_from_file(self, game_id):
        # Прочитаем из json весь файл
        try:
            with open(f"games/{game_id}/gameID_{game_id}.viking", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}.viking' не найден")
            return ""
        # Прочитаем из pickle весь файл
        # try:
        #     with open(f"games/{game_id}/gameID_{game_id}.viking", 'rb') as f:
        #         data = pickle.load(f)
        # except FileNotFoundError:
        #     print(f"Файл 'games/{game_id}/gameID_{game_id}.viking' не найден")
        #     return ""
        # Присвоим параметры
        # Основные параметры
        self.row_id = data["row_id"]
        self.year = data["year"]
        self.turn = data["turn"]

        # Определение победителя
        # Список победителей и статус игры, при окончании победитель повторно не определяется
        self.need_win_points_for_win = data["need_win_points_for_win"]
        self.winners = data["winners"]
        self.winners_ID = data["winners_ID"]
        self.game_the_end = data["game_the_end"]

        # Игроки
        # self.dynasty = data["dynasty"]  # TODO !!! Класс !!! Тут переменная в виде названия Династии на английском
        self.dynasty_list = data["dynasty_list"]  # И тут переменная в виде названия Династии на английском.....
        self.player_list = data["player_list"]
        self.max_players = data["max_players"]

        # Управляемые поселения
        # self.settlements = data["settlements"]
        self.settlements_list = data["settlements_list"]

        # Логи
        self.all_logs = data["all_logs"]
        self.all_logs_party = data["all_logs_party"]
        self.date_create = data["date_create"]

        # TODO Проверим на ошибку чтение только что записанных данных?????????

    def create_dynasty(self, row_id, player_id, name, name_rus, gold):
        # При создании династии передаем название, но можно передавать ид
        self.dynasty[name] = Dynasty(self, row_id=row_id, player_id=player_id, name=name, name_rus=name_rus, gold=gold)
        self.dynasty_list.append(name)
        print(f"Создание династии {self.dynasty_list[-1]}")
        print(f"Создание династии {self.dynasty[name]}")
        print(self.dynasty[name])
        # print(f"Общее количество династий: {len(self.dynasty_list)}")
        # print(f"Общее количество династий: {len(self.dynasty)}")
        self.player_list.append(player_id)
        self.dynasty[name].save_to_file()
        # !!!!!!!!!! Еще нужно запустить у Династии функцию сохранения ее данных в файл
        # Создадим файл с записью хода игрока. Он должен быть пустым при каждом создании игры
        acts = []
        # !!!!!!!! Возможно тут повторная запись в файл, то же самое выполняем выше "self.dynasty[name].save_to_file()"
        # try:
        #     with open(f"games/{self.row_id}/acts/gameID_{self.row_id}_playerID_{player_id}.viking", 'wb') as f:
        #         pickle.dump(acts, f, pickle.HIGHEST_PROTOCOL)
        #     return self.dynasty[name]
        # except FileNotFoundError:
        #     print(f"Файл 'games/{self.row_id}/acts/gameID_{self.row_id}_playerID_{player_id}.viking' не найден")
        #     return ""

    # TODO Создать поселение игрока
    # TODO доделать
    def create_settlement(self, row_id, player_id, name_rus, name):
        # Обьект с экземпляром класса английское название. Список поселений с русским название
        # TODO Можно ли сделать тоже на русском?
        self.settlements[name] = Settlement(self, row_id=row_id, ruler=player_id, name_rus=name_rus, name=name)
        self.settlements_list.append(name_rus)

    # Восстановить династии и поселения из файла. Запускается при обсчете хода.
    # Восстанавливаем все классы и считаем ход
    def restore_dynasty(self, game_id, player_id, dynasty_name):
        self.dynasty[dynasty_name] = Dynasty(self)
        self.dynasty[dynasty_name].load_from_file(game_id, player_id)

    def restore_settlement(self, game_id, player_id, dynasty_name):
        self.dynasty[dynasty_name] = Settlement(self)
        self.dynasty[dynasty_name].load_from_file(game_id, player_id)


def check_readiness(game_id):  # Проверить все ли страны отправили ход
    # Прочитаем общий файл с партией, нам понадобится список стран
    # json
    with open(f"games/{game_id}/gameID_{game_id}.viking", 'r') as f:
        data_main = json.load(f)
    # pickle
    # with open(f"games/{game_id}/gameID_{game_id}.viking", 'rb') as f:
    #     data_main = pickle.load(f)
    for i in data_main["player_list"]:
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{i}.viking", 'rb') as f:
            end_turn_reading = pickle.load(f)
            if not end_turn_reading["end_turn"]:
                print("Как минимум один из игроков еще не готов")
                print(f"Игрок: {i}")
                return
    print("Все игроки готовы")
    calculate_turn(game_id)


def calculate_turn(game_id):
    # Изначально запускается отдельная функция определяющая готовность хода игроков
    # Теперь восстановим все классы игры взяв параметры из pickle
    game = FirstWorld(game_id)  # Восстановим саму игру.
    game.load_from_file(game_id)  # Запустим метод считающий данные из файла.
    # Функция восстанавливая династию по списку игроков, присваивает экземпляр класса не к имени страны,
    # а к ИД игрока, от этого получается баг с клоном династии
    # for player_id in game.player_list:
    # !!!!!! Временно введем счетчик для соотношения ИД игрока от индекса страны в списке стран
    # !!!!!! По-хорошему сделать словарь, название страна: Ид игрока
    dynasty_player_id = 0
    for dynasty_name in game.dynasty_list:
        # !!!!!!!!!!! Мы тут получаем ИД игрока, а надо бы ИД династии.
        # !!!!!!!!!!! Можно было бы это совместить, но что будет, если меняется игрок на династии(стране)....
        # !!!!!!!!!!! Хотя вроде все верно, мы же забираем из подписанного файла ИДшником игрока
        # print(f"Пред восстанавливаем династию: {player_id}")
        game.restore_dynasty(game_id, game.player_list[dynasty_player_id], dynasty_name)
        dynasty_player_id += 1
    # TODO ?????????? Теперь нужно запустить собственно саму обработку действий
    # TODO  В случае начала обсчета хода, необходимо почистить лог прошлого хода у стран.
    # TODO  Или еще лучше, сделать массив вообще со всеми логами.
    # TODO  Может сделать отдельный массив в котором просто будут храниться все логи.
    for dyns in game.dynasty:
        game.dynasty[dyns].result_logs_text = []
    # Так же почистим общий лог
    game.all_logs = []
    # TODO отключил глобальные евенты
    # TODO Запустим глобальные/локальные евенты
    # TODO global_event = events.global_event()
    # TODO if global_event:
    # TODO     game.all_logs.append(global_event)
    # TODO     game.all_logs_party.append(f"Ход {game.turn}. {global_event}")
    # TODO print(f"Глобальный евент {global_event}")
    # Пробуем намутить по остаткам действий у стран
    # Введем переменную для цикла
    acts_left = True  # Будет проверяться в конце каждого цикла у игроков
    while acts_left:
        # Отрандомим через random.sample список имен с династиями
        dyn_arr = sample(game.dynasty_list, len(game.dynasty_list))
        for rand_dynasty in dyn_arr:
            # Проверим остались ли очки действия у страны
            if game.dynasty[rand_dynasty].body_points_left > 0:
                acts_left = True  # Выставим верное значение, для продолжения обсчета цикла
                game.dynasty[rand_dynasty].calc_act()
                game.dynasty[rand_dynasty].body_points_left -= 1  # Вычтем действие после обсчета
            # Вычислим остались ли у игроков ходы
            else:
                acts_left = False   # Выставим ложь, если по итогу всего цикла ни у кого не осталось ходов

    # Пост обсчет хода
    # !!!!!!!!!!!!!!!! Было просто game.dynasty. Но считалось 2 раза. А с dynasty_list другой баг
    for dynasty_name in game.dynasty:
        print(f"Почему запускается два раза? dynasty_name {dynasty_name}")
        game.dynasty[dynasty_name].calc_end_turn()

    # Запустим определение победителя
    if not game.game_the_end:
        check_winners(game)

    # Сохраним данные для стран
    # Данные сохраняем после всех изменений касающихся игрока, фронт потом запрашивает данные уже из файла
    for dynasty_name in game.dynasty:
        game.dynasty[dynasty_name].save_to_file()
    # Проверить список победителей
    # Добавим 1 к номеру хода и года
    game.year += 1
    game.turn += 1

    game.save_to_file()


# Напишем отдельно функцию определяющую победителя и оканчивающую игру
def check_winners(game):
    # Сначала посчитаем победные очки для всех стран
    for dynasty_name in game.dynasty:
        # print(f"dynasty[dynasty_name]: {game.dynasty[dynasty_name]}")
        # Посчитаем победные очки
        wp = game.dynasty[dynasty_name].calc_win_points()
        # Если их больше указанного количества записываем страну в список победителей
        if wp >= game.need_win_points_for_win:
            game.winners.append(game.dynasty[dynasty_name].name_rus)
            print(f"Ид победителя: {game.dynasty[dynasty_name].player_id}")
            game.winners_ID.append(game.dynasty[dynasty_name].player_id)
    print(f"winners: {game.winners}")
    # Если есть победители, надо их записать в БД
    # Необходимо определить страны победительницы, определить ИД игрока, и добавить в БД запись
    # Нужен цикл по массиву с победителями
    db = maindb.get_db()
    dbase = FDataBase(db)
    if len(game.winners_ID) > 0:
        for i in game.winners_ID:
            dbase.update_wins(i)
        # Сменим статус игры, заодно сохраним данные
        game.game_the_end = True
        game.save_to_file()

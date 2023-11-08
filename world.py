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
        self.dynasty_dict = {}   # Словарь, где ключ это ид игрока, а значение это имя династии
        # TODO возможно стоит убрать dynasty_list и player_list, ибо их должен заменить словарь dynasty_dict
        self.dynasty_list = []  # Список стран, для перебора при обсчете хода
        self.player_list = []   # Список ид игроков, он же ид династии
        self.max_players = max_players  # Максимальное количество игроков

        # Сюда сохраняется поселение при создании
        self.settlements = {}  # Тут экземпляр класса
        self.settlements_list = []  # Тут просто список названий
        self.settlements_dict = {}  # Словарь, где значением ид, для перебора при "восстановлении"

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
            "dynasty_dict": self.dynasty_dict,
            "dynasty_list": self.dynasty_list,
            "player_list": self.player_list,
            "max_players": self.max_players,

            # Управляемые поселения
            # "settlements": self.settlements,  # TODO объект с экземплярами класса, в сохранении не нуждается
            "settlements_list": self.settlements_list,
            "settlements_dict": self.settlements_dict,

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
        self.dynasty_dict = data["dynasty_dict"]
        self.dynasty_list = data["dynasty_list"]  # И тут переменная в виде названия Династии на английском.....
        self.player_list = data["player_list"]
        self.max_players = data["max_players"]

        # Управляемые поселения
        # self.settlements = data["settlements"]
        self.settlements_list = data["settlements_list"]
        self.settlements_dict = data["settlements_dict"]

        # Логи
        self.all_logs = data["all_logs"]
        self.all_logs_party = data["all_logs_party"]
        self.date_create = data["date_create"]

        # TODO Проверим на ошибку чтение только что записанных данных?????????

    def create_dynasty(self, row_id, player_id, name_eng, name_rus, main_settlement, gold=1000):
        # При создании династии передаем название, но можно передавать ид
        self.dynasty[name_eng] = Dynasty(self, row_id=row_id, player_id=player_id, name_eng=name_eng,
                                         name_rus=name_rus, main_settlement=main_settlement, gold=gold)
        # Для перебора при обработке хода
        # Старое: Список династий, для перебора при обсчете хода
        self.dynasty_list.append(name_eng)
        # Новое: Сохраним в словарь, где ключ ид игрока(== ид династии), а значение имя династии
        self.dynasty_dict[player_id] = name_eng
        print(f"Создание династии {self.dynasty_list[-1]}")
        print(f"Создание династии {self.dynasty[name_eng]}")
        print(self.dynasty[name_eng])
        # print(f"Общее количество династий: {len(self.dynasty_list)}")
        # print(f"Общее количество династий: {len(self.dynasty)}")
        # Список игроков в виде ид этих самых игроков
        self.player_list.append(player_id)
        # Сохранение династии в файл
        self.dynasty[name_eng].save_to_file()

    # TODO Создать поселение игрока
    # TODO доделать
    def create_settlement(self, game_id, row_id, ruler, name_rus, name_eng):
        # Объект с экземпляром класса английское название. Список поселений с русским название
        # TODO Можно ли сделать тоже на русском?
        self.settlements[name_eng] = Settlement(self, game_id, row_id, ruler, name_rus, name_eng)
        # Для перебора при обработке хода
        # Старое: Список поселений, для перебора при обсчете хода
        self.settlements_list.append(name_eng)
        # Сохраним в новый словарь, где ключ row_id поселения, а значение название.
        # row_id нужен для сохранения файла
        self.settlements_dict[row_id] = name_eng
        # TODO нужно что-то куда-то добавлять еще?

        # Сохраним в файл
        self.settlements[name_eng].save_to_file()

    # Восстановить династии и поселения из файла. Запускается при обсчете хода.
    # Восстанавливаем все классы и считаем ход
    # game_id и player_id необходим для поиска файла при загрузке данных, больше ничего не требуется
    def restore_dynasty(self, game_id, player_id, dynasty_name):  #
        self.dynasty[dynasty_name] = Dynasty(self, game_id)
        self.dynasty[dynasty_name].load_from_file(game_id, player_id)
        print(f"Восстановлена династия: {self.dynasty[dynasty_name].name_eng}")

    # game_id и player_id необходим для поиска файла при загрузке данных, больше ничего не требуется
    def restore_settlement(self, game_id, settlement_id, name_eng):  #
        self.settlements[name_eng] = Settlement(self, game_id)
        self.settlements[name_eng].load_from_file(game_id, settlement_id)
        print(f"Восстановлено поселение: {self.settlements[name_eng].name_eng}")


def check_readiness(game_id):  # Проверить все ли страны отправили ход
    # Прочитаем общий файл с партией, нам понадобится список стран
    # json
    with open(f"games/{game_id}/gameID_{game_id}.viking", 'r') as f:
        data_main = json.load(f)
    # pickle
    # with open(f"games/{game_id}/gameID_{game_id}.viking", 'rb') as f:
    #     data_main = pickle.load(f)
    for i in data_main["player_list"]:
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{i}.viking", 'r') as f:
            end_turn_reading = json.load(f)
            if not end_turn_reading["end_turn"]:
                print("Как минимум один из игроков еще не готов")
                print(f"Игрок: {i}")
                return
    print("Все игроки готовы")
    calculate_turn(game_id)


def calculate_turn(game_id):
    # Изначально запускается отдельная функция определяющая готовность хода игроков
    # Теперь восстановим все классы игры взяв параметры из json файла(уже не pickle)
    game = FirstWorld(game_id)  # Восстановим саму игру.
    game.load_from_file(game_id)  # Запустим метод считающий данные из файла.

    # Восстановим династии.
    # Перебираем словарь с династиями. Где нам для восстановления понадобится и имя и ид.
    # Где ид игрока = ид династии. Это не row_id, а общий ид для удобства восстановления.
    for k, v in game.dynasty_dict.items():
        game.restore_dynasty(game_id=game_id, player_id=k, dynasty_name=v)

    # Восстановим поселения.
    for k, v in game.settlements_dict.items():
        game.restore_settlement(game_id=game_id, settlement_id=k, name_eng=v)

    # Очистим логи у стран.
    for dyns in game.dynasty:
        game.dynasty[dyns].result_logs_text = []
    # Очистим логи у поселений.
    for settl in game.settlements:
        game.settlements[settl].result_events_text = []
    # Так же почистим общий лог
    game.all_logs = []

    # TODO отключил глобальные ивенты
    # Запустим глобальные/локальные ивенты
    # global_event = events.global_event()
    # if global_event:
    #     game.all_logs.append(global_event)
    #     game.all_logs_party.append(f"Ход {game.turn}. {global_event}")
    # print(f"Глобальный ивент {global_event}")

    # Теперь запускаем собственно саму обработку действий.
    # Считать будем пока хотя бы у одного игрока есть невыполненное действие
    # Для этого введем булевую переменную.
    acts_left = True  # Будет проверяться в конце каждого цикла у игроков
    while acts_left:  # Бесконечный цикл пока действия остались
        # Отрандомим через random.sample список имен с династиями
        # Рандомим каждый круг(по 1 действию каждого игрока), для непредсказуемости порядка хода
        dyn_arr = sample(game.dynasty_list, len(game.dynasty_list))
        for rand_dynasty in dyn_arr:
            # Проверим, остались ли очки действия у страны
            if game.dynasty[rand_dynasty].body_points_left > 0:
                acts_left = True  # Выставим верное значение, для продолжения обсчета цикла
                game.dynasty[rand_dynasty].calc_act()
                # TODO пока 1 действие 1 очко, так что пока считаем тут
                game.dynasty[rand_dynasty].body_points_left -= 1  # Вычтем действие после обсчета
            # Вычислим остались ли у игроков ходы
            else:
                acts_left = False   # Выставим ложь, если по итогу всего цикла ни у кого не осталось ходов

    # TODO пост обсчет поселения. Например баланс ресурсов, торговля и рост населения.
    # TODO нужно ли рандомить пост обсчет для поселений?
    for settlement in game.settlements:
        game.settlements[settlement].calc_end_turn()

    # Пост обсчет хода для игрока. Не зависящие от его действий, по типу +1 к возрасту персонажей.
    # TODO нужно ли рандомить пост обсчет для игроков?
    for dynasty_name in game.dynasty:
        print(f"Раньше это запускалось два раза, а сейчас? dynasty_name {dynasty_name}")
        game.dynasty[dynasty_name].calc_end_turn()

    # Запустим определение победителя
    if not game.game_the_end:
        check_winners(game)

    # Сохраним данные для стран
    # Данные сохраняем после всех изменений касающихся игрока, фронт потом запрашивает данные уже из файла
    for dynasty_name in game.dynasty:
        game.dynasty[dynasty_name].save_to_file()
    # Проверить список победителей.
    # Добавим 1 к номеру хода и года.
    # TODO тут будет сезонность если потребуется.
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

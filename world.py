import pickle  # Модуль для сохранения параметров(классов) в файлы
import json     # Вместо pickle пробуем сохранять в json

# Что-то связанное с рандомом.
# Используется для перетасовки игроков каждую итерацию обработки хода.
from random import sample
import random

from dynasty import Dynasty
from settlement import Settlement
from province import Province
from army import Army
from cities import cities
from buildings import buildings
import names
# from events import events
from FDataBase import FDataBase

# Попробуем импортировать main для доступа к БД
# Нельзя, получается цикл
import maindb
import mod  # Различные модификаторы as MOD


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

        # Провинция, создается перед поселением
        self.provinces = {}  # Тут экземпляр класса. Может экземплярЫ?
        self.provinces_list = []  # Тут просто список названий
        self.provinces_dict = {}  # Словарь, где значением ид, для перебора при "восстановлении"

        # Сюда сохраняется поселение при создании
        self.settlements = {}  # Тут экземпляр класса
        self.settlements_list = []  # Тут просто список названий
        self.settlements_dict = {}  # Словарь, где значением ид, для перебора при "восстановлении"

        # Сохранение армий
        self.armies = {}  # Тут экземпляр класса
        self.armies_list = []  # Тут просто список названий
        self.armies_dict = {}  # Словарь, где значением ид, для перебора при "восстановлении"

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
            # "dynasty": self.dynasty,  # объект с экземплярами класса, в сохранении не нуждается
            "dynasty_dict": self.dynasty_dict,
            "dynasty_list": self.dynasty_list,
            "player_list": self.player_list,
            "max_players": self.max_players,

            # Провинции
            # "provinces": self.provinces,  # объект с экземплярами класса, в сохранении не нуждается
            "provinces_list": self.provinces_list,
            "provinces_dict": self.provinces_dict,

            # Управляемые поселения
            # "settlements": self.settlements,  # объект с экземплярами класса, в сохранении не нуждается
            "settlements_list": self.settlements_list,
            "settlements_dict": self.settlements_dict,

            # Армии
            # "armies": self.armies,  # объект с экземплярами класса, в сохранении не нуждается
            "armies_list": self.armies_list,
            "armies_dict": self.armies_dict,

            # Логи
            "all_logs": self.all_logs,
            "all_logs_party": self.all_logs_party,
            "date_create": self.date_create,
        }
        print(f"save_to_file{data}")
        # Пишем в json
        try:
            with open(f"games/{self.row_id}/gameID_{self.row_id}.viking", 'w') as f:
                json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
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

        # self.provinces = data["provinces"]  # Не нужен

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

        # Провинции
        # "provinces": self.provinces,  # объект с экземплярами класса, в сохранении не нуждается
        self.provinces_list = data["provinces_list"]
        self.provinces_dict = data["provinces_dict"]

        # Управляемые поселения
        # self.settlements = data["settlements"]
        self.settlements_list = data["settlements_list"]
        self.settlements_dict = data["settlements_dict"]

        # Армии
        # self.armies = data["armies"]
        self.armies_list = data["armies_list"]
        self.armies_dict = data["armies_dict"]

        # Логи
        self.all_logs = data["all_logs"]
        self.all_logs_party = data["all_logs_party"]
        self.date_create = data["date_create"]

        # TODO Проверим на ошибку чтение только что записанных данных?????????

    def create_dynasty(self, row_id, player_id, name_eng, name_rus, main_settlement, province_id, gold=1000):
        # При создании династии передаем название, но можно передавать ид
        self.dynasty[name_eng] = Dynasty(self, row_id=row_id, player_id=player_id,
                                         name_eng=name_eng, name_rus=name_rus,
                                         main_settlement=main_settlement, province_id=province_id,
                                         gold=gold)
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
        # # Функция поиска юнитов по поселениям указанным в списке принадлежащих игроку.
        # !!! проверяет до создания всех поселений, вылазит ошибка соответственно
        # self.dynasty[name_eng].search_our_units()
        # Сохранение династии в файл
        self.dynasty[name_eng].save_to_file()

    # Создаем провинцию перед созданием поселения
    def create_province(self, game_id, row_id, name_rus, name_eng):
        """Создание класса провинции.
        Класс .... дописать описание"""
        self.provinces[name_eng] = Province(self, game_id, row_id, name_rus, name_eng)
        # Сохраним в словарь. Ключ ид провинции. Значение название на английском.
        self.provinces_dict[row_id] = name_eng
        # Так же добавим в список. Как минимум по его длине определяется ид новой провинции.
        self.provinces_list.append(name_eng)
        # Сохраним в файл.
        # Сохраним позже из класса игры, после добавления различных данных.
        # self.provinces[name_eng].save_to_file()

        return self.provinces[name_eng]  # Вернем ссылку для создания поселений

    # Создаем армию
    # Стартовую в провинции или в любую можно создать данным методом?
    def create_army(self, game_id, row_id, home_location, ruler, name_rus, name_eng):
        """Создание армии в провинции.
        Класс .... дописать описание"""
        # def __init__(self, game, row_id, game_id, player_id=0, home_location=0, name_eng="army", name_rus="армия"):
        self.armies[name_eng] = Army(self, row_id=row_id, game_id=game_id, player_id=ruler,
                                     home_location=home_location, name_eng=name_eng, name_rus=name_rus)
        ...

        # return self.provinces[name_eng]  # Вернем ссылку для создания поселений

    # TODO Создать поселение игрока
    # TODO доделать
    def create_settlement(self, dbase, game_id, province, row_id, ruler, name_rus, name_eng, player=False):
        """
        Функция создания поселения.\n
        1. Создание экземпляра класса, сохраняется в словарь с ключом названием поселения.
        2. Добавление имени поселение в список, для будущих обсчетов.
        3. Сохранение имени поселения в словарь, для навигации при обсчете хода.
        4. Создание стартовой рандомной постройки.
        5. Создание стартовой армии.
        6. Обновление данных о поселении. TODO ??????
        7. Сохранение поселения в файл.
        :param dbase:
        :param game_id:
        :param province:
        :param row_id:
        :param ruler:
        :param name_rus:
        :param name_eng:
        :param player:
        :return:
        """

        # 1. Создание экземпляра класса, сохраняется в словарь с ключом названием поселения.
        # Объект с экземпляром класса английское название. Список поселений с русским название
        # TODO Можно ли сделать тоже на русском?
        # print(f"row_id {row_id}")
        self.settlements[name_eng] = Settlement(self, game_id, province, row_id, ruler, name_rus, name_eng, player)

        # TODO Судя по всему не используется. Идет перебор из переменной в классе игры.
        # 2. Добавление имени поселение в список, для будущих обсчетов.
        # Для перебора при обработке хода
        # Старое: Список поселений, для перебора при обсчете хода
        # Сам по себе список или словарь очень важен. Все поселения хранятся в одном списке без привязки к провинции.
        self.settlements_list.append(name_eng)

        # 3. Сохранение имени поселения в словарь, для навигации при обсчете хода.
        # Сохраним в новый словарь, где ключ row_id поселения, а значение название.
        # row_id нужен для сохранения файла
        self.settlements_dict[str(row_id)] = name_eng

        # TODO нужно что-то куда-то добавлять еще?

        # 4. Создание стартовой рандомной постройки.
        # Добавим новому поселению стартовую рандомную постройку
        rnd = random.randint(1, 4)
        if rnd == 1:
            # self.settlements[name_eng].buildings_list["Огород"] += 1
            self.settlements[name_eng].buildings_list["Рыбацкая_пристань"] += 1
        elif rnd == 2:
            self.settlements[name_eng].buildings_list["Огород"] += 1
        elif rnd == 3:
            # self.settlements[name_eng].buildings_list["Огород"] += 1
            self.settlements[name_eng].buildings_list["Угодье"] += 1
        elif rnd == 4:
            # self.settlements[name_eng].buildings_list["Огород"] += 1
            # self.settlements[name_eng].buildings_list["Рыбацкая_пристань"] += 1
            self.settlements[name_eng].buildings_list["Лесорубка"] += 1

        # 5. Создание стартовой армии.
        list_units = []

        # тестовое добавление 2 юнита
        if player:
            print("Игрок, добавляем доп юнита.")
            new_group_units_id2 = dbase.add_group_units(game_id, row_id, row_id, name_rus, "доп отряд игрока",
                                                        "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?")
            for u in range(20):
                rnd_units_name = random.randint(0, len(names.male_names_list) - 1)
                # Далее добавил в бд, вычислив ид(не требуется)
                id_for_new_unit = dbase.add_unit(game_id, new_group_units_id2,
                                                 4, 4, 3, 3, 3, 3, 1, 1, 2, 2, 2, 2, 0,
                                                 names.male_names_list[rnd_units_name])
            else:
                print("Не игрок.")
        # конец тестового добавления второго юнита

        new_group_units_id = dbase.add_group_units(game_id, row_id, row_id, name_rus, "отряд",
                                                   4, 4, 3, 3, 3, 3, 1, 1, 2, 2, 2, 2, 0)

        for u in range(20):
            rnd_units_name = random.randint(0, len(names.male_names_list)-1)
            # Далее добавил в бд, вычислив ид(не требуется)
            id_for_new_unit = dbase.add_unit(game_id, new_group_units_id,
                                             4, 4, 3, 3, 3, 3, 1, 1, 2, 2, 2, 2, 0,
                                             names.male_names_list[rnd_units_name])

        # В записи поселения будем хранить только ид юнитов, сама запись будет только в БД.
        # Больше не передаем инфу о юнитах в поселение.
        # self.settlements[name_eng].units = [list_units]
        self.settlements[name_eng].calc_mid()

        # TODO новое, теперь вносим всех юнитов в один общий файл в папке и миром.
        # Сначала читаем файл, извлекаем список, дополняем и записываем обратно.
        data = []  # Список с юнитами
        try:
            with open(f"games/{game_id}/gameID_{game_id}_units.viking", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_units.viking' не найден. Возможно еще не создан.")
            # return ""
        # Дополним список
        # data.append(units)
        try:
            with open(f"games/{game_id}/gameID_{game_id}_units.viking", 'w') as f:
                json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_units.viking' не найден")
            return ""

        # 6. Обновление данных о поселении. TODO ??????
        # Обновим различные данные для поселения
        self.settlements[name_eng].update_var()

        # 7. Сохранение поселения в файл.
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
    def restore_province(self, game_id, province_id, name_eng):  #
        """Восстановление провинции перед обработкой хода.
        Должна возвращать ссылку на себя для дальнейшего восстановления поселений"""
        self.provinces[name_eng] = Province(self, game_id)
        self.provinces[name_eng].load_from_file(game_id, province_id)
        print(f"Восстановлена провинция: {self.provinces[name_eng].name_eng}")
        # Восстановим поселения сразу из списка в провинции
        # Внутри класса провинции
        self.provinces[name_eng].restore_settlements()

    # game_id и player_id необходим для поиска файла при загрузке данных, больше ничего не требуется
    # def restore_settlement(self, game_id, settlement_id, name_eng):  #
    #     self.settlements[name_eng] = Settlement(self, game_id)
    #     self.settlements[name_eng].load_from_file(game_id, settlement_id)
    #     print(f"Восстановлено поселение: {self.settlements[name_eng].name_eng}")


def check_readiness(game_id):  # Проверить все ли страны отправили ход
    """
    Определение готовности игроков.\n
    Основная функция запускающая обработку хода до введения в игру таймера.\n
    1. Чтение файла игры, из него получаем словарь со странами.\n
    2. Цикл словаря со странами.\n
    :param game_id:
    :return:
    """

    # 1. Чтение файла игры, из него получаем словарь со странами.
    with open(f"games/{game_id}/gameID_{game_id}.viking", 'r') as f:
        data_main = json.load(f)

    # 2. Цикл словаря со странами
    # По информации из словаря перебираем файлы с игроками, проверяя переменную отвечающую за готовность хода.
    # Если хоть один игрок не готов функция прекращает свою работу и ход не запускается.
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
    """
    Обсчет хода. \n
    1. Восстановим игру создав экземпляр класса игры и загрузив данные(из файла).
    2. Восстановим династии(класс игрока).
    3. Восстановим провинции и поселения(по спискам в записи провинции).
    4. Обнулим торговлю в провинциях.
    5. Очистим логи для записи новых.
    6. Обсчет действий игроков.
    7. Обсчет окончания хода поселения.
    8. Пост обсчёт игроков.
    9. Определение победителей.
    10. Сохранение данных игроков.
    11. Изменение основных параметров игры.
    12. Сохранение файла игры
    """
    # Изначально запускается отдельная функция определяющая готовность хода игроков

    # 1. Создать экземпляр класса игры и загрузить данные(из файла).
    # Восстановим все классы игры взяв параметры из json файла
    game = FirstWorld(game_id)  # Восстановим саму игру.
    game.load_from_file(game_id)  # Запустим метод считающий данные из файла.

    # 2. Восстановим династии(класс игрока)
    # Перебираем словарь с династиями. Где нам для восстановления понадобится и имя и ид.
    # Где ид игрока = ид династии. Это не row_id, а общий ид для удобства восстановления.
    print('Восстанавливаем династии. Класс dynasty.')
    print(game.dynasty_dict)
    for k, v in game.dynasty_dict.items():
        game.restore_dynasty(game_id=game_id, player_id=k, dynasty_name=v)

    # 3. Восстановим провинции.
    # В функции restore_province восстанавливаются и поселения по внутреннему списку.
    print('Восстанавливаем провинции. Класс province.')
    print(game.provinces_dict)
    for k, v in game.provinces_dict.items():
        game.restore_province(game_id=game_id, province_id=k, name_eng=v)

    # 4. Обнулим торговлю в провинциях для составления нового списка товаров, ибо не накапливаемые.
    print("Обнуление торговых складов провинций.")
    print("ВНИМАНИЕ!!!!! Возможно, тут не правильно обнуляются товары.")
    # TODO ну как бы вот
    for prov in game.provinces.values():  # Тут должны быть ссылки на провинции.
        for v in prov.province_goods_for_trade.values():
            # print(f"Было: {v}")
            v = 0
            # print(f"Стало: {v}")
        # for k, v in prov.province_goods_for_trade.items():
        #     v = 0

    # 5. Очистим логи для записи новых.
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

    # 6. Обсчет действий игроков
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
                # Действие вычитается даже если игрок ничего не делал, иначе цикл был бы бесконечный
                game.dynasty[rand_dynasty].body_points_left -= 1  # Вычтем действие после обсчета
            # Вычислим остались ли у игроков ходы
            else:
                acts_left = False   # Выставим ложь, если по итогу всего цикла ни у кого не осталось ходов

    # 7. Обсчет окончания хода поселения.
    # TODO пост обсчет поселения. Например баланс ресурсов, торговля и рост населения.
    # TODO нужно ли рандомить пост обсчет для поселений?
    # print(f"тттттттттттттттттттттттттттттттттттттттттттттттттттттттттттттттттттттт")
    for settlement in game.settlements:
        # print(f"88888888888888888888888888888888888888888888888888888888888888888888888888888888888888")
        # print(f"88888888888         Тут разделение обработки поселений              888888888888888888")
        # print(f"88888888888888888888888888888888888888888888888888888888888888888888888888888888888888")
        # print(f"Обсчитываем поселение")
        print(game.settlements[settlement])
        game.settlements[settlement].calc_turn_settlement()
        game.settlements[settlement].calc_end_turn_settlement()

    # 7.1 Отдельно от поселений пересчитаем армии, средние характеристики и прочее.
    # Исходим из того, что не все группы юнитов привязаны к поселениям.
    # TODO подключимся к БД, возможно стоит перенести в другое место
    db = maindb.get_db()
    dbase = FDataBase(db)
    print(f"Готовимся высчитать средние параметры юнитов при обсчета хода (world.py)")
    list_param = ["hp_max", "hp_cur", "endurance_max", "endurance_cur",
                  "strength", "agility", "armor", "shield",
                  "melee_skill", "melee_weapon", "ranged_skill", "ranged_weapon",
                  "experience"]
    dbase.update_average_parameters_units(game_id, list_param)
    # dbase.calc_average_parameters_units(game_id, list_param)

    # 8. Пост обсчёт игроков.
    # Пост обсчет хода для игрока. Не зависящие от его действий, по типу +1 к возрасту персонажей.
    # TODO нужно ли рандомить пост обсчет для игроков?
    for dynasty_name in game.dynasty:
        print(f"Раньше это запускалось два раза, а сейчас? dynasty_name {dynasty_name}")
        game.dynasty[dynasty_name].calc_end_turn_dynasty()

    # 9. Определение победителей.
    # Запустим определение победителя
    if not game.game_the_end:
        check_winners(game)

    # 10. Сохранение данных игроков.
    # Сохраним данные для стран.
    # Данные сохраняем после всех изменений касающихся игрока, фронт потом запрашивает данные уже из файла
    for dynasty_name in game.dynasty:
        game.dynasty[dynasty_name].save_to_file()

    # 11. Изменение основных параметров игры.
    # Добавим 1 к номеру хода и года.
    # TODO тут будет сезонность если потребуется.
    game.year += 1
    game.turn += 1

    # 12. Сохранение файла игры
    game.save_to_file()


# Функция определяющая победителя и оканчивающую игру
def check_winners(game):
    """
    Определение победителей.
    ВНИМАНИЕ!!!! Функция не изменялась с прошлой версии.
    :param game:
    :return:
    """
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

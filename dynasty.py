# from colony_buildings import buildings
import os
import pickle
import redis

from goods import Goods
from buildings import Buildings
import decision  # Импортируем решения, будет обращаться напрямую


# Настройка Redis для хранения данных игроков
rediska = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    # password='qwerty',
    charset="utf-8",
    decode_responses=True
)


class Dynasty:
    def __init__(self, game, row_id=0, player_id=0, name="default_name", name_rus="Страна", gold=0):
        self.row_id = row_id
        self.player_id = player_id
        self.name = name
        self.name_rus = name_rus
        self.gold = gold
        self.title = 0  # Стартовый ранг игрока.
        self.body_points = 3  # Очки действий для игрока
        # Остаток очков действий, для цикла подсчета хода. Восстанавливается перед подсчетом хода взяв значение выше
        self.body_points_left = self.body_points

        # Общие стартовые условия
        self.win_points = 0

        self.acts = []  # Список действий
        # self.logs = []
        # self.acts_text = [] # Список с текстом не выполненных действий
        self.result_logs_text = []  # Список с текстом выполненных действий
        self.result_logs_text_all_turns = []  # Список с текстом выполненных действий по всем ходам

        self.end_turn = False  # Отправила ли страна заявку
        self.end_turn_know = True  # Прочитал ли оповещение о новом ходе

        # Это должно быть не у страны, а отдельный столбец у игрока в БД
        # self.active_game = 0 # Id Активной игры. Надо что-то решить и убрать 0

        self.game = game
        self.game_id = game.row_id  # Сохраним ИД игры, для создания правильной ссылки при необходимости
        # Но конечно же, можно было бы передать ее аргументом при создании династии

    def save_to_file(self):
        data = {
            "row_id": self.row_id,
            "game_id": self.game_id,
            "player_id": self.player_id,
            "name": self.name,
            "name_rus": self.name_rus,
            "gold": self.gold,
            "title": self.title,
            "body_points": self.body_points,
            "win_points": self.win_points,

            "acts": self.acts,
            "result_logs_text": self.result_logs_text,
            "result_logs_text_all_turns": self.result_logs_text_all_turns,
            "end_turn": self.end_turn,
            "end_turn_know": self.end_turn_know,
        }
        # Пишем в pickle.
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.trader", 'wb') as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.trader' не найден")
            return ""

    def load_from_file(self, game_id, player_id):
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player_id}.trader", 'rb') as f:
                data = pickle.load(f)
                # print(f"Восстанавливаем династию: {data}")
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player_id}.trader' не найден")
            return ""
        self.row_id = data["row_id"]
        self.game_id = data["game_id"]
        self.player_id = data["player_id"]
        self.name = data["name"]
        self.name_rus = data["name_rus"]
        self.gold = data["gold"]
        self.title = data["title"]
        self.win_points = data["win_points"]
        self.body_points = data["body_points"]

        # TODO убрать
        # Список доступных для строительства построек
        # !!!!!!! Это нужно не сохранять, а каждый раз обновлять из класса, мало ли что изменилось
        # self.buildings_available_list = data["buildings_available_list"]

        self.acts = data["acts"]
        self.result_logs_text = data["result_logs_text"]
        self.result_logs_text_all_turns = data["result_logs_text_all_turns"]
        self.end_turn = data["end_turn"]
        self.end_turn_know = data["end_turn_know"]

    def calc_act(self):  # Подсчет одного действия для династии
        # print(f"Считаем ход для династии: {self.name}")
        if self.acts:
            # 1 индекс это первое по списку действие, первый элемент в списке, оно выполняется и удаляется
            # 2 индекс это индекс с ИД действия, он под индексом 1, под 0 текстовое описание. Начиная с 2 аргументы
            # Передавать ли аргументы в функцию или вытаскивать их уже в самой функции. Попробуем по разному =>
            if self.acts[0][1] == 101:
                # self.act_build_colony(self.acts[0][2])  # Тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            elif self.acts[0][1] == 201:
                # self.act_sell_goods(self.acts[0][2], self.acts[0][3], self.acts[0][4])  # И тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            elif self.acts[0][1] == 202:  #
                # self.act_sell_all_goods(self.acts[0][2])  # И тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            elif self.acts[0][1] == 301:  #
                # self.act_buy_title()  # Аргументов нет
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            elif self.acts[0][1] == 302:  #
                # self.act_make_donate(self.acts[0][2])  # Аргументом сумма пожертвования
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            else:
                print('Записей в акте нет')


    # Подсчет каких либо параметров после обсчета действия игроков. Обязательно выполняется после действий
    # Типо какие-нибудь налоги или наоборот доп доход
    # Производство товаров будет обрабатываться здесь
    def calc_end_turn(self):
        # self.()  # Рассчитаем баланс товаров(производство-потребление)

        # Выставим False для параметра подтверждающего отправку хода и получение оповещения о новом ходе
        self.end_turn = False
        self.end_turn_know = False
        self.save_to_file()
        print(f"Функция обработки конца хода")

    # Неактуальный метод. Теперь запускается как функция получая аргументами ИД партии и страны.
    def act_build(self, buildings_name):     # 101 id
        # !!!!!!! На будущее нужно сделать сверку, доступна ли это постройка для игрока
        # Два раза buildings это: 1 = экземпляр класса с постройками, 2 = список построек уже в классе
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        if self.gold >= self.game.buildings_price[buildings_name]:
            self.buildings_list[buildings_name] += 1  # Добавим постройку Династии
            self.game.buildings_list[buildings_name] += 1  # И добавим к общему количеству в стране
            self.gold -= self.game.buildings_price[buildings_name]

            self.result_logs_text.append(f"Вы построили {buildings_name}")
            self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы построили {buildings_name}")
            self.game.all_logs.append(f"{self.name_rus} построили {buildings_name}")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"{self.name_rus} построили {buildings_name}")
        else:
            self.result_logs_text.append(f"Вы НЕ построили {buildings_name}, не хватило денег.")

    def calc_win_points(self):
        # Возьмем по 1 очку за 3000
        win_points = round(self.gold / 3000)

        # Добавим за титул
        win_points += self.title
        self.win_points = win_points
        # print(f"Победные очки {self.name_rus}: {self.win_points}")
        return win_points

    # Отмена действий. TODO Вторым аргументом количество, все, последний или номер индекса(еще не реализованно)
    def cancel_act(self, what):
        if what == "all":
            self.acts = []
        elif what == "last":
            self.acts.pop(-1)



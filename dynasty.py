# from colony_buildings import buildings
import os
import pickle
import redis
import json

import mod
from goods import Goods
from buildings import Buildings
import decision  # Импортируем решения, будет обращаться напрямую

import maindb
from FDataBase import FDataBase


# Настройка Redis для хранения данных игроков
rediska = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    # password='qwerty',
    charset="utf-8",
    decode_responses=True
)


class Dynasty:
    def __init__(self, game, row_id, player_id=0, name_eng="default_name", name_rus="Страна",
                 main_settlement=0, province_id=0, gold=0):
        self.row_id = row_id
        # self.row_id = player_id  # Для id династии присвоим id игрока
        self.player_id = player_id  # id игрока
        self.name_eng = name_eng            # Имя Династии игрока на английском
        self.name_rus = name_rus    # Имя Династии игрока на русском
        self.gold = gold            # Казна непосредственно игрока
        self.main_settlement = str(main_settlement)  # ид "главного" поселения игрока(управляемого). Строка
        # Высчитаем ид родной провинции, для передачи данных на фронтенд.
        # TODO пока просто передадим при создании экземпляра класса.
        self.main_province = province_id
        # self.our_settlements = [str(main_settlement)]  # Список ид поселений под управлением игрока
        # TODO выдаем несколько поселений для тестов.
        self.our_settlements = [str(main_settlement),
                                str(main_settlement+1),
                                str(main_settlement+2),
                                str(main_settlement+3),
                                str(main_settlement+4),
                                # str(main_settlement+5),
                                # str(main_settlement+6),
                                # str(main_settlement+7),
                                # str(main_settlement+8),
                                # str(main_settlement+9),
                                # str(main_settlement+10),
                                ]  # Список ид поселений под управлением игрока
        self.our_units = []  # Наши юниты, соберем из наших поселений. TODO не используется?
        self.armies = []  # Список ид армий игрока

        # Уловно характеристики правителя. Пока играем без династии
        self.title = 0              # Стартовый ранг игрока
        self.body_points = 3        # Очки действий игрока
        self.authority = 0          # Авторитет
        # Остаток очков действий, для цикла подсчета хода.
        # Восстанавливается перед подсчетом хода взяв значение выше
        self.body_points_left = self.body_points

        self.win_points = 0  # Победные очки

        # Логи
        self.acts = []  # Список действий
        # self.logs = []  # TODO ???
        # self.acts_text = [] # Список с текстом не выполненных действий
        self.result_logs_text = []  # Список с текстом выполненных действий за прошедший ход
        self.result_logs_text_all_turns = []  # Список с текстом выполненных действий за всю игру

        self.end_turn = False  # Отправила ли страна заявку
        self.end_turn_know = True  # Прочитал ли оповещение о новом ходе

        # Ссылка на мир для взаимодействия.
        self.game = game

        # TODO не понятен функционал ниже описанного
        # Сохраним ИД игры, для создания правильной ссылки при необходимости
        # Но конечно же, можно было бы передать ее аргументом при создании династии
        self.game_id = game.row_id

    def save_to_file(self):
        data = {
            "row_id": self.row_id,
            "game_id": self.game_id,
            "player_id": self.player_id,
            "name_eng": self.name_eng,
            "name_rus": self.name_rus,
            "gold": round(self.gold, 1),  # Перед записью округлим до десятых

            "title": self.title,
            "body_points": self.body_points,
            "authority": self.authority,

            "main_settlement": self.main_settlement,
            "main_province": self.main_province,
            "our_settlements": self.our_settlements,

            # "our_units": self.our_units,
            "armies": self.armies,

            "win_points": self.win_points,

            "acts": self.acts,
            "result_logs_text": self.result_logs_text,
            "result_logs_text_all_turns": self.result_logs_text_all_turns,

            "end_turn": self.end_turn,
            "end_turn_know": self.end_turn_know,
        }
        # Пишем в json
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.viking", 'w') as f:
                json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
        except FileNotFoundError:
            print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.viking' не найден")
            return ""
        # Пишем в pickle
        # Тут нужно отловить ошибку отсутствия файла
        # try:
        #     with open(f"games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.viking", 'wb') as f:
        #         pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        # except FileNotFoundError:
        #     print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.viking' не найден")
        #     return ""

    def load_from_file(self, game_id, player_id):
        # game_id и player_id необходим для поиска файла
        # Тут нужно отловить ошибку отсутствия файла
        # json
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player_id}.viking", 'r') as f:
                data = json.load(f)
                # print(f"Восстанавливаем династию: {data}")
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player_id}.viking' не найден")
            return ""
        # pickle
        # try:
        #     with open(f"games/{game_id}/gameID_{game_id}_playerID_{player_id}.viking", 'rb') as f:
        #         data = pickle.load(f)
        #         # print(f"Восстанавливаем династию: {data}")
        # except FileNotFoundError:
        #     print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player_id}.viking' не найден")
        #     return ""
        self.row_id = data["row_id"]
        self.game_id = data["game_id"]
        self.player_id = data["player_id"]
        self.name_eng = data["name_eng"]
        self.name_rus = data["name_rus"]

        self.gold = data["gold"]
        self.title = data["title"]
        self.body_points = data["body_points"]
        self.authority = data["authority"]

        self.main_settlement = data["main_settlement"]
        self.main_province = data["main_province"]
        self.our_settlements = data["our_settlements"]

        self.armies = data["armies"]  # our_armies

        self.win_points = data["win_points"]

        # TODO убрать. Сейчас как напоминание о том, что где-то будет определяться доступные постройки
        # Список доступных для строительства построек
        # !!!!!!! Это нужно не сохранять, а каждый раз обновлять из класса, мало ли что изменилось
        # self.buildings_available_list = data["buildings_available_list"]

        self.acts = data["acts"]
        self.result_logs_text = data["result_logs_text"]
        self.result_logs_text_all_turns = data["result_logs_text_all_turns"]

        self.end_turn = data["end_turn"]
        self.end_turn_know = data["end_turn_know"]

    # # Функция поиска наших юнитов по нашим поселениям
    # def search_our_units(self):
    #     self.our_units = []  # Обновим список
    #     # Перебор по списку наших поселений ["units"]
    #     # print(self.our_settlements)
    #     print("НЕ!!!!!! Ищем юнитов через новую функцию поиска через класс династии.")
    #     # for i in self.our_settlements:
    #     #     # print(self.game.settlements)
    #     #     # print(self.game.settlements_dict)
    #     #     # print(self.game.settlements_dict[str(i)])
    #     #     # print("################################")
    #     #     units = self.game.settlements[self.game.settlements_dict[str(i)]].units
    #     #     for u in units:
    #     #         # print(u)
    #     #         self.our_units.append(u)
    #     # print(f"Наши юниты: {self.our_units}")

    # Возможно для передачи данных на фронтенд можно использовать отдельную функцию
    # Из плюсов возможность собрать более полный данные
    # Из минусов необходимость восстановления классов
    def return_var_to_front(self):
        ...

    def calc_act(self):  # Подсчет одного действия для династии
        """
        Метод берет первое действие игрока и в зависимости от его ид запускает соответствующий метод.

        :return:
        """
        # print(f"Считаем ход для династии: {self.name}")
        # TODO часть действий неактивны, не удаляю с прошлой игры
        if self.acts:
            # 1 индекс это первое по списку действие, первый элемент в списке, оно выполняется и удаляется
            # 2 индекс это индекс с ИД действия, он под индексом 1, под 0 текстовое описание. Начиная с 2 аргументы
            # Передавать ли аргументы в функцию или вытаскивать их уже в самой функции. Попробуем по разному =>
            # Строительство в поселении
            if self.acts[0][1] == 101:
                # self.act_build_colony(self.acts[0][2])  # Тут передадим аргумент
                # Запустим сразу метод у класса поселение
                print(f"Вызываем функцию строительства {self.acts[0][2]}")
                print(f"Тест, проверяем аргументы. Название: {self.acts[0][2]}. Ид поселения: {self.acts[0][3]}")
                self.game.settlements[self.game.settlements_dict[self.acts[0][3]]].act_build(self.acts[0][2])
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)

            # TODO отключен
            elif self.acts[0][1] == 201:
                # self.act_sell_goods(self.acts[0][2], self.acts[0][3], self.acts[0][4])  # И тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)

            # TODO отключен
            elif self.acts[0][1] == 202:  #
                # self.act_sell_all_goods(self.acts[0][2])  # И тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)

            # Раздать деньги населению
            elif self.acts[0][1] == 301:  #
                self.act_donate(self.acts[0][2])  # Передадим аргумент, сумму
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)

            # TODO отключен
            elif self.acts[0][1] == 302:  #
                # self.act_make_donate(self.acts[0][2])
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)

            elif self.acts[0][1] == 401:  # Распустить юниты
                self.act_dismiss_unit(self.acts[0][2])
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)

            elif self.acts[0][1] == 402:  # Тренировать юниты
                self.act_train_unit(self.acts[0][2])
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)

            elif self.acts[0][1] == 403:  # Сформировать армию
                self.act_create_army(self.acts[0][2])
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)

            else:
                print('Записей в акте нет')

    # Подсчет каких либо параметров после обсчета действия игроков. Обязательно выполняется после действий
    # Какие-нибудь налоги или наоборот доп доход
    # Производство товаров будет обрабатываться здесь
    def calc_end_turn_dynasty(self):
        # self.() # Рассчитаем баланс товаров(производство-потребление)
        # TODO Соберем налоги с поселения.
        # print("Соберем налоги с поселения.")
        # print(self.main_settlement)
        # print(self.game.settlements_dict)
        # print(self.game.settlements_dict[self.main_settlement])
        # print(self.game.settlements)
        # print(self.game.settlements[self.game.settlements_dict[self.main_settlement]])
        trade_tax = (
                self.game.settlements[self.game.settlements_dict[self.main_settlement]].gold_traded_for_tax *
                mod.TRADE_TAX)
        trade_tax = round(trade_tax, 1)
        self.gold += trade_tax
        self.result_logs_text.append(f"Вы собрали налог с торговли: {trade_tax}")
        self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы собрали налог с торговли: {trade_tax}")
        self.game.all_logs.append(f"{self.name_rus} собрали налог с торговли: {trade_tax}")
        self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                        f"{self.name_rus} собрали налог с торговли: {trade_tax}")

        # Выставим False для параметра подтверждающего отправку хода и получение оповещения о новом ходе
        self.end_turn = False
        self.end_turn_know = False
        self.save_to_file()
        print(f"Функция обработки конца хода")

    # !!!!!!!!!!!! TODO не рабочая функция. Оставляем для примера составления логов
    # def act_build(self, buildings_name):     # 101 id
    #     # !!!!!!! На будущее нужно сделать сверку, доступна ли это постройка для игрока
    #     # Два раза buildings это: 1 = экземпляр класса с постройками, 2 = список построек уже в классе
    #
    #     if self.gold >= self.game.buildings_price[buildings_name]:
    #         self.buildings_list[buildings_name] += 1  # Добавим постройку Династии
    #         self.game.buildings_list[buildings_name] += 1  # И добавим к общему количеству в стране
    #         self.gold -= self.game.buildings_price[buildings_name]
    #
    #         self.result_logs_text.append(f"Вы построили {buildings_name}")
    #         self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы построили {buildings_name}")
    #         self.game.all_logs.append(f"{self.name_rus} построили {buildings_name}")
    #         self.game.all_logs_party.append(f"Ход {self.game.turn}. "
    #                                         f"{self.name_rus} построили {buildings_name}")
    #     else:
    #         self.result_logs_text.append(f"Вы НЕ построили {buildings_name}, не хватило денег.")

    def act_donate(self, summ):     # 301 id.  TODO Возможно надо будет добавить аргумент с ид поселения.
        self.gold = int(self.gold)
        if self.gold >= summ:
            self.gold -= summ  # Заберем деньги у игрока

            # TODO Передадим деньги населению.
            self.game.settlements[self.game.settlements_dict[self.main_settlement]].gold += summ

            # Логи
            self.result_logs_text.append(f"Вы раздали {summ} с.")
            self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы раздали  {summ} с.")
            self.game.all_logs.append(f"{self.name_rus} раздали {summ} с. населению.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"{self.name_rus} раздали {summ} с. населению.")
        else:
            self.result_logs_text.append(f"Вы НЕ раздали {summ} с. населению, не хватило денег.")

    def act_dismiss_unit(self, arg):     # 401 id.  TODO Возможно надо будет добавить аргумент с ид поселения.

        if arg:

            # Логи
            self.result_logs_text.append(f"Вы распустили юниты.")
            self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы распустили юниты.")
            self.game.all_logs.append(f"{self.name_rus} распустили юниты.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"{self.name_rus} распустили юниты.")
        else:
            self.result_logs_text.append(f"Вы НЕ распустили юниты. Хз по какой причине.")

    def act_train_unit(self, arg):     # 402 id.  TODO Возможно надо будет добавить аргумент с ид поселения.
        # TODO Необходима проверка наш ли юнит.
        # Возможно сохранять ид владельца в таблице с юнитами.
        if arg:
            print("Обучение юнитов")
            print(f"arg {arg}")

            db = maindb.get_db()
            dbase402 = FDataBase(db)

            # TODO Тестовая заглушка тренировать ближний бой
            check = dbase402.update_units_in_group(self.game_id, arg, ["melee_skill"], self.our_settlements)

            # Логи
            if check:
                self.result_logs_text.append(f"Вы тренировали юниты.")
                self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы тренировали юниты.")
                self.game.all_logs.append(f"{self.name_rus} тренировали юниты.")
                self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                                f"{self.name_rus} тренировали юниты.")
            else:
                self.result_logs_text.append(f"Вы НЕ тренировали юниты. Хз по какой причине.")
        else:
            self.result_logs_text.append(f"Вы НЕ тренировали юниты. Не получены аргументы.")

    def act_create_army(self, arg):     # 403 id.  TODO Возможно надо будет добавить аргумент с ид поселения.
        # TODO Фактически это не создание армии, а присвоение общего ид пачкам юнитов
        if arg:
            print("Формирование армии.")
            print(f"arg {arg}")

            db = maindb.get_db()
            dbase403 = FDataBase(db)
            # arg[0] это список групп юнитов, его передаем единым аргументом
            param_names = "army"  # столбец с ид армии, к которой присваивается группа юнитов
            # arg[1] это id армии к которой присвоим юнитов

            check = dbase403.set_param_in_units_group(self.game_id, arg, param_names, 0)

            # Логи
            if check:
                self.result_logs_text.append(f"Вы сформировали армию.")
                self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы сформировали армию.")
                self.game.all_logs.append(f"{self.name_rus} сформировали армию.")
                self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                                f"{self.name_rus} сформировали армию.")
            else:
                self.result_logs_text.append(f"Вы НЕ распустили юниты. Хз по какой причине.")
        else:
            self.result_logs_text.append(f"Вы НЕ распустили юниты. Не получены аргументы.")

    def calc_win_points(self):
        # Возьмем по 1 очку за 3000
        win_points = round(self.gold / 3000)

        # Добавим за титул
        win_points += self.title
        self.win_points = win_points

        return win_points

    # Отмена действий. TODO Вторым аргументом количество, все, последний или номер индекса(еще не реализованно)
    def cancel_act(self, what):
        if what == "all":
            self.acts = []
        elif what == "last":
            self.acts.pop(-1)



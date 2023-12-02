# Тут можно взять класс Buildings для взаимодействия
# и заранее созданные экземпляр для сохранения каких либо параметров
import json
import random

import buildings
from goods import Goods
# import pickle
import mod as MOD

wealth_status_names = ["Ужасное", "Низкое", "Среднее", "Хорошее", "Отличное"]


class Settlement:
    def __init__(self, game, game_id, row_id=0, ruler=0, name_rus="default_name", name_eng="default_name", population=1,
                 gold=50):
        self.game = game  # Ссылка на игру
        self.game_id = game_id
        self.row_id = row_id  # row_id возвращается при записи в БД, которая позже нигде не используется
        self.ruler = ruler  # Игрок управляющий поселением, id игрока
        self.name_rus = name_rus
        self.name_eng = name_eng

        # Создаем экземпляр общего класса ресурсов и построек
        # TODO зачем?
        self.goods = Goods()
        self.buildings = buildings.Buildings()  # Класс для взаимодействия
        self.buildings_list = self.buildings.buildings_list  # Список для сохранения
        # Постройки, для вывода на фронт при строительстве.
        self.buildings_cost = self.buildings.buildings_cost  # Список стоимости для сохранения
        self.buildings_icon_name = self.buildings.buildings_icon_name  # Список иконок для сохранения

        # Примерные параметры
        # TODO Население лучше создать как отдельный класс со своими параметрами и методами
        self.population = population
        self.gold = gold  # Запасы золота у населения
        self.wealth = self.gold / self.population  # Благосостояние населения в цифрах
        self.wealth_status = "..."  # Благосостояние населения в значении
        # TODO Размером будет количество населения
        self.max_size = self.population

        # TODO размер торговых операция населения, для подсчета налога у правителя.
        self.gold_traded = 0

        # Отдельные переменные под расчет еды
        self.food = 0  # Тестовая переменная, под хз знает что
        self.balance_food = self.food - self.population  # Баланс еды: еда - население

        # TODO как рассчитать размер поселения
        # Попробуем сделать перебор по экземпляру класса
        self.size = 0
        for k, v in self.buildings.buildings_list.items():
            # print(f"Постройка: {k}, количество {v}")
            # print(f"Постройка: {k}, размер {self.buildings.buildings_size[k]}")
            self.size += self.buildings.buildings_size[k] * self.buildings.buildings_list[k]
        # print(f"Текущий размер поселения {self.size}")

        # Строительство
        # Очки строительства. 1 к 1 за свободный размер поселения и 0.5 к 1 за используемый
        self.build_points = self.population - self.size + self.size * 0.5

        # Логи поселения. Или события, то, что напрямую не зависит от игрока.
        # self.acts = []  # Список действий Это для Династии
        self.result_events_text = []  # Список с текстом событий за прошедший ход
        self.result_events_text_all_turns = []  # Список с текстом событий за всю игру

    def calc_turn(self):
        self.food = 0  # Обнулим запас еды. Производство не накапливается
        # Рассчитаем уровень благосостояния.
        self.wealth = self.gold / self.population
        # if self.wealth >=
        # Посчитаем статус благосостояние, округлив деление на модификатор
        try:
            self.wealth_status = wealth_status_names[round(self.wealth / MOD.WEALTH_STATUS)]
        except IndexError:
            self.wealth_status = "Отличное"
        # TODO Необходимо выполнить проверку управляет ли игрок поселением
        print(f"Рассчитываем производство в {self.name_rus}")
        self.buildings.prod(self)  # Запустим функцию расчета товаров у построек
        self.balance_food = self.food - self.population  # Баланс еды: еда - население. Расчет перед ростом для торговли
        self.pop_trade()  # Расчет торговли населения.

    def calc_end_turn(self):
        # Рост/убыль населения
        self.growth_pop_natural()
        self.growth_pop_migration()
        self.balance_food = self.food - self.population  # Баланс еды: еда - население
        # Пересчитаем очки строительство
        self.build_points = self.population - self.size + self.size * 0.5

        self.save_to_file()
        print(f"Функция обработки конца хода у поселения")

    def pop_trade(self):  # Расчет торговли населения.
        # TODO нужно ввести предварительную переменную трат(доходов) для высчета налога.
        # Торговля едой
        # TODO временно покупка 100% недостатка
        # !!! Торговля едо до роста населения(функция calc_end_turn)
        self.gold += self.balance_food * self.goods.resources_price["Еда"]
        if self.balance_food < 0:
            self.result_events_text.append(f"Население купило {self.balance_food*-1} еды.")
            self.result_events_text_all_turns.append(f"Ход {self.game.turn}. "
                                                     f"Население купило {self.balance_food*-1} еды.")
            self.game.all_logs.append(f"В {self.name_rus} население купило {self.balance_food*-1} еды.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"В {self.name_rus} купило {self.balance_food*-1} еды.")
        elif self.balance_food > 0:
            self.result_events_text.append(f"Население продало {self.balance_food} еды.")
            self.result_events_text_all_turns.append(f"Ход {self.game.turn}. "
                                                     f"Население продало {self.balance_food} еды.")
            self.game.all_logs.append(f"В {self.name_rus} население продало {self.balance_food} еды.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"В {self.name_rus} продало {self.balance_food} еды.")
        # Остальная торговля
        self.gold_traded = 0  # Обнулим расчет прошлого хода
        list_trade_buy = ""  # Составим список чем торговли
        list_trade_sell = ""  # Составим список чем торговли
        for k, v in self.goods.resources_list.items():
            print("Что у нас тут с торговлей")
            print(k, v)
            if v > 0:  # Продажа излишек
                self.gold += v * self.goods.resources_price[k]  # Доход населения
                self.gold_traded += v * self.goods.resources_price[k]  # Счетчик торговли. Всегда +
                if len(list_trade_sell) > 0:
                    list_trade_sell += f", {k}({v})"
                else:
                    list_trade_sell += f"{k}({v})"
            elif v < 0:  # Покупка недостатка
                self.gold -= v * self.goods.resources_price[k]  # Доход населения
                self.gold_traded += v * self.goods.resources_price[k]  # Счетчик торговли. Всегда +
                if len(list_trade_buy) > 0:
                    list_trade_buy += f", {k}({v*-1})"
                else:
                    list_trade_buy += f"{k}({v*-1})"
        # Общий лог покупки
        if len(list_trade_buy) > 0:
            self.result_events_text.append(f"Население покупает: {list_trade_buy}.")
            self.result_events_text_all_turns.append(f"Ход {self.game.turn}. "
                                                     f"Население покупает: {list_trade_buy}.")
            self.game.all_logs.append(f"В {self.name_rus} население покупает: {list_trade_buy}.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"В {self.name_rus} покупает: {list_trade_buy}.")
        # Общий лог продажи
        if len(list_trade_sell) > 0:
            self.result_events_text.append(f"Население продает: {list_trade_sell}.")
            self.result_events_text_all_turns.append(f"Ход {self.game.turn}. "
                                                     f"Население продает: {list_trade_sell}.")
            self.game.all_logs.append(f"В {self.name_rus} население продает: {list_trade_sell}.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"В {self.name_rus} продает: {list_trade_sell}.")

    def growth_pop_natural(self):
        rnd = random.randint(0, 10)
        grown = 5  # TODO тестовый рост в 50% без модификаторов

        # TODO тут только положительный рост, как сделать отрицательный?
        # self.population += 1 if grown > rnd else 0
        if grown > rnd:
            self.population += 1
            self.result_events_text.append(f"Население выросло на 1.")
            self.result_events_text_all_turns.append(f"Ход {self.game.turn}. Население выросло на 1.")
            self.game.all_logs.append(f"В {self.name_rus} население выросло на 1.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"В {self.name_rus} население выросло на 1.")

    def growth_pop_migration(self):
        rnd = random.randint(0, 10)
        grown = 5  # TODO тестовый рост в 50% без модификаторов

        # TODO тут только положительный рост, как сделать отрицательный?
        # self.population += 1 if grown > rnd else 0
        if grown > rnd:
            self.population += 1
            self.gold += 10  # Мигранты приносят с собой немного денег
            # Запись лога через отдельную функцию
            # Не имеет смысла. Строк столько же.
            # Проблема в том, что всегда надо 4 строки, а это не всегда необходимо
            # self.write_log(
            #     f"Миграция 1 ед населения в поселение.",
            #     f"Ход {self.game.turn}. Миграция 1 ед. населения в поселение.",
            #     f"В {self.name_rus} миграция 1 ед. населения.",
            #     f"Ход {self.game.turn}. Миграция 1 ед. населения в поселение {self.name_rus}.")
            self.result_events_text.append(f"Миграция 1 ед населения в поселение.")
            self.result_events_text_all_turns.append(f"Ход {self.game.turn}. Миграция 1 ед населения в поселение.")
            self.game.all_logs.append(f"В {self.name_rus} миграция 1 ед населения.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"Миграция 1 ед населения в поселение {self.name_rus}.")

    # Строительство
    # Вызов функции от игрока(dynasty)
    def act_build(self, buildings_name):  # 101 id

        self.buildings_list[buildings_name] += 1  # Добавим постройку Династии
            # self.game.buildings_list[buildings_name] += 1  # И добавим к общему количеству в стране
            # self.gold -= self.game.buildings_price[buildings_name]
            #
            # self.result_logs_text.append(f"Вы построили {buildings_name}")
            # self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы построили {buildings_name}")
            # self.game.all_logs.append(f"{self.name_rus} построили {buildings_name}")
            # self.game.all_logs_party.append(f"Ход {self.game.turn}. "
            #                                 f"{self.name_rus} построили {buildings_name}")
        # else:
        #     self.result_logs_text.append(f"Вы НЕ построили {buildings_name}, не хватило денег.")

    def save_to_file(self):
        data = {
            "game_id": self.game_id,
            "row_id": self.row_id,

            "ruler": self.ruler,
            "name_rus": self.name_rus,
            "name_eng": self.name_eng,

            # Экземпляры класса не сохраняем
            # "goods": self.goods,
            "buildings_list": self.buildings_list,

            "population": self.population,
            "gold": self.gold,
            "wealth_status": self.wealth_status,
            "wealth": self.wealth,

            # Еда
            "food": self.food,
            "balance_food": self.balance_food,
            # Размер не сохраняем, высчитывается каждый раз при создании
            # "max_size": self.max_size,
            # "size": self.size,

            # Строительство
            "build_points": self.build_points,

            # Строительство, сохранение построек для строительства
            "buildings_cost": self.buildings_cost,
            "buildings_icon_name": self.buildings_icon_name,

            # Логи
            "result_events_text": self.result_events_text,
            "result_events_text_all_turns": self.result_events_text_all_turns,
        }
        # Пишем в pickle.
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{self.game_id}/gameID_{self.game_id}_settlementID_{self.row_id}.viking", 'w') as f:
                json.dump(data, f)
        except FileNotFoundError:
            print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_settlementID_{self.row_id}.viking' не найден")
            return ""

    def load_from_file(self, game_id, row_id):
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{game_id}/gameID_{game_id}_settlementID_{row_id}.viking", 'r') as f:
                data = json.load(f)
                # print(f"Восстанавливаем династию: {data}")
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_settlementID_{row_id}.viking' не найден")
            return ""
        self.game_id = data["game_id"]
        self.row_id = data["row_id"]
        self.ruler = data["ruler"]
        self.name_rus = data["name_rus"]
        self.name_eng = data["name_eng"]

        self.buildings_list = data["buildings_list"]

        self.population = data["population"]
        self.gold = data["gold"]
        self.wealth_status = data["wealth_status"]
        self.wealth = data["wealth"]

        # Еда
        self.food = data["food"]
        self.balance_food = data["balance_food"]

        self.build_points = data["build_points"]

        # Строительство, сохранение построек
        self.buildings_cost = data["buildings_cost"]
        self.buildings_icon_name = data["buildings_icon_name"]

        self.result_events_text = data["result_events_text"]
        self.result_events_text_all_turns = data["result_events_text_all_turns"]

    # Запись лога через отдельную функцию.
    # Не имеет смысла. Строк столько же.
    # Проблема в том, что всегда надо 4 строки, а это не всегда необходимо.
    def write_log(self, our_log, our_log_turn, all_log, all_log_turn):
        self.result_events_text.append(our_log)
        self.result_events_text_all_turns.append(our_log_turn)
        self.game.all_logs.append(all_log)
        self.game.all_logs_party.append(all_log_turn)

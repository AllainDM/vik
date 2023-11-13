# Тут можно взять класс Buildings для взаимодействия
# и заранее созданные экземпляр для сохранения каких либо параметров
import json
import random

import buildings
from goods import Goods
import pickle


class Settlement:
    def __init__(self, game, game_id, row_id=0, ruler=0, name_rus="defaut_name", name_eng="defaut_name", population=1, gold=50):
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

        # Примерные параметры
        # TODO Население лучше создать как отдельный класс со своими параметрами и методами
        self.population = population
        self.gold = gold  # Запасы золота у населения
        # TODO Размером будет количество населения
        self.max_size = self.population

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

        # Логи поселения. Или события, то, что напрямую не зависит от игрока.
        # self.acts = []  # Список действий Это для Династии
        self.result_events_text = []  # Список с текстом событий за прошедший ход
        self.result_events_text_all_turns = []  # Список с текстом событий за всю игру

    def calc_turn(self):
        self.food = 0  # Обнулим запас еды. Производство не накапливается
        # TODO Необходимо выполнить проверку управляет ли игрок поселением
        print(f"Рассчитываем производство в {self.name_rus}")
        self.buildings.prod(self)  # Запустим функцию расчета товаров у построек

    def calc_end_turn(self):
        # Рост/убыль населения
        self.growth_pop_natural()
        self.growth_pop_migration()
        self.balance_food = self.food - self.population  # Баланс еды: еда - население
        self.save_to_file()
        print(f"Функция обработки конца хода у поселения")

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
            self.result_events_text.append(f"Миграция 1 ед населения в поселение.")
            self.result_events_text_all_turns.append(f"Ход {self.game.turn}. Миграция 1 ед населения в поселение.")
            self.game.all_logs.append(f"В {self.name_rus} миграция 1 ед населения.")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"Миграция 1 ед населения в поселение {self.name_rus}.")

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

            # Еда
            "food": self.food,
            "balance_food": self.balance_food,
            # Размер не сохраняем, высчитывается каждый раз при создании
            # "max_size": self.max_size,
            # "size": self.size,

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

        # Еда
        self.food = data["food"]
        self.balance_food = data["balance_food"]

        self.result_events_text = data["result_events_text"]
        self.result_events_text_all_turns = data["result_events_text_all_turns"]

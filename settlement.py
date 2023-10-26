# Тут можно взять класс Buildings для взаимодействия
# и заранее созданные экземпляр для сохранения каких либо параметров
import json

import buildings
from goods import Goods
import pickle


class Settlement:
    def __init__(self, game, game_id, row_id=0, ruler=0, name_rus="defaut_name", name_eng="defaut_name", population=1000, gold=0):
        # self.game_id = game.row_id
        self.game_id = game_id
        self.row_id = row_id  # row_id возвращается при записи в БД, которая позже нигде не используется
        self.ruler = ruler  # Игрок управляющий поселением, id игрока
        self.name_rus = name_rus
        self.name_eng = name_eng

        # Создаем экземпляр общего класса ресурсов и построек
        # TODO зачем?
        self.goods = Goods()
        self.buildings = buildings.Buildings()  # Класс для взаимодействия
        self.buildings_list = buildings.buildings.buildings_list  # Список для сохранения

        # Примерные параметры
        # TODO Население лучше создать как отдельный класс со своими параметрами и методами
        self.population = population
        self.gold = gold  # Запасы золота у населения
        # TODO временно для определения размера возьмем население / 100
        self.max_size = self.population / 100

        # TODO как рассчитать размер поселения
        # Попробуем сделать перебор по экземпляру класса
        self.size = 0
        for k, v in self.buildings.buildings_list.items():
            # print(f"Постройка: {k}, количество {v}")
            # print(f"Постройка: {k}, размер {self.buildings.buildings_size[k]}")
            self.size += self.buildings.buildings_size[k] * self.buildings.buildings_list[k]
        # print(f"Текущий размер поселения {self.size}")

    def calc_turn(self):
        # TODO Необходимо выполнить проверку управляет ли игрок поселением
        self.buildings.prod(self)  # Запустим функцию расчета товаров у построек

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
            # Размер не сохраняем, высчитывается каждый раз при создании
            # "max_size": self.max_size,
            # "size": self.size,
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

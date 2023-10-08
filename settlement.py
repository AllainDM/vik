from buildings import Buildings
from goods import Goods
import pickle


class Settlement:
    def __init__(self, game, row_id, ruler, name_rus, name, population=1000, gold=0):
        self.game_id = game.row_id
        self.row_id = row_id
        self.ruler = ruler  # Игрок управляющий поселением, id игрока
        self.name_rus = name_rus
        self.name = name

        # Создаем экземпляр общего класса ресурсов и построек
        # TODO зачем?
        self.goods = Goods()
        self.buildings = Buildings()

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
            print(f"Постройка: {k}, количество {v}")
            print(f"Постройка: {k}, размер {self.buildings.buildings_size[k]}")
            self.size += self.buildings.buildings_size[k] * self.buildings.buildings_list[k]
        print(f"Текущий размер поселения {self.size}")

    def calc_turn(self):
        # TODO Необходимо выполнить проверку управляет ли игрок поселением
        self.buildings.prod(self)  # Запустим функцию расчета товаров у построек

    def save_to_file(self):
        data = {
            "game_id": self.game_id,
            "row_id": self.row_id,
            "ruler": self.ruler,
            "name_rus": self.name_rus,
            "name": self.name,

            # Экземпляры класса не сохраняем
            # "goods": self.goods,
            # "buildings": self.buildings,

            "population": self.population,
            "gold": self.gold,
            # Размер не сохраняем, высчитывается каждый раз при создании
            # "max_size": self.max_size,
            # "size": self.size,
        }
        # Пишем в pickle.
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{self.game_id}/gameID_{self.game_id}_settlementID_{self.row_id}.viking", 'wb') as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_settlementID_{self.row_id}.viking' не найден")
            return ""

    def load_from_file(self, game_id, row_id):
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{game_id}/gameID_{game_id}_settlementID_{row_id}.viking", 'rb') as f:
                data = pickle.load(f)
                # print(f"Восстанавливаем династию: {data}")
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_settlementID_{row_id}.viking' не найден")
            return ""
        self.game_id = data["game_id"]
        self.row_id = data["row_id"]
        self.ruler = data["ruler"]
        self.name_rus = data["name_rus"]
        self.name = data["name"]

        self.population = data["population"]
        self.gold = data["gold"]

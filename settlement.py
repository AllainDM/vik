from buildings import Buildings
from goods import Goods


class Settlement:
    def __init__(self, game, row_id, ruler, name_rus, name, population=100, gold=0):
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

        # TODO как рассчитать размер поселения
        # Попробуем сделать перебор по экземпляру класса
        self.size = 0
        for b in self.buildings.buildings_list:
            print(f"Постройка: {b}")

    def calc_turn(self):
        # TODO Необходимо выполнить проверку управляет ли игрок поселением
        self.buildings.prod(self)  # Запустим функцию расчета товаров у построек

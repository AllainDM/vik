from buildings import Buildings
from goods import Goods


class Settlement:
    def __init__(self, game, name, name_rus, population=100, gold=0):
        self.name = name
        self.name_rus = name_rus

        # Создаем экземпляр общего класса ресурсов и построек
        self.goods = Goods()
        self.buildings = Buildings()

        # Примерные параметры
        # TODO Население лучше создать как отдельный класс со своими параметрами и методами
        self.population = population
        self.gold = gold  # Запасы золота у населения

    def calc_turn(self):
        self.buildings.prod(self)  # Запустим функцию расчета товаров у построек

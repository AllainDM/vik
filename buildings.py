# Что удобнее просто брать цену из класса или использовать функцию возврата цены
class Buildings:
    def __init__(self):
        # Словарь с ценами построек
        self.resources_price = {
            'Гавань': 200,
            'Лесорубка': 200,
        }
        # Количество построек в поселении
        self.buildings_list = {
            'Гавань': 0,
            'Лесорубка': 0,
        }
        # Просто список с названиями построек
        self.resources_name_list = [
            'Гавань',
            'Лесорубка',
        ]

    # Производство товаров
    def prod(self, settlement):
        # Пристань
        # +2 рыба и -1 дерево(типо на лодки)
        settlement.goods.resources_list["Рыба"] += self.buildings_list["Гавань"] * 2
        settlement.goods.resources_list["Дерево"] -= self.buildings_list["Гавань"] * 1

        # Лесорубки
        # +2 дерево
        settlement.goods.resources_list["Дерево"] += self.buildings_list["Лесорубка"] * 2

    # TODO методы из Торговца, пока оставим тут
    # def cost(self, build):
    #     return self.buildings_cost[build]

    # # Получить список доступных построек. По каким либо определенным параметрам отдельного игрока(страны)
    # # Пока передается весь список
    # # И чисто экспериментом у Баркидов не доступно поле
    # def buildings_available(self, dynasty):
    #     available_list = []
    #     for i in self.buildings_name_list:
    #         if dynasty == 'Barkid111' and i == 'Поля(Зерно)':
    #             continue
    #         available_list.append(i)
    #     return available_list


buildings = Buildings()

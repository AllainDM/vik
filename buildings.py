# Что удобнее просто брать цену из класса или использовать функцию возврата цены
class Buildings:
    def __init__(self):
        # Словарь с ценами построек
        self.buildings_price = {
            'Гавань': 200,
            'Лесорубка': 200,
        }
        # Количество построек в поселении
        self.buildings_list = {
            'Гавань': 1,
            'Лесорубка': 0,
        }
        # Просто список с названиями построек
        self.buildings_name_list = [
            'Гавань',
            'Лесорубка',
        ]
        # Размер построек(требования населения)
        self.buildings_size = {
            'Гавань': 0.2,
            'Лесорубка': 0.5,
        }
        # Стоимость в очках строительства
        self.buildings_cost = {
            'Гавань': 1,
            'Лесорубка': 1,
        }

        # Название иконки для фронта
        self.buildings_icon_name = {
            'Гавань': "Small_Harbor.png",
            'Лесорубка': "Logging_Camp.png",
        }

    # Производство товаров
    def prod(self, settlement):
        print(f"Рассчитываем производство в {settlement}")
        # Пристань
        # +2 еда +2 рыба и -1 дерево(типо на лодки)
        settlement.food += self.buildings_list["Гавань"] * 4
        settlement.goods.resources_list["Рыба"] += self.buildings_list["Гавань"] * 4
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

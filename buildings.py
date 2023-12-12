# Что удобнее просто брать цену из класса или использовать функцию возврата цены
class Buildings:
    def __init__(self):
        # Словарь с ценами построек
        self.buildings_price = {
            'Рыбацкая_пристань': 200,
            'Огород': 200,
            'Пастбище(овцы)': 200,
            'Лесорубка': 200,
            'Угодье': 200,

            'Длинный_дом': 200,
        }
        # Количество построек в поселении
        self.buildings_list = {
            'Рыбацкая_пристань': 1,
            'Огород': 0,
            'Пастбище(овцы)': 0,
            'Лесорубка': 0,
            'Угодье': 0,

            'Длинный_дом': 0,
        }
        # Просто список с названиями построек
        self.buildings_name_list = [
            'Рыбацкая_пристань',
            'Огород',
            'Пастбище(овцы)',
            'Лесорубка',
            'Угодье',

            'Длинный_дом',
        ]

        # Размер построек(требования населения)
        self.buildings_size = {
            'Рыбацкая_пристань': 1,
            'Огород': 1,
            'Пастбище(овцы)': 1,
            'Лесорубка': 1,
            'Угодье': 1,

            'Длинный_дом': 1,
        }
        # Стоимость в очках строительства
        self.buildings_cost = {
            'Рыбацкая_пристань': 1,
            'Огород': 1,
            'Пастбище(овцы)': 1,
            'Лесорубка': 1,
            'Угодье': 1,

            'Длинный_дом': 1,
        }

        # Название иконки для фронта
        self.buildings_icon_name = {
            'Рыбацкая_пристань': "Fishermen_House.png",
            'Огород': "Vegetable_Garden.png",
            'Пастбище(овцы)': "Vegetable_Garden.png",
            'Лесорубка': "Logging_Camp.png",
            'Угодье': "Hunt.png",

            'Длинный_дом': "Longhouses.png",
        }

        # Описание. Временно используем как подсказка о производительности
        self.buildings_description = {
            'Рыбацкая_пристань': "+4 еда(рыба). -1 дерево",
            'Огород': "+1 еда(овощи)",
            'Пастбище(овцы)': "+1 нихуя",
            'Лесорубка': "+2 дерево",
            'Угодье': "+2 меха",

            'Длинный_дом': "-1 меха",
        }
        #  Будут какие-то бонусы связанные с наймом войск.

        # TODO тут будет новые словари с потреблениями и производством ресурсов

    # Производство товаров
    def prod(self, settlement):
        print(f"Рассчитываем производство в {settlement}")
        # Пища
        settlement.food = 0
        # Рыбацкая пристань
        # +2 еда +2 рыба и -1 дерево(типо на лодки)
        settlement.food += settlement.buildings_list["Рыбацкая пристань"] * 4
        settlement.goods.resources_list["Рыба"] += settlement.buildings_list["Рыбацкая пристань"] * 4
        settlement.goods.resources_list["Дерево"] -= settlement.buildings_list["Рыбацкая пристань"] * 1
        # Огород
        settlement.food += settlement.buildings_list["Огород"] * 1
        settlement.goods.resources_list["Овощи"] += settlement.buildings_list["Огород"] * 1

        # Лесорубки
        # +2 дерево
        settlement.goods.resources_list["Дерево"] += settlement.buildings_list["Лесорубка"] * 2

        # Угодье. +2 меха
        settlement.goods.resources_list["Меха"] += settlement.buildings_list["Угодье"] * 2

        # Длинный дом. -1 меха
        settlement.goods.resources_list["Меха"] -= settlement.buildings_list["Длинный дом"] * 1

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

class Goods:
    def __init__(self):
        # Словарь с ценами ресурсов
        self.resources_price = {
            'Рыба': 200,
            'Дерево': 200,
        }
        # Количество ресурсов в поселении
        self.resources_list = {
            'Рыба': 0,
            'Дерево': 0,
        }
        # Просто список с названиями ресурсов
        self.resources_name_list = [
            'Рыба',
            'Дерево',
        ]
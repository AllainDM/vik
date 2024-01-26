# Класс провинции для общей торговли и прочего.
import json

from goods import available_province_goods
from settlement import Settlement


class Province:
    """Создание провинции. Объединяет поселения. Тут хранится общая торговля"""
    def __init__(self, game, game_id, row_id=0, name_rus="default_name", name_eng="default_name"):
        self.game = game  # Ссылка на игру
        self.game_id = game_id
        self.row_id = row_id  # Ид для отношений с поселениями

        self.name_rus = name_rus
        self.name_eng = name_eng

        self.dict_settlements = {}  # Словарь поселений в провинции для восстановления

        # Доступные товары. Экспортируем актуальный список из заранее созданного экземпляра класса.
        self.available_goods = available_province_goods.resources_list

    def restore_settlements(self):  # , game_id , settlement_id, name_eng
        """Восстановление поселений из класса провинции."""
        print("Восстановление поселений из класса провинции.")
        # self.game.settlements[name_eng] = Settlement(province=self, game=self.game, game_id=game_id)
        # self.game.settlements[name_eng].load_from_file(game_id, settlement_id)
        # print(f"Восстановлено поселение: {self.game.settlements[name_eng].name_eng}")
        for k, v in self.dict_settlements.items():
            self.game.settlements[v] = Settlement(province=self, game=self.game, game_id=self.game_id)
            self.game.settlements[v].load_from_file(self.game_id, k)
            print(f"Восстановлено поселение: {self.game.settlements[v].name_eng}")

    def save_to_file(self):
        data = {
            "game_id": self.game_id,
            "row_id": self.row_id,

            "name_rus": self.name_rus,
            "name_eng": self.name_eng,

            "dict_settlements": self.dict_settlements,

            # "available_goods": self.available_goods,

        }
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{self.game_id}/gameID_{self.game_id}_provinceID_{self.row_id}.viking", 'w') as f:
                json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
        except FileNotFoundError:
            print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_provinceID_{self.row_id}.viking' не найден")
            return ""

    def load_from_file(self, game_id, row_id):
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{game_id}/gameID_{game_id}_provinceID_{row_id}.viking", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_provinceID_{row_id}.viking' не найден")
            return ""

        self.game_id = data["game_id"]
        self.row_id = data["row_id"]

        self.name_rus = data["name_rus"]
        self.name_eng = data["name_eng"]

        self.dict_settlements = data["dict_settlements"]

        # self.available_goods = data["available_goods"]

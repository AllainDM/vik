import json


class Army:
    """Армия, тут будут храниться пачки юнитов, для дальнейшего использования."""
    def __init__(self, game, row_id, game_id, player_id, name_eng="army", name_rus="армия"):
        self.game = game  # Ссылка на мир для взаимодействия.

        self.row_id = row_id
        self.game_id = game_id

        self.player_id = player_id  # id игрока владельца(или династии?)
        self.name_eng = name_eng            # Имя армии на английском
        self.name_rus = name_rus    # Имя армии на русском

        self.units = []  # Список с юнитами

        self.mid_param = []  # Среднее значение по юнитам для вывода на фронтенд.

    def calc_mid(self):
        # TODO возможно первым элементов в списке units будет какая-то общая инфа
        # Так же в самом юните последний элемент это имя
        # Если есть хоть один юнит(или 2 если первый элемент не общая инфа)
        if self.units[1]:
            # Перебор по количеству параметров
            for p in range(len(self.units[1])-1):  # -1 это не считая последний элемент(имя)
                parameter = 0
                for unit in self.units:
                    parameter += unit[p]
                    parameter = parameter/len(self.units)
                self.mid_param.append(parameter)
            print(f"Средние параметры армии {self.mid_param}")

    def save_to_file(self):
        data = {
            "row_id": self.row_id,
            "game_id": self.game_id,

            "player_id": self.player_id,
            "name_eng": self.name_eng,
            "name_rus": self.name_rus,

            "units": self.units,
        }
        # Пишем в json
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}_armyID_{self.row_id}.viking", 'w') as f:
                json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
        except FileNotFoundError:
            print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}_armyID_{self.row_id}.viking' не найден")
            return ""

    def load_from_file(self, game_id, player_id):
        # Тут нужно отловить ошибку отсутствия файла
        # json
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player_id}_armyID_{self.row_id}.viking", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player_id}_armyID_{self.row_id}.viking' не найден")
            return ""

        self.row_id = data["row_id"]
        self.game_id = data["game_id"]

        self.player_id = data["player_id"]
        self.name_eng = data["name_eng"]
        self.name_rus = data["name_rus"]

        self.units = data["units"]

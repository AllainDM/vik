

class Army:
    """Армия. Не вижу необходимости в этом классе. Но нужно найти это необходимость."""
    def __init__(self, game, row_id, game_id, player_id=0, name_eng="army", name_rus="армия"):
        self.game = game  # Ссылка на мир для взаимодействия.

        self.row_id = row_id
        self.game_id = game_id

        self.ruler = player_id  # id игрока владельца(или династии?)
        self.location = 0  # Месторасположение

        self.hp_max = 0
        self.hp_cur = 0
        self.endurance_max = 0
        self.endurance_cur = 0

        self.name_eng = name_eng    # Имя армии на английском
        self.name = name_rus    # Имя армии на русском


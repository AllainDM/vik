# Модуль рассчета боя
import maindb
from FDataBase import FDataBase


def battle(game_id, inv_army, target_id):
    """
    В нападении принимает участие поко только одна армия, но мы можем передавать и список
    :param game_id:
    :param inv_army:
    :param target_id:
    :return:
    """
    print(f"Армия вторжения: {inv_army}")
    print(f"Целевая провинция: {target_id}")
    # id всех армий нападения. Обязательно собрать список с ид.
    req_army_a = []
    for a in inv_army:
        req_army_a.append(a[0])  # Добавим первый элемент, это ид армии.
    print(f"id армии вторжения: {req_army_a}")

    db = maindb.get_db()
    dbase404 = FDataBase(db)
    # req_army_a = [1, 2, 3]
    # units_group_a = dbase404.get_all_our_units(game_id, req_army_a, "army")
    units_group_a = dbase404.get_all_our_units(game_id, req_army_a[0], "army")
    print(f"units_group_a {units_group_a}")

    return "Неизвестен."


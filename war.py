# Модуль рассчета боя
import random

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
    # units_group_a = dbase404.get_all_our_units(game_id, req_army_a[0], "army")
    group_a = dbase404.get_all_our_units(game_id, 1, "army")
    print(f"units_group_a {group_a}")
    print("Выведем войска по циклу:")
    units_group_a = []  # Список со словарями каждого юнита
    # TODO сделать парамерт живой или мертвый для отметки в бд, чтобы не удалять
    dead_id_units_in_group_a = set()  # Список с ид убитых юнитов(для удаления с бд)
    for u_group in group_a:
        for unit in u_group[1]:
            print(unit)
            units_group_a.append(unit)  # Обьединим всех юнитов всех групп в один список.
    # Тестим два раунда боя, для правильного удаления юнитов.
    # Не идем по циклу с конца, ибо не факт, что этот вариант подойдет для боевки
    for round in range(1, 3):
        print("######################")
        print(f"Раунд: {round}")
        for unit in units_group_a:
            unit["hp_cur"] -= damage()
            if unit["hp_cur"] <= 0:
                dead_id_units_in_group_a.add(unit["row_id"])
            print(unit)
        units_group_a = [u for u in units_group_a if u["hp_cur"] > 0]
        print("Юниты после раунда:")
        print(units_group_a)
    print("Потери:")
    print(dead_id_units_in_group_a)
    dead_in_group_a = f"Потери атакующей армии: {len(dead_id_units_in_group_a)}"
    dead_in_group_b = f"Потери атакующей армии: Неизвестно"

    return f"{dead_in_group_a}. {dead_in_group_b}"  
  

def damage():
    return random.randint(0, 3)
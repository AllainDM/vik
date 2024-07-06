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
    print(f"id армий вторжения: {req_army_a}")

    db = maindb.get_db()
    dbase404 = FDataBase(db)
    # req_army_a = [1, 2, 3]
    # units_group_a = dbase404.get_all_our_units(game_id, req_army_a, "army")
    # units_group_a = dbase404.get_all_our_units(game_id, req_army_a[0], "army")
    # req_army_a[0] это ид атакующей армии
    # TODO у нас еще не сформированы армии и как заглушка передаем home_id
    group_a = dbase404.get_all_our_units(game_id, req_army_a[0], "army")
    print(f"units_group_a {group_a}")
    print("Выведем войска по циклу, атакующая армия:")
    units_group_a = []
    for u_group in group_a:
        for unit in u_group[1]:
            print(unit)
            units_group_a.append(unit)  # Обьединим всех юнитов всех групп в один список.

    db = maindb.get_db()
    dbase404 = FDataBase(db)
    # Защищающаяся армия.
    group_d = dbase404.get_all_our_units(game_id, target_id, "army")
    # group_d = dbase404.get_all_our_units(game_id, [str(target_id), str(target_id)], "home_location")
    units_group_d = []
    print("Выведем войска по циклу, защищающаяся армия:")
    for u_group in group_d:
        for unit in u_group[1]:
            print(unit)
            units_group_d.append(unit)  # Обьединим всех юнитов всех групп в один список.
    return "Неизвестен."


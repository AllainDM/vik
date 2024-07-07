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
    for arm in inv_army:
        req_army_a.append(arm[0])  # Добавим первый элемент, это ид армии.
    print(f"id армии вторжения: {req_army_a}")

    # Атакующая армия.
    db = maindb.get_db()
    dbase404 = FDataBase(db)
    # TODO у нас еще не сформированы армии и как заглушка передаем home_id
    # TODO бля
    group_a = dbase404.get_all_our_units(game_id, '1', "army")
    # Первый элемент словарь с общими параметрами.
    # !!! Второй элемент это список с юнитами.
    # Необходимо запросить все группы юнитов выбраной армии.
    if not group_a:
        return f"Произошла ошибка при обсчете боя, атакующая армия не найдена."
    units_group_a = []  # Список со словарями каждого юнита

    # TODO сделать парамерт живой или мертвый для отметки в бд, чтобы не удалять
    dead_id_units_in_group_a = set()  # Список с ид убитых юнитов(для удаления с бд)

    print(f"group_a {group_a}")
    # print("Выведем войска по циклу, атакующая армия:")
    for one_list_group in group_a:
        units_group_a += one_list_group[1]  # Второй элемент это список с юнитами.
    print(f"units_group_a {units_group_a}")

    # Защищающаяся армия.
    db = maindb.get_db()
    dbase404 = FDataBase(db)
    # TODO на текущий момент у обороняющей стороны берутся юниты с местной локацией
    group_b = dbase404.get_all_our_units(game_id, str(target_id), "home_location")
    # if not group_b:
    #     return f"Тут не совсем ошибка, просто защищающаяся армия не найдена."
    units_group_b = []

    # TODO сделать парамерт живой или мертвый для отметки в бд, чтобы не удалять
    dead_id_units_in_group_b = set()  # Список с ид убитых юнитов(для удаления с бд)

    print(f"units_group_b {group_b}")
    # print("Выведем войска по циклу, защищающаяся армия:")
    for one_list_group in group_b:
        units_group_b += one_list_group[1]  # Второй элемент это список с юнитами.
    print(f"units_group_a {units_group_a}")

    # Высччитаем ширину фронта и количество юнитов поддержки.
    front_width = (len(units_group_a) + len(units_group_b) - abs(len(units_group_a) - len(units_group_b))) / 2

    support = lambda a, b: a - b if a > b else 0
    support_a = support(len(units_group_a), len(units_group_b))
    support_b = support(len(units_group_b), len(units_group_a))
    print(f"Поддержка а: {support_a}")
    print(f"Поддержка b: {support_b}")

    # Бой !!!
    # Отыграем два раунда
    # for round in range(1, 3):
    #     print("######################")
    #     print(f"Раунд: {round}")
    #     for unit in units_group_a:
    #         unit["hp_cur"] -= damage()
    #         if unit["hp_cur"] <= 0:
    #             dead_id_units_in_group_a.add(unit["row_id"])
    #         print(unit)
    #     units_group_a = [u for u in units_group_a if u["hp_cur"] > 0]
    #     print("Юниты после раунда:")
    #     print(units_group_a)

    print("Потери:")
    print(dead_id_units_in_group_a)
    dead_in_group_a = f"Потери атакующей армии: {len(dead_id_units_in_group_a)}"
    dead_in_group_b = f"Потери атакующей армии: {len(dead_id_units_in_group_b)}"

    return f"{dead_in_group_a}. {dead_in_group_b}"
    # return "Неизвестен."


def damage():
    return random.randint(0, 3)

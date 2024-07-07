# Модуль рассчета боя
import random

import maindb
from FDataBase import FDataBase


def battle(game_id, inv_army, target_id):
    """
    В нападении принимает участие поко только одна армия, но мы можем передавать и список.
    1. Определение армий(хз).
    2. Получение юнитов атакующей армии.
    3. Получение юнитов защищающейся армии.
    4. Расчет ширины фронта и количество юнитов поддержки.
    5. Бой.
    6. Сбор текстовой информации для игроков.
    :param game_id:
    :param inv_army:
    :param target_id:
    :return:
    """

    # Пункт 1. Определение армий(хз)
    print(f"Армия вторжения: {inv_army}")
    print(f"Целевая провинция: {target_id}")
    # id всех армий нападения. Обязательно собрать список с ид.
    req_army_a = []
    for arm in inv_army:
        req_army_a.append(arm[0])  # Добавим первый элемент, это ид армии.
    print(f"id армии вторжения: {req_army_a}")

    # Пункт 2. Получение юнитов атакующей армии.
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

    # Пункт 3. Получение юнитов защищающейся армии.
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
    print(f"units_group_b {units_group_b}")

    # Пункт 4. Расчет ширины фронта и количество юнитов поддержки.
    # Высчитаем ширину фронта и количество юнитов поддержки.
    front_width = (len(units_group_a) + len(units_group_b) - abs(len(units_group_a) - len(units_group_b))) / 2

    support = lambda a, b: a - b if a > b else 0
    support_a = support(len(units_group_a), len(units_group_b))
    support_b = support(len(units_group_b), len(units_group_a))
    print(f"Поддержка а: {support_a}")
    print(f"Поддержка b: {support_b}")

    # Пункт 5. Бой.
    # Бой !!!
    # Отыграем два раунда.
    # TODO необходимо пересчитать все выше вначале каждого раунда.
    for round in range(1, 3):
        # TODO по хорошему перетасовывать юнитов вначале раунда.
        print("######################")
        print(f"Раунд: {round}")
        for u in range(int(front_width)):  # Преобразовали float
            # Рассчет бонусов
            bonus_a = 0
            bonus_b = 0
            if units_group_a[u]["agility"] > units_group_b[u]["agility"]:
                bonus_a += 1
            elif units_group_a[u]["agility"] < units_group_b[u]["agility"]:
                bonus_b += 1
            if u < support_a:  # Поддержку определяем как индекс юнита меньше количества поддержки
                bonus_a += 1
            if u < support_b:  # Новое условие, поддержка может быть у обеих армий.
                bonus_b += 1

            # Рассчет рейтинга атаки(просто атаки)
            attack_a = (units_group_a[u]["melee_skill"] +
                        bonus_a +
                        units_group_a[u]["endurance_cur"] - 2 +
                        damage())
            attack_b = (units_group_b[u]["melee_skill"] +
                        bonus_b +
                        units_group_b[u]["endurance_cur"] - 2 +
                        damage())
            if attack_a > attack_b:
                dam = units_group_a[u]["strength"] + units_group_a[u]["melee_weapon"] + damage()
                def_ = units_group_b[u]["armor"] + damage()
                units_group_b[u]["hp_cur"] = (def_ - dam) / 2
                units_group_b[u]["endurance_cur"] = (def_ - dam) / 2
            elif attack_a < attack_b:
                dam = units_group_b[u]["strength"] + units_group_b[u]["melee_weapon"] + damage()
                def_ = units_group_a[u]["armor"] + damage()
                units_group_a[u]["hp_cur"] = (def_ - dam) / 2
                units_group_a[u]["endurance_cur"] = (def_ - dam) / 2
            if units_group_a[u]["hp_cur"] <= 0:
                dead_id_units_in_group_a.add(units_group_a[u]["row_id"])
            if units_group_b[u]["hp_cur"] <= 0:
                dead_id_units_in_group_b.add(units_group_b[u]["row_id"])

            # Рассчет урона.

            print(f"Скилл attack_a: {attack_a}")
            print(f"Скилл attack_b: {attack_b}")


    #     for unit in units_group_a:
    #         unit["hp_cur"] -= damage()
    #
    #         print(unit)
    #     units_group_a = [u for u in units_group_a if u["hp_cur"] > 0]
    #     print("Юниты после раунда:")
    #     print(units_group_a)

    # Пункт 6. Сбор текстовой информации для игроков.
    print("Потери:")
    print(dead_id_units_in_group_a)
    dead_in_group_a = f"Потери атакующей армии: {len(dead_id_units_in_group_a)}"
    dead_in_group_b = f"Потери атакующей армии: {len(dead_id_units_in_group_b)}"

    return f"{dead_in_group_a}. {dead_in_group_b}"
    # return "Неизвестен."


def damage():
    # rnd = random.randint(0, 3)
    # print(f"rnd {rnd}")
    # return rnd
    return random.randint(0, 3)

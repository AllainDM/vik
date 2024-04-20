from datetime import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        pass

    def get_all_user(self):  # На будущее надо как то передавать ИД игры в которой участвует игрок.
        try:
            self.__cur.execute(f"SELECT * FROM users")
            res = self.__cur.fetchall()
            if not res:
                print("Users not found")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска пользователей в БД", _ex)

        return False

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE row_id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска пользователя в БД", _ex)

        return False

    # Добавить сообщение в фидбек
    def add_feedback(self, mess, user_id, user_name):
        try:
            # Пока без даты, надо модифицировать таблицу
            date = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M")  # Дата: день, часы, минуты
            self.__cur.execute("INSERT INTO feedback (message, user_id, user_name, date) VALUES(%s, %s, %s, %s)",
                               (mess, user_id, user_name, date))
            self.__db.commit()
            print(f"Добавилось? id:{user_id} name: {user_name} text: {mess} date: {date}")
        except Exception as _ex:
            print("Ошибка добавления данных в БД 1", _ex)
            return False

        return True

    def add_game(self, turn, year, players, cur_num_players, max_players, is_active=1, the_end=0):
        try:
            # Пока без даты, надо модифицировать таблицу
            date_create = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты
            self.__cur.execute("INSERT INTO games (is_active, the_end, turn, year, "
                               "players, cur_num_players, max_players, "
                               "date_create) "
                               "VALUES(%s, %s, %s, %s, %s, %s, %s, %s) "
                               "RETURNING row_id",
                               (is_active, the_end, turn, year, players, cur_num_players, max_players, date_create))
            # Вернем ид записи
            row_id = self.__cur.fetchone()[0]
            self.__db.commit()
            print(f"Добавление игры в БД. turn:{turn} year: {year} players: {players} "
                  f"date_create: {date_create}")
            return row_id
        except Exception as _ex:
            print("Ошибка добавления данных в БД 2", _ex)
            return False
        # Если все норм, то запрос возвращает ид записи, выше
        # return True

    def add_settlement(self, game_id, name_eng="default_name", name_rus="поселение", ruler=0):
        try:
            # Пока без даты, надо модифицировать таблицу
            date_create = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты
            self.__cur.execute("INSERT INTO settlements (game_id, name_eng, name_rus, ruler, date_create) "
                               "VALUES(%s, %s, %s, %s, %s) "
                               "RETURNING row_id",
                               (game_id, name_eng, name_rus, ruler, date_create))
            # Вернем ид записи
            row_id = self.__cur.fetchone()[0]
            self.__db.commit()
            print(f"Добавилось? game_id:{game_id} name_eng:{name_eng} name_rus: {name_rus} ruler: {ruler}")
            return row_id
        except Exception as _ex:
            print("Ошибка добавления данных в БД 3", _ex)
            return False
        # Если все норм, то запрос возвращает ид записи, выше
        # return True

    def add_group_units(self, game_id, home_location_id, location_id, location_name, name,
                        hp_max, hp_cur, endurance_max, endurance_cur,
                        strength, agility, armor, shield,
                        melee_skill, melee_weapon, ranged_skill, ranged_weapon,
                        experience):
        try:
            self.__cur.execute("INSERT INTO group_units (game_id, home_location_id, location_id, location_name, name,"
                               "hp_max, hp_cur, endurance_max, endurance_cur, "
                               "strength, agility, armor, shield, "
                               "melee_skill, melee_weapon, ranged_skill, ranged_weapon, "
                               "experience) "
                               "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                               "RETURNING row_id",
                               (game_id, home_location_id, location_id, location_name, name,
                                hp_max, hp_cur, endurance_max, endurance_cur,
                                strength, agility, armor, shield,
                                melee_skill, melee_weapon, ranged_skill, ranged_weapon,
                                experience))
            # Вернем ид записи
            row_id = self.__cur.fetchone()[0]
            self.__db.commit()
            print(f"Пачка юнитов добавлена. game_id:{game_id}, row_id:{row_id}, "
                  f"home_location_id:{home_location_id}.")
            return row_id
        except Exception as _ex:
            print("Ошибка добавления данных в БД 5 add_group_units", _ex)
            return False
        # Если все норм, то запрос возвращает ид записи, выше
        # return True

    # Получить пачку юнитов
    def get_units_group(self, home_location_id):
        print("Запрос к БД в получении пачки юнитов (FDataBase.py).")
        try:
            self.__cur.execute(f"SELECT * FROM group_units WHERE home_location_id = {home_location_id}")

            res_group_units = self.__cur.fetchall()

            if not res_group_units:
                print("Group_units not found")
                return False
            else:
                print(f"Выведем все полученные войска (FDataBase.py): {res_group_units}")
                return res_group_units
        except Exception as _ex:
            print("Ошибка поиска юнитов в БД 2", _ex)

    # Получить пачку юнитов
    def get_units_group_dict(self, home_location_id):
        print("Запрос к БД в получении пачки юнитов (FDataBase.py).")
        all_units = []  # Необходимый нам список.
        try:
            # with self.__cur as cursor:
            # Тут ищем пачки юнитов, которые хранят общую инфу
            self.__cur.execute(f"SELECT * FROM group_units WHERE home_location_id = {home_location_id}")

            # Соберем описание колонок
            columns_groups_units = []
            for column in self.__cur.description:
                columns_groups_units.append(column[0].lower())

            res_group_units = self.__cur.fetchall()

            # Нам нужно собрать пачки юнитов, пройдемся по циклу по количеству групп юнитов
            for ug in range(len(res_group_units)):
                res_group_units_dict = {}
                for i in range(len(res_group_units[ug])):
                    res_group_units_dict[columns_groups_units[i]] = res_group_units[ug][i]
                    if isinstance(res_group_units[ug][i], str):
                        res_group_units_dict[columns_groups_units[i]].strip()
                    all_units.append(res_group_units_dict)

            if not res_group_units:
                print("Group_units not found")
                return False
            else:
                print(f"Выведем все полученные войска (FDataBase.py): {all_units}")
                return [all_units]
        except Exception as _ex:
            raise Exception

    # Получить пачку юнитов
    def get_all_our_units(self, list_location_id):
        print("Запрос к БД в получении пачки юнитов (FDataBase.py).")
        all_units = []  # Необходимый нам список.
        try:
            with self.__cur as cursor:
                # Тут ищем пачки юнитов, которые хранят общую инфу
                cursor.execute(f"SELECT * FROM group_units WHERE home_location_id in {tuple(list_location_id)}")

                # Соберем описание колонок
                columns_groups_units = []
                for column in cursor.description:
                    columns_groups_units.append(column[0].lower())

                res_group_units = cursor.fetchall()

                # Нам нужно собрать пачки юнитов, пройдемся по циклу по количеству групп юнитов
                for ug in range(len(res_group_units)):
                    res_group_units_dict = {}
                    for i in range(len(res_group_units[ug])):
                        res_group_units_dict[columns_groups_units[i]] = res_group_units[ug][i]
                        if isinstance(res_group_units[ug][i], str):
                            res_group_units_dict[columns_groups_units[i]].strip()
                    try:
                        cursor.execute(f"SELECT * FROM units WHERE units_group_id = {res_group_units[ug][0]}")
                        res_all_units = cursor.fetchall()

                        # Соберем описание колонок
                        columns_units = []
                        for column in cursor.description:
                            columns_units.append(column[0].lower())

                        units_list = []  # Список со словарями для добавления в общий список
                        for u in range(len(res_all_units)):
                            units_dict = {}
                            for i in range(len(res_all_units[u])):
                                units_dict[columns_units[i]] = res_all_units[u][i]
                                if isinstance(res_all_units[u][i], str):
                                    units_dict[columns_units[i]] = res_all_units[u][i].strip()
                            units_list.append(units_dict)

                        # Первый элемент общая инфа, второй список с юнитами.
                        group_units = [res_group_units_dict, units_list]

                        # Добавим собранную группу юнитов в общий список для ответа фронту.
                        all_units.append(group_units)

                    except Exception as _ex:
                        print("Ошибка поиска юнитов в БД 1", _ex)

                if not res_group_units:
                    print("Group_units not found")
                    return False
                else:
                    print(f"Выведем все полученные войска (FDataBase.py): {all_units}")
                    return all_units
        except Exception as _ex:
            # raise Exception
            print("Ошибка поиска юнитов в БД 2", _ex)
        # raise Exception

            # Код для получения словаря вместо кортежа.
            # Остами в нетронутом виде.
            # columns = []
            # for column in self.__cur.description:
            #     columns.append(column[0].lower())
            # units_dict = {}
            # for row in self.__cur:
            #     for i in range(len(row)):
            #         units_dict[columns[i]] = row[i]
            #         if isinstance(row[i], str):
            #             units_dict[columns[i]] = row[i].strip()
            # print(f"columns {columns}")
            # print(f"units_dict {units_dict}")

    def update_average_parameters_units(self, game_id, param):
        print(f"Будем обновлять средние параметры (FDataBase)")
        try:
            for par in param:  # Перебор параметров для обновления
                self.__cur.execute(f"SELECT units_group_id, avg({par}) "
                                   f"FROM units "
                                   f"WHERE game_id = {game_id} "
                                   f"GROUP BY units_group_id")
                avr_param = self.__cur.fetchall()
                for i in avr_param:
                    try:
                        self.__cur.execute(f"UPDATE group_units "
                                           f"SET {par} = {round(i[1])}"
                                           f"WHERE row_id = {i[0]} "
                                           f"")
                        self.__db.commit()  # TODO Может перенести сохранение в другое место???

                    except Exception as _ex:
                        print("Ошибка высчитывания средних параметров в БД 6 calc_average_parameters_units", _ex)

        except Exception as _ex:
            print("Ошибка высчитывания средних параметров в БД 7 calc_average_parameters_units", _ex)

    def calc_average_parameters_units(self, game_id, param):
        print(f"Будем высчитывать средние параметры (FDataBase): {param}")
        all_units = []
        for par in param:
            try:
                self.__cur.execute(f"SELECT units_group_id, avg({par}) "
                                   f"FROM units "
                                   f"WHERE game_id = {game_id} " 
                                   f"GROUP BY units_group_id")
                avr_param = self.__cur.fetchall()
                all_units.append([param, avr_param])
                for result in avr_param:
                    print(result)
                print(f"Высчитываем средние параметры (FDataBase): {avr_param}")

            except Exception as _ex:
                print("Ошибка высчитывания средних параметров в БД 5 calc_average_parameters_units", _ex)
                return False
        print(f"Выведем все средние параметры (FDataBase.py): {all_units}")
        # Не возвращаем, попробуем тут же и обновит данные
        # if not all_units:
        #     print("Group_units not found")
        #     return False
        # else:
        #     print(f"Выведем все средние параметры (FDataBase.py): {all_units}")
        #     return all_units
    def add_unit(self, game_id, units_group_id, hp_max, hp_cur, endurance_max, endurance_cur,
                 strength, agility, armor, shield, melee_skill, melee_weapon, ranged_skill, ranged_weapon,
                 experience, name):
        try:
            self.__cur.execute("INSERT INTO units (game_id, units_group_id, "
                               "hp_max, hp_cur, endurance_max, endurance_cur, "
                               "strength, agility, armor, shield, "
                               "melee_skill, melee_weapon, ranged_skill, ranged_weapon, "
                               "experience, name) "
                               "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                               "RETURNING row_id",
                               (game_id, units_group_id, hp_max, hp_cur, endurance_max, endurance_cur,
                                strength, agility, armor, shield,
                                melee_skill, melee_weapon, ranged_skill, ranged_weapon,
                                experience, name))
            # Вернем ид записи
            row_id = self.__cur.fetchone()[0]
            self.__db.commit()
            # print(f"Новый юнит добавлен. game_id:{game_id}, row_id:{row_id}, units_group_id:{units_group_id}.")
            return row_id
        except Exception as _ex:
            print("Ошибка добавления данных в БД 4 add_unit", _ex)
            return False
        # Если все норм, то запрос возвращает ид записи, выше
        # return True

    def add_player(self, game_id, player_id):  # "Удаление" игры на самом деле просто делает ее не активной
        # Возможно будет смысл сделать и кнопку полного удаления
        # Просто возникла сложность при создании новой игры, если ни одной не создано
        # Типо игра получает ИД 1, а в БД используется порядковый номер
        try:
            self.__cur.execute(f"UPDATE games set players = array_append(players, {player_id}) WHERE row_id = {game_id}")
            self.__db.commit()
            print(f"Игра сделалась НЕ активной?")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    def delete_game(self, game_id):  # "Удаление" игры на самом деле просто делает ее не активной
        # Возможно будет смысл сделать и кнопку полного удаления
        # Просто возникла сложность при создании новой игры, если ни одной не создано
        # Типо игра получает ИД 1, а в БД используется порядковый номер
        try:
            self.__cur.execute(f"UPDATE games set is_active = 0 WHERE row_id = {game_id}")
            self.__db.commit()
            print(f"Игра сделалась НЕ активной?")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    def end_game(self, game_id):  # Окончание игры, можно продолжать играть, победитель определен
        try:
            self.__cur.execute(f"UPDATE games set the_end = 1 WHERE row_id = {game_id}")
            self.__db.commit()
            print(f"Игра окончена")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    def get_all_active_games(self):
        try:
            self.__cur.execute(f"SELECT * FROM games WHERE is_active = 1")
            res = self.__cur.fetchall()
            if not res:
                print("games not found")
                return []  # Вернем пустой список, для возможности добавления в него первого элемента

            return res
        except Exception as _ex:
            print("Ошибка поиска игр в БД", _ex)

        return False

    def get_all_games(self):
        try:
            self.__cur.execute(f"SELECT * FROM games WHERE is_active = 1")
            res = self.__cur.fetchall()
            if not res:
                print("games not found")
                return []  # Вернем пустой список, для возможности добавления в него первого элемента

            return res
        except Exception as _ex:
            print("Ошибка поиска игр в БД", _ex)

        return False

    # Список игр, где еще есть места
    def get_all_not_full_games(self):
        try:
            self.__cur.execute(f"SELECT * FROM games WHERE max_players > cur_num_players")
            res = self.__cur.fetchall()
            if not res:
                print("games not found")
                return []  # Вернем пустой список, для возможности добавления в него первого элемента

            return res
        except Exception as _ex:
            print("Ошибка поиска игр в БД", _ex)

        return False

    def get_user_by_login(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False
            print("Пользователь найден")
            return res

        except Exception as _ex:
            print("Ошибка поиска пользователя в БД", _ex)

        return False

    # Обновить счетчик побед у игрока
    def update_wins(self, user_id):
        print("Функция обновления считчика побед попыталась запуститься")
        try:
            # self.__cur.execute(f"UPDATE games set is_active = 0 WHERE row_id = {game_id}")
            # self.__cur.execute(f"UPDATE users set wins = 1 WHERE row_id = {user_id}")
            self.__cur.execute(f"UPDATE users set wins = wins + 1 WHERE row_id = {user_id}")
            self.__db.commit()
            print(f"Победа засчиталась?")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    def update_win_game(self, game_id):
        print("Функция обновления считчика побед попыталась запуститься")
        try:
            self.__cur.execute(f"UPDATE games set the_end = 1 WHERE row_id = {game_id}")
            self.__db.commit()
            print(f"Партия окончена?")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    # Получить количество побед у игрока
    # Есть общая функция получения инфы про игроков get_all_users, оттуда возьмем количество побед
    # def get_wins(self, user_id):
    #     try:
    #         self.__cur.execute(f"SELECT wins FROM users WHERE row_id = {user_id} LIMIT 1")
    #         res = self.__cur.fetchone()
    #         if not res:
    #             print("User not found")
    #             return False
    #
    #         return res
    #     except Exception as _ex:
    #         print("Ошибка поиска пользователя в БД", _ex)
    #
    #     return False

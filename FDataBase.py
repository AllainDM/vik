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
    def get_units(self, home_location_id):
        print("Запрос к БД в получении пачки юнитов (FDataBase.py).")
        # print(f"home_location_id {home_location_id}")
        # print(type(home_location_id))
        units = []  # Необходимый нам список. Где первый элемент общая инфа из отдельной таблицы.
        try:
            # Тут ищем пачки юнитов, которые хранят общую инфу
            self.__cur.execute(f"SELECT * FROM group_units WHERE row_id = {home_location_id}")
            # print(f"self.__cur.description {self.__cur.description}")
            # print(f"self.__cur.description[0] {self.__cur.description[0]}")

            # Код для получения словаря вместо кортежа
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

            res_group_units = self.__cur.fetchall()
            print(f"res_group_units: {res_group_units}")
            group_units = res_group_units[0][3]  # home_location_id
            print(f"group_units: {group_units}")
            if not res_group_units:
                print("Group_units not found")
                return False
            else:
                units.append(res_group_units[0])
                print(f"units {units}")
                # return res_group_units
                try:
                    self.__cur.execute(f"SELECT * FROM units WHERE units_group_id = {group_units}")
                    res_all_units = self.__cur.fetchall()
                    print(f"res_all_units: {res_all_units}")
                    full_unit = units + res_all_units
                    print(f"full_unit: {full_unit}")
                    if not res_all_units:
                        print("Res_all_units not found")
                        return False
                    return full_unit
                except Exception as _ex:
                    print("Ошибка поиска юнитов в БД 1", _ex)
        except Exception as _ex:
            print("Ошибка поиска юнитов в БД 2", _ex)

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
            print(f"Новый юнит добавлен. game_id:{game_id}, row_id:{row_id}, units_group_id:{units_group_id}.")
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

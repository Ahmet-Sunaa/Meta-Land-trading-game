import datetime

import mysql.connector


class database:
    pass


def connecter():
    cnx = mysql.connector.connect(user='root', password='18436572',
                                  host='127.0.0.1',
                                  database='prolab')
    return cnx


def register(name, surname, pasword):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select *  from start where idstart=1")
        starter_value = cursor.fetchall()

        sql = "INSERT INTO users (name, surname, password, food, item, money, starting_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, surname, pasword, starter_value[0][3], starter_value[0][1], starter_value[0][2],
               datetime.datetime.today())

        cursor.execute(sql, val)
        cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def login(name, surname, pasword):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        sql = "select * from users where not(id_user=1) and name=%s and  surname=%s and password=%s"
        cursor.execute(sql, (name, surname, pasword))
        starter_value = cursor.fetchall()
        cursor.close()
        cnx.close()
        if starter_value == []:
            return [starter_value, False]

        return [starter_value[0], True]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def manager_login(name, surname, pasword):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        sql = "select * from users where id_user=1 and name=%s and  surname=%s and password=%s"
        cursor.execute(sql, (name, surname, pasword))
        starter_value = cursor.fetchall()
        cnx.close()
        if starter_value == []:
            return [starter_value, False]
        return [starter_value[0], True]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def manager_upgrade_starter(item, money, food, area_size, shop_salary, item_salary, emlak_salary, food_price,
                            item_price):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        sql = "TRUNCATE TABLE game_area"
        sql2 = "TRUNCATE TABLE show_coast"
        sql3 = "TRUNCATE TABLE business_salary"
        sql4 = "TRUNCATE TABLE business"
        sql5 = "TRUNCATE TABLE emlak_cost"
        sql6 = "TRUNCATE TABLE komisyon"
        cursor.execute(sql)
        cnx.commit()
        cursor.execute(sql2)
        cnx.commit()
        cursor.execute(sql3)
        cnx.commit()
        cursor.execute(sql4)
        cnx.commit()
        cursor.execute(sql5)
        cnx.commit()
        cursor.execute(sql6)
        cnx.commit()
        cursor.execute("""
           UPDATE start
           SET start_item=%s, start_money=%s, start_food=%s, game_size=%s
           where idstart=%s
           
        """, (item, money, food, str(area_size), 1))
        cursor.execute(
            "INSERT INTO komisyon (id_emlak, emlak_satis_komisyon, emlak_kiralama_komisyon, id_user) VALUES (%s, %s, %s, %s)",
            (1, 0, 0, 1))

        area = int(area_size[0]) * int(area_size[2])
        cnx.commit()
        for i in range(area):
            sql = "INSERT INTO game_area (type_area, area_users_id) VALUES (%s, %s)"
            sql2 = "INSERT INTO show_coast (id_shop_cost, cost, id_owner) VALUES (%s, %s, %s)"
            sql3 = "INSERT INTO business_salary (idbusiness_salary, salary, owner_id) VALUES (%s, %s, %s)"
            sql4 = "INSERT INTO business (idbusiness, level, capacity,total_worker,id_owner) VALUES (%s, %s, %s, %s, %s)"
            sql5 = "INSERT INTO emlak_cost (sold_price, rent_price,owner_id,business_id) VALUES (%s, %s, %s, %s)"
            if i == 0:
                cursor.execute(sql, (1, 1))
                cursor.execute(sql3, (i + 1, emlak_salary, 1))
                cursor.execute(sql4, (i + 1, 3, 99, 0, 1))
                cursor.execute(sql5, (9999, 9999, 1, i + 1))
            elif i == 1:
                cursor.execute(sql, (2, 1))
                cursor.execute(sql2, (i + 1, food_price, 1))
                cursor.execute(sql3, (i + 1, shop_salary, 1))
                cursor.execute(sql4, (i + 1, 3, 99, 0, 1))
                cursor.execute(sql5, (9999, 9999, 1, i + 1))
            elif i == 2:
                cursor.execute(sql, (3, 1))
                cursor.execute(sql2, (i + 1, item_price, 1))
                cursor.execute(sql3, (i + 1, item_salary, 1))
                cursor.execute(sql4, (i + 1, 3, 99, 0, 1))
                cursor.execute(sql5, (9999, 9999, 1, i + 1))
            else:
                cursor.execute(sql, (4, 1))
                cursor.execute(sql5, (200, 9999, 1, i + 1))

            cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def manager_upgrade_daily(item, money, food):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("""
           UPDATE daily_coast
           SET food=%s, money=%s, item=%s
           where iddaily_coast=%s
        """, (item, money, food, 1))
        cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def manager_upgrade_build_cost(emlak, market, supermarket):
    oran = [emlak, market, supermarket]
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        for i in range(3):
            cursor.execute("""
                       UPDATE type_business
                       SET build_cost=%s
                       where idtype_business=%s
                    """, (oran[i], i + 1))

        cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def manager_upgrade_level_cost(first, second, third):
    oran = [first, second, third]
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        for i in range(3):
            cursor.execute("""
                       UPDATE business_level_oran
                       SET oran=%s
                       where id_busines=%s
                    """, (oran[i], i + 1))

        cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def buy_food_item(uid, buy_count, area_id):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "select c.cost, c.id_owner from game_area as g INNER JOIN show_coast as c ON g.idgame_area=%s and g.idgame_area=c.id_shop_cost",
            (area_id[0],))
        cost = cursor.fetchall()
        cursor.execute("select food, item, money from users where id_user=%s", (uid,))
        user_info = cursor.fetchall()

        new_money = int(user_info[0][2]) - (int(buy_count) * int(cost[0][0]))
        if area_id[1] == '2':
            new_food = int(user_info[0][0]) + int(buy_count)
            cursor.execute("""
                      UPDATE users
                      SET food=%s, money=%s
                      where id_user=%s
                   """, (new_food, new_money, uid))
            cnx.commit()
        elif area_id[1] == '3':
            new_item = int(user_info[0][1]) + int(buy_count)
            cursor.execute("""
                      UPDATE users
                      SET item=%s, money=%s
                      where id_user=%s
                   """, (new_item, new_money, uid))
            cnx.commit()

        cnx.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


"""------------------------------------ GET FUNCTİON ----------------------------------------------"""


def getIMF(uid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select food,item,money from users where id_user=%s", (uid,))
        starter_value = cursor.fetchall()
        cnx.close()
        return starter_value[0]
    except mysql.connector.Error as error:
        print("err: {}".format(error))
        return 1


def get_game_area():
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select game_size from start where idstart=1")
        starter_value = cursor.fetchall()
        cursor.close()
        cnx.close()
        if starter_value == []:
            return [starter_value, False]

        return [starter_value[0][0][0], starter_value[0][0][2], True]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_area_type(aid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select * from game_area where idgame_area=%s", (aid,))
        starter_value = cursor.fetchall()
        cursor.close()
        cnx.close()
        if starter_value == []:
            return [starter_value, False]

        return [starter_value[0], True]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_area_owner_tooltip(aid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select * from game_area where idgame_area=%s", (aid,))
        starter_value = cursor.fetchall()
        cursor.execute("select name, surname from users where id_user=%s", (starter_value[0][2],))
        user = cursor.fetchall()
        user = "owner by: " + user[0][0] + " " + user[0][1]
        cursor.close()
        cnx.close()
        return user

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_area_owner(bid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select * from game_area where idgame_area=%s", (bid,))
        starter_value = cursor.fetchall()
        cursor.execute("select name, surname from users where id_user=%s", (starter_value[0][2],))
        user = cursor.fetchall()
        user = user[0][0] + " " + user[0][1]
        cursor.close()
        cnx.close()
        return user

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_shop_price(bid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT c.cost FROM game_area as g INNER JOIN show_coast as c ON g.idgame_area=%s and c.id_owner=g.area_users_id and g.idgame_area=c.id_shop_cost",
            (bid,))
        cost = cursor.fetchall()
        cursor.close()
        cnx.close()
        return cost[0]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_shop_salary(bid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT s.salary FROM game_area as g INNER JOIN business_salary as s ON g.idgame_area=%s and s.owner_id = g.area_users_id and g.idgame_area=s.idbusiness_salary",
            (bid,))
        salary = cursor.fetchall()
        cursor.close()
        cnx.close()
        return salary[0]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_sold_business(bid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT e.sold_price FROM game_area as g INNER JOIN emlak_cost as e ON g.idgame_area=%s and e.owner_id = g.area_users_id and g.idgame_area=e.business_id",
            (bid,))
        sold_price = cursor.fetchall()
        cursor.close()
        cnx.close()
        return sold_price[0]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_all_property():
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT u.id_user, u.name, u.surname, g.idgame_area,t.type FROM game_area as g INNER JOIN users as u ON u.id_user=g.area_users_id INNER JOIN type_business as t ON g.type_area = t.idtype_business")
        starter_value = cursor.fetchall()
        cursor.close()
        cnx.close()
        return starter_value

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_area(uid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT b.idbusiness_salary,t.type,salary,u.id_user,u.name,u.surname FROM business_salary as b INNER JOIN game_area as g ON  g.idgame_area = b.idbusiness_salary INNER JOIN type_business as t ON t.idtype_business=g.type_area INNER JOIN users as u ON u.id_user=b.owner_id where NOT(b.owner_id=%s)",
            (uid,))
        user = cursor.fetchall()
        cursor.close()
        cnx.close()
        return user

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_build_business_price(type_business):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT build_cost FROM type_business where type=%s",
            (type_business,))
        type_business_cost = cursor.fetchall()
        cursor.close()
        cnx.close()
        return type_business_cost[0][0]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_owner_land(uid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT * FROM game_area where area_users_id=%s and type_area=4",
            (uid,))
        user = cursor.fetchall()
        cursor.close()
        cnx.close()
        return user

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


"---------------------------------------SET FUNCTİON-----------------------------------------------"


def set_find_job(bid, uid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("""
           UPDATE users
           SET job_id=%s
           where id_user=%s
        """, (bid, uid[0]))
        cursor.execute("""
                   INSERT INTO busines_start
                   (idbusines_start, worker_id, starting_time) VALUES (%s, %s, %s)
                """, (bid, uid[0], datetime.datetime.today()))
        cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def set_rent_sold(bid, rent_or_sold, uid, days=0, emlak_id=-1, owner=-1):
    if rent_or_sold == 'sold':
        try:
            cnx = connecter()
            cursor = cnx.cursor()
            cursor.execute("SELECT type_area FROM game_area where idgame_area=%s", (bid,))
            b_type = cursor.fetchall()
            if b_type[0][0] == '4':
                cursor.execute(
                    "SELECT u.money, t.idtype_business, k.emlak_satis_komisyon, e.sold_price, u.id_user FROM game_area as g INNER JOIN emlak_cost as e ON  g.idgame_area = %s and e.idemlak_cost = g.idgame_area INNER JOIN komisyon as k ON k.id_emlak=%s INNER JOIN type_business as t ON t.idtype_business=g.type_area INNER JOIN users as u ON u.id_user = %s",
                    (bid, emlak_id, uid))
                sold_info = cursor.fetchall()
                sold_info = sold_info[0]
                cursor.execute(
                    "SELECT u.id_user,u.money FROM game_area as g INNER JOIN users as u ON g.idgame_area=%s and g.area_users_id=u.id_user ",
                    (emlak_id,))
                emlak_info = cursor.fetchall()
                emlak_info = emlak_info[0]
                cursor.execute(
                    "SELECT u.id_user,u.money FROM game_area as g INNER JOIN users as u ON g.area_users_id=u.id_user and g.idgame_area=%s",
                    (bid,))
                owner_id = cursor.fetchall()
                owner_id = owner_id[0]
                print(sold_info)
                print(emlak_info)
                print(owner_id)
                if int(sold_info[0]) < int(sold_info[3]):
                    return False
                else:
                    new_money = int(int(sold_info[0]) - int(sold_info[3]))
                    cursor.execute("""
                        UPDATE users
                        SET money=%s
                        where id_user=%s
                        """, (new_money, uid))
                    cnx.commit()
                    cursor.execute(
                        "SELECT u.id_user,u.money FROM game_area as g INNER JOIN users as u ON g.idgame_area=%s and g.area_users_id=u.id_user ",
                        (emlak_id,))
                    emlak_money = cursor.fetchall()
                    emlak_money = emlak_money[0]

                    cursor.execute("""
                        UPDATE emlak_cost
                        SET owner_id=%s
                        where idemlak_cost=%s
                        """, (uid, bid))

                    cursor.execute("""
                        UPDATE game_area
                        SET area_users_id=%s
                        where idgame_area=%s
                        """, (uid, bid))
                    commition = int(emlak_money[1]) + int((int(sold_info[3]) * int(sold_info[2])) / 100)
                    cursor.execute("""
                        UPDATE users
                        SET money=%s
                        where id_user=%s
                        """, (commition, emlak_info[0]))

                    if owner_id[0] == emlak_info[0]:
                        owner_money = (int(sold_info[3]) + int(owner_id[1]))
                    else:
                        owner_money = (int(sold_info[3]) + int(owner_id[1])) - (
                            int((int(sold_info[3]) * int(sold_info[2])) / 100))

                    cursor.execute("""
                        UPDATE users
                        SET money=%s
                        where id_user=%s
                        """, (owner_money, owner_id[0]))
                    cursor.execute(
                        """INSERT INTO sold (id_emlak, id_owner, id_user, id_busines, date) VALUES (%s, %s, %s, %s, %s)""",
                        (emlak_id, owner_id[0], sold_info[4], bid, datetime.datetime.today()))
                cnx.commit()
            else:
                cursor.execute(
                    "SELECT u.money, t.idtype_business, k.emlak_satis_komisyon, e.sold_price, u.id_user FROM game_area as g INNER JOIN emlak_cost as e ON  g.idgame_area = %s and e.idemlak_cost = g.idgame_area INNER JOIN komisyon as k ON k.id_emlak=%s INNER JOIN type_business as t ON t.idtype_business=g.type_area INNER JOIN users as u ON u.id_user = %s",
                    (bid, emlak_id, uid))
                sold_info = cursor.fetchall()
                sold_info = sold_info[0]
                cursor.execute(
                    "SELECT u.id_user,u.money FROM game_area as g INNER JOIN users as u ON g.idgame_area=%s and g.area_users_id=u.id_user ",
                    (emlak_id,))
                emlak_info = cursor.fetchall()
                emlak_info = emlak_info[0]
                cursor.execute(
                    "SELECT u.id_user,u.money FROM game_area as g INNER JOIN users as u ON g.area_users_id=u.id_user and g.idgame_area=%s",
                    (bid,))
                owner_id = cursor.fetchall()
                owner_id = owner_id[0]
                if int(sold_info[0]) < int(sold_info[3]):
                    return False
                else:
                    new_money = int(int(sold_info[0]) - int(sold_info[3]))
                    cursor.execute("""
                                       UPDATE users
                                       SET money=%s
                                       where id_user=%s
                                       """, (new_money, uid))
                    cnx.commit()
                    cursor.execute(
                        "SELECT u.id_user,u.money FROM game_area as g INNER JOIN users as u ON g.idgame_area=%s and g.area_users_id=u.id_user ",
                        (emlak_id,))
                    emlak_money = cursor.fetchall()
                    emlak_money = emlak_money[0]

                    cursor.execute("""
                                       UPDATE emlak_cost
                                       SET owner_id=%s
                                       where idemlak_cost=%s
                                       """, (uid, bid))

                    cursor.execute("""
                                       UPDATE game_area
                                       SET area_users_id=%s
                                       where idgame_area=%s
                                       """, (uid, bid))
                    commition = int(emlak_money[1]) + int((int(sold_info[3]) * int(sold_info[2])) / 100)
                    cursor.execute("""
                                       UPDATE users
                                       SET money=%s
                                       where id_user=%s
                                       """, (commition, emlak_info[0]))
                    cursor.execute("""
                                       UPDATE show_coast
                                       SET id_owner=%s
                                       where id_shop_cost=%s
                                       """, (uid, bid))
                    cursor.execute("""
                                       UPDATE business_salary
                                       SET owner_id=%s
                                       where idbusiness_salary=%s
                                       """, (uid, bid))
                    cursor.execute("""
                                       UPDATE business
                                       SET id_owner=%s
                                       where idbusiness=%s
                                       """, (uid, bid))
                    if owner_id[0] == emlak_info[0]:
                        owner_money = (int(sold_info[3]) + int(owner_id[1]))
                    else:
                        owner_money = (int(sold_info[3]) + int(owner_id[1])) - (
                            int((int(sold_info[3]) * int(sold_info[2])) / 100))

                    cursor.execute("""
                                       UPDATE users
                                       SET money=%s
                                       where id_user=%s
                                       """, (owner_money, owner_id[0]))
                    cursor.execute(
                        """INSERT INTO sold (id_emlak, id_owner, id_user, id_busines, date) VALUES (%s, %s, %s, %s, %s)""",
                        (emlak_id, owner_id[0], sold_info[4], bid, datetime.datetime.today()))
                    if b_type[0][0] == '1':
                        cursor.execute("""
                                       UPDATE komisyon
                                       SET id_user=%s
                                       where id_emlak=%s
                                       """, (uid, bid))
                cnx.commit()
            cnx.close()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))

    elif rent_or_sold == 'rent':
        try:
            start_day = datetime.date.today()
            finish_day = datetime.date.today() + datetime.timedelta(days=int(days))
            cnx = connecter()
            cursor = cnx.cursor()
            cursor.execute("""
                       INSERT INTO rent
                       (rent_time, rent_date, rent_finish_date, id_emlak, id_user, id_business, id_owner) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (days, start_day, finish_day, emlak_id, uid, bid, owner))
            cnx.commit()
            cursor.close()
            cnx.close()


        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))


def set_emlak_rent_sold_price(bid, sold_price, rent_price):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("""UPDATE emlak_cost SET sold_price=%s,rent_price=%s where business_id=%s """,
                       (sold_price, rent_price, bid))
        cnx.commit()
        cursor.close()
        cnx.close()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def set_build_business(uid, bid, emlak_id, type_business, b_cost):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("SELECT money FROM users where id_user=%s", (uid,))
        u_money = cursor.fetchall()

        if int(u_money[0][0]) < int(b_cost):
            return None
        else:
            u_money = int(u_money[0][0]) - int(b_cost)
            cursor.execute("""
                    UPDATE users
                    SET money=%s
                    where id_user=%s
                    """, (u_money, uid))
            cursor.execute(
                "INSERT INTO business_salary (idbusiness_salary, salary, owner_id, business_level_oran) VALUES (%s, %s, %s, %s)",
                (bid, 0, uid, 1))
            cursor.execute(
                "INSERT INTO business (idbusiness, level, capacity, total_worker, id_owner) VALUES (%s, %s, %s, %s, %s)",
                (bid, 1, 3, 0, uid))
            cursor.execute(
                "INSERT INTO sold (id_emlak, id_owner, id_user, id_busines, date) VALUES (%s, %s, %s, %s, %s)",
                (emlak_id, uid, uid, bid, datetime.datetime.today()))
            cursor.execute(
                "SELECT idtype_business FROM type_business where type=%s",
                (type_business,))
            type_business = cursor.fetchall()

            cursor.execute("""
                    UPDATE game_area
                    SET type_area=%s
                    where idgame_area=%s
                    """, (type_business[0][0], bid))
            cnx.commit()
            if type_business[0][0] != 1:
                cursor.execute(
                    "INSERT INTO show_coast (id_shop_cost, cost, id_owner) VALUES (%s, %s, %s)",
                    (bid, 0, uid))
            else:
                cursor.execute(
                    "INSERT INTO komisyon (id_emlak, emlak_satis_komisyon, emlak_kiralama_komisyon,id_user) VALUES (%s, %s, %s, %s)",
                    (bid, 1, 1, uid))
            cnx.commit()
        cursor.close()
        cnx.close()


    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


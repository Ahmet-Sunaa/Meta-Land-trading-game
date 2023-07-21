import mysql.connector


class database:
    pass


def connecter():
    cnx = mysql.connector.connect(user='root', password='18436572',
                                  host='127.0.0.1',
                                  database='prolab')
    return cnx


def deleted_database():
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("TRUNCATE TABLE users")
        cursor.execute("TRUNCATE TABLE sold")
        cursor.execute("TRUNCATE TABLE rent")
        cursor.execute("TRUNCATE TABLE show_coast")
        cursor.execute("TRUNCATE TABLE komisyon")
        cursor.execute("TRUNCATE TABLE game_area")
        cursor.execute("TRUNCATE TABLE emlak_cost")
        cursor.execute("TRUNCATE TABLE daily_coast")
        cursor.execute("TRUNCATE TABLE business_salary")
        cursor.execute("TRUNCATE TABLE business")
        cursor.execute("TRUNCATE TABLE busines_start")
        cnx.commit()
        cursor.execute("""UPDATE type_business SET build_cost=%s""",
                       (0,))
        cursor.execute("""
                  UPDATE start
                  SET start_item=%s, start_money=%s, start_food=%s, game_size=%s
                  where idstart=%s
               """, (0, 0, 0, '0x0', 1))
        cursor.execute(
            "INSERT INTO users (id_user, name, surname, password, food, item, money, starting_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (1, 'admin', 'admin', 'admin', 999999, 999999, 999999, 999999))
        cursor.execute(
            "INSERT INTO komisyon (id_emlak, emlak_satis_komisyon, emlak_kiralama_komisyon, id_user) VALUES (%s, %s, %s, %s)",
            (1, 0, 0, 1))
        cursor.execute(
            "INSERT INTO daily_coast (iddaily_coast, food, money, item) VALUES (%s, %s, %s, %s)",
            (1, 0, 0, 0))
        cursor.execute(
            "INSERT INTO business_salary (idbusiness_salary, salary, owner_id, business_level_oran) VALUES (%s, %s, %s ,%s)",
            (1, 0, 1, 3))
        cursor.execute(
            "INSERT INTO business_salary (idbusiness_salary, salary, owner_id, business_level_oran) VALUES (%s, %s, %s ,%s)",
            (2, 0, 1, 3))
        cursor.execute(
            "INSERT INTO business_salary (idbusiness_salary, salary, owner_id, business_level_oran) VALUES (%s, %s, %s ,%s)",
            (3, 0, 1, 3))
        cursor.execute(
            "INSERT INTO business (idbusiness, level, capacity, total_worker, id_owner) VALUES (%s, %s, %s, %s, %s)",
            (1, 3, 99, 0, 1))
        cursor.execute(
            "INSERT INTO business (idbusiness, level, capacity, total_worker, id_owner) VALUES (%s, %s, %s, %s, %s)",
            (2, 3, 99, 0, 1))
        cursor.execute(
            "INSERT INTO business (idbusiness, level, capacity, total_worker, id_owner) VALUES (%s, %s, %s, %s, %s)",
            (3, 3, 99, 0, 1))
        cnx.commit()
        cursor.close()
        cnx.close()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_area_owner(aid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select name, surname from users where id_user=%s", (aid,))
        user = cursor.fetchall()
        cursor.close()
        cnx.close()
        return user

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_cost(uid, bid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select type_area from game_area where idgame_area=%s", (bid,))
        type_area = cursor.fetchall()
        if type_area[0][0] != '1':
            cursor.execute("select cost from show_coast where id_owner=%s and id_shop_cost=%s", (uid, bid))
            cost = cursor.fetchall()
            cursor.execute("select salary from business_salary where owner_id=%s and idbusiness_salary=%s", (uid, bid))
            salary = cursor.fetchall()
            cursor.execute("select sold_price, rent_price from emlak_cost where owner_id=%s and business_id=%s", (uid, bid))
            business_price = cursor.fetchall()
            cursor.close()
            cnx.close()
            return [cost[0], salary[0], business_price[0]]

        else:
            cursor.execute("select salary from business_salary where owner_id=%s and idbusiness_salary=%s", (uid, bid))
            salary = cursor.fetchall()
            cursor.execute("select sold_price, rent_price from emlak_cost where owner_id=%s and business_id=%s",
                           (uid, bid))
            business_price = cursor.fetchall()
            cursor.close()
            cnx.close()
            return [salary[0], business_price[0]]
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_area(bid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT u.name, u.surname, g.idgame_area,t.type,g.area_users_id FROM game_area as g INNER JOIN users as u ON u.id_user=g.area_users_id and g.idgame_area=%s INNER JOIN type_business as t ON g.type_area = t.idtype_business",
            (bid,))
        user = cursor.fetchall()
        cursor.close()
        cnx.close()
        return user[0]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_emlak_rent_sold_price(bid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT e.sold_price, e.rent_price,g.type_area FROM emlak_cost as e INNER JOIN game_area as g ON e.business_id = g.idgame_area and e.business_id = %s",
            (bid,))
        user = cursor.fetchall()
        cursor.close()
        cnx.close()
        return user[0]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def get_emlak_commission(bid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT emlak_satis_komisyon, emlak_kiralama_komisyon FROM komisyon as k INNER JOIN game_area as g ON k.id_emlak = g.idgame_area and k.id_emlak = %s",
            (bid,))
        user = cursor.fetchall()
        cursor.close()
        cnx.close()
        return user[0]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))


def set_cost(uid, bid, salary, cost, sold, rent):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute("select type_area from game_area where idgame_area=%s", (bid,))
        btype = cursor.fetchall()
        print('sa')
        if btype[0][0] != '1':

            print('1')
            cursor.execute("""UPDATE show_coast SET cost=%s where id_owner=%s and id_shop_cost=%s""", (cost, uid, bid))
            cursor.execute("""UPDATE business_salary SET salary=%s where owner_id=%s and idbusiness_salary=%s""",
                           (salary, uid, bid))
            cnx.commit()
        else:
            cursor.execute("""UPDATE business_salary SET salary=%s where owner_id=%s and idbusiness_salary=%s""",
                           (salary, uid, bid))
            cnx.commit()

        cursor.execute("""UPDATE emlak_cost SET sold_price=%s, rent_price=%s where owner_id=%s and business_id=%s""",
                       (sold, rent, uid, bid))
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


def set_emlak_commission(sold_c, rent_c, bid, uid):
    try:
        cnx = connecter()
        cursor = cnx.cursor()
        cursor.execute(
            """UPDATE komisyon SET emlak_satis_komisyon=%s, emlak_kiralama_komisyon=%s where id_emlak=%s and id_user=%s""",
            (sold_c, rent_c, bid, uid))
        cnx.commit()
        cursor.close()
        cnx.close()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

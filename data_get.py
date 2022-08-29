import mariadb


def all_result():
    """Zwrócenie danych potrzebnych do wykresu przebiegu temperatury"""

    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        database="automatyka")
    cur = conn.cursor()

    #retrieving information
    # some_name = "Georgi"
    # cur.execute("SELECT first_name,last_name FROM employees WHERE first_name=?", (some_name,))
    cur.execute("SELECT m.temp, m.date_time, c.temp_w FROM measurement as m LEFT JOIN configuration as c ON m.id_config = c.id_config")

    result_json = []

    for temp, date_time, temp_w in cur:
        # formatowanie z usunięciem T
        x = str(date_time)
        x.replace("T", " ")

        result_json.append({"temp":temp, "date_time":x, "temp_s":temp_w})

    conn.close()

    return result_json

def config_result():
    """Zwrócenie aktualnych parametrów"""

    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        database="automatyka")
    cur = conn.cursor()


    cur.execute("SELECT temp_w,temp_e,dimension_x,dimension_y,dimension_z, id_config FROM configuration ORDER BY id_config DESC LIMIT 1")

    result_json = []

    for temp_w,temp_e,dimension_x,dimension_y,dimension_z, id_config  in cur:

        result_json.append({"temp_w":temp_w, "temp_e":temp_e, "dimension_x":dimension_x, "dimension_y":dimension_y, "dimension_z":dimension_z})

    conn.close()

    return result_json
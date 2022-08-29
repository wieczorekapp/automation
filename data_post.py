import mariadb


def config_set(json_data):
    """Dodanie nowej konfiguracji"""

    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        database="automatyka")
    cur = conn.cursor()
    result_json = []

    try:
        cur.execute("INSERT INTO configuration(temp_w,temp_e,dimension_x,dimension_y,dimension_z) VALUES (?,?,?,?,?)",
        (json_data.temp_w,json_data.temp_e,json_data.dimension_x,json_data.dimension_y,json_data.dimension_z))

        result_json.append({"status":"Succes"})
    except mariadb.Error as e:
        result_json.append({"status":"Fail"})

    conn.commit()
    conn.close()

    return result_json
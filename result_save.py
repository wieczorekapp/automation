import mariadb
import time
import math
from datetime import datetime
from decimal import Decimal

POWER = 1000

def db_save_increase():
    """Funkcja symulująca odczyty temperatury przy włączonej grzałce"""

    # parametry połączenia z bazą danych
    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        database="automatyka")
    cur = conn.cursor()

    # pobranie ostatniej temperatury, wymiarów oraz id obecnej konfiguracji
    temp_last = 0.0
    id_config = 0
    d_x = 0
    d_y = 0
    d_z = 0

    cur.execute("SELECT temp FROM measurement ORDER BY id_measurement DESC LIMIT 1")
    for x in cur:
        temp_last = float(x[0])

    cur.execute("SELECT dimension_x, dimension_y, dimension_z, id_config FROM configuration ORDER BY id_config DESC LIMIT 1")
    for x in cur:
        d_x = int(x[0])
        d_y = int(x[1])
        d_z = int(x[2])
        id_config = int(x[3])
    conn.close()

    # wyliczenie nowej wartści temperatury przy wzroście
    temp = temp_last + (POWER)/(4200*(d_x*d_y*d_z/1000))
    temp = round(temp,3)

    print(f"New tmp: {temp}")


    # ustalenie i sformatowanie do formatu daty i czasu odczytu
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        database="automatyka")
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO measurement (id_config,temp,date_time) VALUES (?, ?, ?)", (id_config,temp,dt_string))
    except mariadb.Error as e:
        print(f"Error: {e}")

    # zatwierdzenie zmian w bazie oraz zamknięcie połączenia
    conn.commit()
    conn.close()


def db_save_decrease():
    """Funkcja symulująca odczyty temperatury przy wyłączonej grzałce"""

    # parametry połączenia z bazą danych
    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        database="automatyka")
    cur = conn.cursor()


    # pobranie ostatniej temperatury, "błędu odczytu" oraz id obecnej konfiguracji
    temp_last = 0.0
    temp_e = 0.0
    id_config = 0
    d_x = 0
    d_y = 0
    d_z = 0

    cur.execute("SELECT temp FROM measurement ORDER BY id_measurement DESC LIMIT 1")
    for x in cur:
        temp_last = float(x[0])

    cur.execute("SELECT dimension_x, dimension_z, id_config, temp_e FROM configuration ORDER BY id_config DESC LIMIT 1")
    for x in cur:
        d_x = int(x[0])
        d_z = int(x[1])
        id_config = int(x[2])
        temp_e = float(x[3])
    conn.close()

    # wyliczenie nowej wartści temperatury przy spadku
    temp = (temp_e + (temp_last - temp_e) * math.exp((-1)*(0.6*((d_x*d_z*6)/10000)/(4200))))
    temp = round(temp,3)
    print(f"New tmp: {temp}")

    # ustalenie i sformatowanie do formatu daty i czasu odczytu
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        database="automatyka")
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO measurement (id_config,temp,date_time) VALUES (?, ?, ?)", (id_config,temp,dt_string))
    except mariadb.Error as e:
        print(f"Error: {e}")


    # zatwierdzenie zmian w bazie oraz zamknięcie połączenia
    conn.commit()
    conn.close()



if __name__ == "__main__":
    """Główna pętla skrytu symulującego realne odczyty temperatury"""

    while(True):
        # dodanie opóźninia, odczyt co 1 sekundę
        time.sleep(1)

        odczyt = True

        # ustalenie na podstawie informacji w pliku trybu odczytu
        try:
            file_object = open("tryb.ini", "r")
            tryb = int(file_object.read())
            file_object.close()
            odczyt = False
        except:
            file_object.close()

        while odczyt:
            try:
                file_object = open("tryb.ini", "r")
                tryb = int(file_object.read())
                file_object.close()
                odczyt = False
            except:
                file_object.close()

        if tryb == 1:
            print("Wzorst temperatury")
            db_save_increase()
        else:
            print("Spadek temperatury")
            db_save_decrease()

import time
import mariadb

class PID:
    """
    Dyskretny regulator PID
    """

    def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator=Derivator
        self.Integrator=Integrator
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min

        self.set_point=0.0
        self.error=0.0

    def update(self,current_value):
        """
        Wyznaczenie wyjścia z regulatora PID
        """

        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.I_value = self.Integrator * self.Ki

        PID = self.P_value + self.I_value + self.D_value

        return PID

    def setPoint(self,set_point):
        """
        Inicjalizacja nową wartością zadaną, wyzerowanie
        """
        self.set_point = set_point
        self.Integrator=0
        self.Derivator=0

    # settery i gettery to pól w regulatorze
    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self,P):
        self.Kp=P

    def setKi(self,I):
        self.Ki=I

    def setKd(self,D):
        self.Kd=D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):
        return self.Derivator



if __name__ == "__main__":
    """Główna pętla skrytu symulującego regulator"""

    # Zdefiniowanie nastaw regulatora (P, I, D)
    p=PID(3.0,0.4,1.2)

    while True:
        # parametry połączenia z bazą danych
        conn = mariadb.connect(
            user="root",
            password="root",
            host="localhost",
            database="automatyka")
        cur = conn.cursor()

        # pobranie aktualnej temperatury i zadanej temperatury
        temp_w = 0.0
        temp_last = 0.0

        cur.execute("SELECT temp FROM measurement ORDER BY id_measurement DESC LIMIT 1")
        for x in cur:
            temp_last = float(x[0])

        cur.execute("SELECT temp_w FROM configuration ORDER BY id_config DESC LIMIT 1")
        for x in cur:
            temp_w = float(x[0])

        conn.close()

        # przekazanie temperatury zadanej w każdej iteracji regulatra w razie jej zmiany
        p.setPoint(temp_w)
        # przekazanie bieżącej temperatury
        pid = p.update(temp_last)
        print(f"Wartość z pid {pid}")

        dostep = True
        if pid > 0:
            # grzałka włączona
            print("Tryb 1")

            try:
                file_object = open("tryb.ini", "w")
                file_object.write("1")
                file_object.close()
                dostep = False
            except:
                file_object.close()

            while dostep:
                try:
                    file_object = open("tryb.ini", "w")
                    file_object.write("1")
                    file_object.close()
                    dostep = False
                except:
                    file_object.close()

            time.sleep(int(abs(pid) + 1) * 2)

        else:
            # grzałka wyłączona
            print("Tryb 0")

            try:
                file_object = open("tryb.ini", "w")
                file_object.write("0")
                file_object.close()
                dostep = False
            except:
                file_object.close()

            while dostep:
                try:
                    file_object = open("tryb.ini", "w")
                    file_object.write("0")
                    file_object.close()
                    dostep = False
                except:
                    file_object.close()

            if(int(abs(pid)) <= 1):
                time.sleep(10)
            else:
                time.sleep(int(abs(pid) + 1) * 2)

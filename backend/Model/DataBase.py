from backend.Model.Connexion import Connexion
from pyodbc import ProgrammingError
from backend.Controller.pathFinder import JSONFinder


class SQLSERVERDBModel:

    def __init__(self):
        self.cursor = Connexion().cursor()

    def get_all_recordings_given_date(self, a, m, d):
        requete = f"select id_gestion, accion_ges, respuesta_ges, telefono_ges, fecha_ges, cedente, serial_ced from CEDENTE a inner join GESTIONES b  on a.nombre_ced=b.cedente where tipo_ges = 1 and convert(date,fecha_ges,120)=convert(date,'{a}-{m}-{d}',120)"
        self.cursor.execute(
            requete
        )
        return self.cursor.fetchall()

    def get_serialced_fromname(self, name: str):

        requete = """select * from CEDENTE where nombre_ced= ? """
        self.cursor.execute(requete, name)
        return self.cursor.fetchone()

    def get_positive_phrases(self, ced_num: str):
        requete = "select * from CCALIDAD_FRASE where serial_ced= ? and tipo_ccf='ACTIVO' order by etiqueta_ccf"
        self.cursor.execute(requete, ced_num)
        return self.cursor.fetchall()

    def get_negative_phrases(self):
        request = "select * from CCALIDAD_PALABRA"
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def get_grabaciones(self):
        requete = "select * from grabaciones"
        self.cursor.execute(requete)
        return self.cursor.fetchall()

    def get_autogenerated_scores(self):
        requete = "select * from AUTOGENERATED_SCORES"
        self.cursor.execute(requete)
        return self.cursor.fetchall()

    def test(self):
        requests = "select id_gestion, accion_ges, respuesta_ges, telefono_ges, fecha_ges, cedente, serial_ced \
                   from CEDENTE a \
                   inner join GESTIONES b  on a.nombre_ced=b.cedente \
                   where tipo_ges = 1 and convert(date,fecha_ges,120)=convert(date,'2023-04-27',120) \
                   and telefono_ges='0980427196' "
        self.cursor.execute(requests)
        return self.cursor.fetchall()

    def add_grabaciones(self, id_grabacion, nombre, telefono, fecha, audio):
        fech = f"{fecha[:4]}-{fecha[4:6]}-{fecha[6:8]}"
        hora = f"{fecha[-6:-4]}:{fecha[-4:-2]}:{fecha[-2:]}"
        fecha_real = f"{fech} {hora}"
        requete = f"INSERT INTO GRABACIONES VALUES ({id_grabacion}, '{nombre}', '{telefono}', '{fecha_real}', '{audio}')"
        self.cursor.execute(requete)

    def add_autogenerated_scores(self, id_grabacion: str, scores: dict):
        attributes = {"total": "total",
                      "cedente": "cedente",
                      "cierre": "cierre",
                      "convenio": "convenio",
                      "grabacion": "grabacion",
                      "identificacion": "identificacion",
                      "motivo": "motivo",
                      "objeciones": "objeciones",
                      "saludo": "saludo"}

        self.cursor.execute("SELECT top 1 * FROM AUTOGENERATED_SCORES")
        for key in self.cursor.description:
            real_key = key[0].lower()
            if real_key in scores:
                attributes[real_key] = scores[real_key]
            elif real_key in attributes:
                attributes[real_key] = 0

        requete = f"INSERT INTO AUTOGENERATED_SCORES" \
                  f" VALUES ({id_grabacion}, {attributes['total']}, {attributes['cedente']}, {attributes['cierre']}, {attributes['convenio']}, {attributes['grabacion']}, {attributes['identificacion']}, {attributes['motivo']}, {attributes['objeciones']}, {attributes['saludo']})"
        self.cursor.execute(requete)

    def _check_if_exists(self, table_name) -> bool:
        try:
            requete = f"select top 1 * from {table_name}"
            self.cursor.execute(requete)

            return True

        except ProgrammingError:
            return False

    def create_tables(self):
        autogenerated_IA = self._check_if_exists("AUTOGENERATED_SCORES")
        grabaciones = self._check_if_exists("GRABACIONES")

        if not grabaciones:
            self.cursor.execute(
                "CREATE TABLE GRABACIONES (\
                g_id INT, \
                nombre VARCHAR(70), \
                numero VARCHAR(10), \
                fecha DATE, \
                mensaje VARCHAR(8000),\
                PRIMARY KEY (id_grabacion)\
            )"
            )

        if not autogenerated_IA:
            self.cursor.execute(
                "CREATE TABLE AUTOGENERATED_SCORES( \
                id INT, \
                TOTAL INT NOT NULL,\
                CEDENTE INT, \
                CIERRE INT, \
                CONVENIO INT, \
                GRABACION INT, \
                IDENTIFICACION INT, \
                MOTIVO INT, \
                OBJECCIONES INT, \
                SALUDO INT,\
                PRIMARY KEY(id), \
                FOREIGN KEY (id) REFERENCES GRABACIONES(id_grabacion) \
                )")

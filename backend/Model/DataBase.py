from backend.Model.Connexion import Connexion


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

        requete = """select * from CEDENTE where nombre_ced= %(name)s """
        self.cursor.execute(requete, {
            'name': name
        })
        return self.cursor.fetchall()

    def get_positive_phrases(self):
        requete = "select * from CCALIDAD_FRASE where serial_ced=235 and tipo_ccf='ACTIVO' order by etiqueta_ccf"
        self.cursor.execute(requete)
        return self.cursor.fetchall()

    def get_negative_phrases(self):
        request = "select * from CCALIDAD_PALABRA"
        self.cursor.execute(request)
        return self.cursor.fetchall()


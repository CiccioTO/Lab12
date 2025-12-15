from database.DB_connect import DBConnect
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    def __init__(self):
        pass

    @staticmethod
    def read_connessioni(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select id, id_rifugio1, id_rifugio2, distanza, difficolta
                   from connessione 
                   where anno<=%s
                                """
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_rifugi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select id, nome , localita
                    from rifugio"""
        cursor.execute(query)

        for row in cursor:
            r = Rifugio(row['id'], row['nome'], row['localita'])
            result.append(r)

        cursor.close()
        conn.close()
        return result

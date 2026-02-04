from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_ruoli():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """ SELECT DISTINCT role
                    FROM authorship"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['role'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti(ruolo: str):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """ SELECT DISTINCT ar.artist_id, ar.name
                    FROM authorship au, artists ar, objects o
                    WHERE au.artist_id = ar.artist_id AND au.object_id = o.object_id 
                    AND au.role = %s AND o.curator_approved = 1 """

        cursor.execute(query, (ruolo,))

        for row in cursor:
            result.append(Artist(
                artist_id=row['artist_id'],
                name=row['name'],
            ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_indice_per_specific_artist(id_artista):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """ select count(distinct o.object_id) as indice
                    from authorship au, objects o
                    where au.object_id = o.object_id and au.artist_id = %s
                    and exists (select *
                                from objects o1
                                where o1.object_id = o.object_id
                                and o1.curator_approved = 1) """

        cursor.execute(query, (id_artista,))

        for row in cursor:
            result.append(row['indice'])

        cursor.close()
        conn.close()
        return result[0]

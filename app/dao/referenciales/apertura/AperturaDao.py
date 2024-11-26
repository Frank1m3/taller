from flask import current_app as app
from app.conexion.Conexion import Conexion

class AperturaDao:

    def getAperturas(self):
        aperturaSQL = """
        SELECT id_apertura,nro_turno, fiscal, cajero, registro, monto_inicial
        FROM aperturas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(aperturaSQL)
            # trae datos de la bd
            lista_aperturas = cur.fetchall()
            # retorno los datos
            lista_ordenada = []
            for item in lista_aperturas:
                lista_ordenada.append({
                    "id_apertura": item[0],
                    "nro_turno": item[1],
                    "fiscal": item[2],
                    "cajero": item[3],
                    "registro": item[4],
                    "monto_inicial": item[5] 
                })
            return lista_ordenada
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()

    def getAperturaById(self, id_apertura):
        aperturaSQL = """
        SELECT id_apertura, nro_turno, fiscal, cajero, registro
        FROM aperturas WHERE id_apertura=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(aperturaSQL, (id_apertura,))
            # trae datos de la bd
            aperturaEncontrada = cur.fetchone()
            # retorno los datos
            if aperturaEncontrada:
                return {
                    "id_apertura": aperturaEncontrada[0],
                    "nro_turno": aperturaEncontrada[1],
                    "fiscal": aperturaEncontrada[2],
                    "cajero": aperturaEncontrada[3],
                    "registro": aperturaEncontrada[4],
                    "monto_inicial": aperturaEncontrada[5]    
                }
            return None
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()

    def guardarApertura(self, nro_turno, fiscal, cajero, registro, monto_inicial):
        insertAperturaSQL = """
        INSERT INTO aperturas(ruc, fiscal, cajero, registro, monto_inicial)
        VALUES (%s, %s, %s, %s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertAperturaSQL, (nro_turno, fiscal, cajero, registro, monto_inicial))
            # se confirma la insercion
            con.commit()
            return True
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()

        return False

    def updateApertura(self, id_apertura, nro_turno, fiscal, cajero, registro, monto_inicial):
        updateAperturaSQL = """
        UPDATE aperturas
        SET nro_turno=%s, fiscal=%s, cajero=%s, registro=%s, monto:inicial=%s
        WHERE id_apertura=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(updateAperturaSQL, (nro_turno, fiscal, cajero, registro, monto_inicial, id_apertura))
            # se confirma la insercion
            con.commit()
            return True
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()

        return False

    def deleteApertura(self, id_apertura):
        deleteAperturaSQL = """
        DELETE FROM aperturas
        WHERE id_apertura=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(deleteAperturaSQL, (id_apertura,))
            # se confirma la eliminación
            con.commit()
            return True
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()

        return False

from flask import current_app as app
from app.conexion.Conexion import Conexion

class AperturaDao:

    def getAperturas(self):
        aperturaSQL = """
        SELECT id_apertura, nro_turno, clave_fiscal, cajero, registro, monto_inicial
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
                    "clave_fiscal": item[2],
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
        SELECT id_apertura, nro_turno, clave_fiscal, cajero, registro
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
                    "clave_fiscal": aperturaEncontrada[2],
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

    def guardarApertura(self, clave_fiscal, cajero, monto_inicial):
        insertAperturaSQL = """
        INSERT INTO aperturas(clave_fiscal, cajero, monto_inicial)
        VALUES (%s, %s ,%s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertAperturaSQL, ( clave_fiscal, cajero, monto_inicial))
            # se confirma la insercion
            con.commit()
            return True
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()

        return False

    def updateApertura(self, id_apertura, nro_turno, clave_fiscal, cajero, registro, monto_inicial):
        updateAperturaSQL = """
        UPDATE aperturas
        SET nro_turno=%s, clave_fiscal=%s, cajero=%s, registro=%s, monto_inicial=%s
        WHERE id_apertura=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(updateAperturaSQL, (nro_turno, clave_fiscal, cajero, registro, monto_inicial, id_apertura))
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
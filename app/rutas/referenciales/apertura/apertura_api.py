from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.apertura.AperturaDao import AperturaDao

aperapi = Blueprint('aperapi', __name__)

@aperapi.route('/aperturas', methods=['GET'])
def getAperturas():
    aperturadao = AperturaDao()

    try:
        aperturas = aperturadao.getAperturas()

        return jsonify({
            'success': True,
            'data': aperturas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las aperturas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@aperapi.route('/aperturas/<int:id_apertura>', methods=['GET'])
def getApertura(id_apertura):
    aperturadao = AperturaDao()

    try:
        apertura = aperturadao.getAperturaById(id_apertura)

        if apertura:
            return jsonify({
                'success': True,
                'data': apertura,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la apertura con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener apertura: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@aperapi.route('/aperturas', methods=['POST'])
def addApertura():
    data = request.get_json()
    aperturadao = AperturaDao()

    # Aseguramos que los campos requeridos estén presentes y no vacíos
    campos_requeridos = ['clave_fiscal', 'cajero', 'monto_inicial']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        # Guardamos la apertura, la base de datos generará automáticamente el nro_turno
        id_apertura = aperturadao.guardarApertura(
            data['clave_fiscal'].strip().upper(),
            data['cajero'].strip(),
            data['monto_inicial']
        )

        # Devolvemos solo los datos que no son autogenerados
        return jsonify({
            'success': True,
            'data': {
                'id_apertura': id_apertura,  # ID generado por la base de datos
                'clave_fiscal': data['clave_fiscal'].upper(),
                'cajero': data['cajero'].upper(),
                'monto_inicial': data['monto_inicial']
            },
            'error': None
        }), 201

    except Exception as e:
        app.logger.error(f"Error al realizar apertura: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@aperapi.route('/aperturas/<int:id_apertura>', methods=['PUT'])
def updateApertura(id_apertura):
    data = request.get_json()
    aperturadao = AperturaDao()

    # Aseguramos que los campos requeridos estén presentes y no vacíos
    campos_requeridos = ['clave_fiscal', 'cajero', 'registro', 'monto_inicial', 'estado']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    # Validar y normalizar el estado
    estado = data['estado'].lower()
    if estado not in ['activo', 'inactivo', 'pendiente']:
        return jsonify({
            'success': False,
            'error': 'El estado debe ser "activo", "inactivo" o "pendiente".'
        }), 400

    try:
        # Llamamos a la función de actualización
        updated = aperturadao.updateApertura(
            id_apertura,
            data['clave_fiscal'].strip().upper(),
            data['cajero'].strip().upper(),
            data['registro'],
            data['monto_inicial'],
            estado  # Solo enviamos el estado, no el nro_turno
        )

        if updated:
            return jsonify({
                'success': True,
                'data': {
                    'id_apertura': id_apertura,
                    'clave_fiscal': data['clave_fiscal'].upper(),
                    'cajero': data['cajero'].upper(),
                    'registro': data['registro'],
                    'monto_inicial': data['monto_inicial'],
                    'estado': estado
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la apertura con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar apertura: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@aperapi.route('/aperturas/<int:id_apertura>', methods=['DELETE'])
def deleteApertura(id_apertura):
    aperturadao = AperturaDao()

    try:
        if aperturadao.deleteApertura(id_apertura):
            return jsonify({
                'success': True,
                'mensaje': f'Apertura con ID {id_apertura} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la apertura con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar la apertura: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

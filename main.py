from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import config
from geopy.distance import geodesic
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app)

conexion = MySQL(app)

@app.route('/comunidades', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Se muestran las comunidades cargadas',
            'examples': {
                'application/json': {
                    'Comunidades cerca de tu locacion': [
                        {
                            'nombre': 'Institución 1',
                            'direccion': 'Calle Falsa 123'
                        },
                        {
                            'nombre': 'Institución 2',
                            'direccion': 'Calle Falsa 8923'
                        },
                        {
                            'nombre': 'Institución 3',
                            'direccion': 'Calle Falsa 2048'
                        }
                    ]
                }
            }
        },
        500: {
            'description': 'Error interno del servidor',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'mensaje': {
                                'type': 'string',
                                'example': 'Error :('
                            }
                        }
                    }
                }
            }
        }
    }
})
def listar_entidades():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT nombre, direccion, latitud, longitud FROM comunidades"
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        entidades = []
        for dato in datos:
            entidad = {
                'nombre': dato[0],
                'direccion': dato[1],
                'latitud': dato[2],
                'longitud': dato[3]
            }
            entidades.append(entidad)
        
        return jsonify(entidades)
    except Exception as ex:
        return jsonify({'mensaje': "Error :("}), 500

@app.route('/recomendar', methods = ['GET'])
@swag_from({'parameters': [
        {
            'name': 'lat',
            'in': 'query',
            'type': 'number',
            'required': True,
            'description': 'Latitud de la ubicación actual'
        },
        {
            'name': 'lon',
            'in': 'query',
            'type': 'number',
            'required': True,
            'description': 'Longitud de la ubicación actual'
        },
        {
            'name': 'radio',
            'in': 'query',
            'type': 'number',
            'required': True,
            'description': 'Radio en kilómetros para buscar comunidades cercanas'
        }
    ],
    'responses': {
        200: {
            'description': 'Comunidades cercanas a tu ubicación.',
            'examples': {
                'application/json': {
                    'Comunidades cerca de tu locacion': [
                        {
                            'nombre': 'Institución 1',
                            'direccion': 'Calle Falsa 123'
                        }
                    ]
                }
            }
        }
    }
})
def recomendar_lugares():
    try:
        # Obtener los parámetros de la solicitud
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        radio = float(request.args.get('radio'))

        # Conectar a la base de datos
        cursor = conexion.connection.cursor()

        # Consulta para obtener todas las comunidades
        query = "SELECT nombre, direccion, latitud, longitud FROM instituciones"
        cursor.execute(query)
        comunidades = cursor.fetchall()

        # Filtrar comunidades dentro del radio
        ubicacion_actual = (lat, lon)
        comunidades_en_radio = []

        for comunidad in comunidades:
            ubicacion_comunidad = (comunidad['latitud'], comunidad['longitud'])
            distancia = geodesic(ubicacion_actual, ubicacion_comunidad).kilometers
            if distancia <= radio:
                comunidades_en_radio.append((comunidad['nombre'], comunidad['direccion']))

        return jsonify({'Comunidades cerca de tu locacion': comunidades_en_radio})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def pagina_no_encontrada(error):
    return "<h1>Lo siento, la página que estás buscando no existe</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

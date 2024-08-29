from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import config
from geopy.distance import geodesic
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app)

conexion = MySQL(app)

      
@app.route('/recomendar', methods=['GET'])
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

        # Consulta para obtener todas las instituciones
        query = "SELECT nombre, direccion, latitud, longitud FROM instituciones"
        cursor.execute(query)
        instituciones = cursor.fetchall()

        # Filtrar instituciones dentro del radio
        ubicacion_actual = (lat, lon)
        instituciones_en_radio = []

        for institucion in instituciones:
            ubicacion_institucion = (institucion['latitud'], institucion['longitud'])
            distancia = geodesic(ubicacion_actual, ubicacion_institucion).kilometers
            if distancia <= radio:
                instituciones_en_radio.append((institucion['nombre'], institucion['direccion']))

        return jsonify({'Comunidades cerca de tu locacion': instituciones_en_radio})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def pagina_no_encontrada(error):
    return "<h1>Lo siento, la página que estás buscando no existe</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
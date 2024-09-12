import mysql.connector
from mysql.connector import errorcode
from config import DevelopmentConfig  # Importar la configuración

# Obtener la configuración de desarrollo
config = DevelopmentConfig()

# Script SQL para crear la base de datos y la tabla
sql_script = """
CREATE DATABASE IF NOT EXISTS comunidades_donantes;
USE comunidades_donantes;

CREATE TABLE IF NOT EXISTS comunidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    latitud DECIMAL(10, 8) NOT NULL,
    longitud DECIMAL(11, 8) NOT NULL
);
"""

def ejecutar_script(script, config):
    try:
        # Conectar a MySQL usando la configuración
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        cursor = conn.cursor()

        # Dividir el script en múltiples consultas
        queries = script.split(';')

        # Ejecutar cada consulta
        for query in queries:
            if query.strip():
                cursor.execute(query)

        print("Base de datos y tabla creadas exitosamente.")
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error en el acceso: Usuario o contraseña incorrecta.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: La base de datos no existe.")
        else:
            print(f"Error: {err}")
    
    finally:
        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()

# Ejecutar el script
if __name__ == "__main__":
    ejecutar_script(sql_script, config)

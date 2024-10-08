# Recomendador Comunidades 
`version 1.0.0` 

## Descripcion
* La API REST Recomendador comunidades está diseñada para facilitar la búsqueda de comunidades y organizaciones cercanas a tu ubicación donde puedes realizar donaciones. Con solo proporcionar una ubicación geográfica y un radio específico, la API te ayudará a identificar las instituciones y comunidades más cercanas que están aceptando donaciones.

## Documentacion
* La documentacion de la API se puede encontrar en http://localhost:5000/apidocs/ una vez la API esta en ejecucion. Esto se realizo con la libreria flasgger de python para poder generar desde el mismo codigo la documentacion y la ruta donde se encuentra
* Tambien se puede visualizar desde https://app.swaggerhub.com/apis/JGALGANO/RecomendadorComunidades/1.0.0
  
## Uso
Para poder utilizar la API es necesario seguir los siguientes pasos

0. Verificar que se tiene instalado python (si no es asi se puede instalar desde la web oficial https://python.org/downloads/)
1. Clonarse el repositorio
2. Instalarse las librerias especificadas con el comando pip install -r requirements.txt
3. Modificar el archivo config.py con los datos propios
4. Ejecutar el archivo sript_bd.py para generar la base de datos local ingresndo en la terminal python sript_bd 
5. Ejecutar el archivo main.py para levantar la API ingresando en la terminal python main.py

extra. un ejemplo de uso es con las coordenadas lat=-34.6037 y lon=-58.3816 y radio=5

## Ejemplo de respuesta
```http
GET http://localhost:5000/recomendar?lat=-34.6037&lon=-58.3816&radio=5
{
  "Comunidades cerca de tu locacion": [
    [
      "Institución A",
      "Dirección A"
    ],
    [
      "Institución B",
      "Dirección B"
    ],
    [
      "Institución C",
      "Dirección C"
    ]
  ]
}

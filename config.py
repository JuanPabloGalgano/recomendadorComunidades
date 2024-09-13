class DevelopmentConfig():
      DEBUG = True
      MYSQL_HOST = 'localhost'
      MYSQL_USER = 'root'
      MYSQL_PASSWORD = 'contraseñaGenerica'
      MYSQL_DB = 'instituciones_donantes'
      MYSQL_CURSORCLASS = 'DictCursor'
       
config = {
      'development': DevelopmentConfig
}

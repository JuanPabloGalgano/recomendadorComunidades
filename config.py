class DevelopmentConfig():
      DEBUG = True
      MYQSL_HOST = 'localhost'
      MYSQL_USER = 'root'
      MYSQL_PASSWORD = 'Operator.2024'
      MYSQL_DB = 'instituciones_donantes'
      MYSQL_CURSORCLASS = 'DictCursor'
       
config = {
      'development': DevelopmentConfig
}
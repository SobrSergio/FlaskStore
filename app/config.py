class Configuration():
    DEBUG = True
    
    SECRET_KEY = 'pilpy4gwoeygel32yge2oyureg2ley2gdl2yglyg'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Sergey120799Tamara2607@localhost/sneakshop'
    
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'SneakShop.ru@gmail.com'
    MAIL_PASSWORD = 'uzowevoofbjfulba'
    MAIL_DEFAULT_SENDER = 'SneakShop.ru@gmail.com'
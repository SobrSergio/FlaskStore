class Configuration():
    DEBUG = True
    
    SECRET_KEY = 'pilpy4gwoeygel32yge2oyureg2ley2gdl2yglyg'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://YourDb'
    
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'youremail@gmail.com'
    MAIL_PASSWORD = 'passwordforyouremail'
    MAIL_DEFAULT_SENDER = 'youremail@gmail.com'
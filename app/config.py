class Configuration():
    DEBUG = True
    
    SECRET_KEY = 'HERE-YOUR-SECRET-KEY'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://YourDb'  #Example connection on postgresql- 'postgresql://postgres:YourPassword@localhost/sneakshop'
    
    
    MAIL_SERVER = 'smtp.googlemail.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'youremail@gmail.com' #enter email admin
    MAIL_PASSWORD = 'passwordforyouremail' #enter password email admin
    MAIL_DEFAULT_SENDER = 'youremail@gmail.com' #enter email admin
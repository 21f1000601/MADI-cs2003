class Config():
    
    #application is not in debug mode, and the errors messages will not be shown to the user
    DEBUG = False 

    #this setting tracks changes that are made to the objects and emits signal. 
    #it can use extra memory, thus set it to false in production
    SQLALCHEMY_TRACK_MODIFICATIONS = True 

class LocalDevelopmentConfig(Config): #inherits the class Config 
    
#database configuration begins here
    #set the uri & tells SQLALCHEMY to use SQLite database file 
    SQLALCHEMY_DATABASE_URI = "sqlite:///fix_it_db.sqlite3"

    #this line overrides the DEBUG property in Config class and sets it to true
    DEBUG = True

    
#security configuration begins here

    #it sets the secret key that is used for cryptographic operations like signing cookies or sessions
    #it is important for security and should be kept secret
    SECRET_KEY = "this-is-my-secret-key" 

    #specifies the hashing algorithm to use for securing passwords securely.
    SECURITY_PASSWORD_HASH = "bcrypt" 

    #it sets the salt value that is used for hashing passwords. 
    #it is added to the password, making it secure
    SECURITY_PASSWORD_SALT = "this-is-my-secret-password-salt" 

    #this line disables Cross-Site Request Forgery protection
    #it is a security feature that prevents unauthorised commands from being transmitted from the user to the web application trusts
    #it can be turned off for convinience in development phase
    WTF_CSRF_ENABLED = False

    #it sets the header name for the authentication token.
    #when the user logins, this is the key name that will be used for authentication
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
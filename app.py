from flask import Flask, render_template
from application.models import db 
import secrets
app =None

def setup_app():
    app=Flask(__name__)
    app.debug=True
    app.secret_key = 'PQDBXH3GTY'  # Replace with a strong random string
    #pending here is sqlite connection
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///fix_it_db.sqlite3" #Having db file
    db.init_app(app) #Flask app connected to db(SQL alchemy)
    
    app.app_context().push()
    print("Household cleaning app is started...\n\n WELCOME TO FIX IT")


#call seytupd

setup_app()

from application.controllers import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import *

from admin import admin

from public import public 

from user import users

app=Flask(__name__)

app.secret_key="mockai"

app.register_blueprint(admin)

app.register_blueprint(public)

app.register_blueprint(users)

app.run(debug=True)
from flask import Blueprint, render_template
from werkzeug.security import generate_password_hash
import x
import uuid

from icecream import ic
ic.configureOutput(prefix=f'***** | ', includeContext=True)


post_create_user = Blueprint("post_create_user", __name__)


##############################
@post_create_user.post("/users")
def create_user():
    try:
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        hashed_password = generate_password_hash(user_password)

        user_pk = str(uuid.uuid4())

        db, cursor = x.db()
        q = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(q, (user_pk, user_name, user_last_name, user_email, hashed_password))
        db.commit()
    
        return """<template mix-redirect="/login"></template>"""
    
    except Exception as ex:

        ic(ex)
        if "db" in locals(): db.rollback()

        # My own exception
        if isinstance(ex, x.CustomException):
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code
        
        # Database exception
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            if "users.user_email" in str(ex):
                return "<template>email not available</template>", 400
            return "<template>System upgrating</template>", 500  
      
        # Any other exception
        return "<template>System under maintenance</template>", 500  
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()











from flask import Blueprint, session
from werkzeug.security import check_password_hash
import x

from icecream import ic
ic.configureOutput(prefix=f'***** | ', includeContext=True)

post_login = Blueprint("post_login", __name__)

##############################
@post_login.post("/login")
def login():
    try:

        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user:
            return """<template mix-target="#toast">user not registered</template>""", 400
        if not check_password_hash(user["user_password"], user_password):
            return """<template mix-target="#toast">invalid credentials</template>""", 401
        # MUST DO: REMOVE THE PASSWORD FROM THE user
        user.pop("user_password")
        ic(user)
        session["user"] = user
        return """<template mix-redirect="/profile"></template>"""
    except Exception as ex:
        ic(ex)

        # Mysql exception
        if len(ex.args) == 3:
            """<template>database error</template>""", 500
        # Own exception
        if len(ex.args) == 2:
            return f"""<template mix-target="#toast" mix-bottom>{ex.args[0]}</template>""", ex.args[1]
        # Not under control
        return f"""<template>upc</template>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()











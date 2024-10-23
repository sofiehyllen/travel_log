from flask import Flask, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import x
import uuid 
import time

from icecream import ic
ic.configureOutput(prefix=f'***** | ', includeContext=True)

app = Flask(__name__)

app.secret_key = "your_secret_key"

##############################
def _________GET_________(): pass

##############################
@app.get("/")
def show_index():
    name = "X"
    return render_template("view_index.html", name=name)

##############################
@app.get("/login")
def show_login(): return render_template("view_login.html")



##############################
@app.get("/profile")
def show_profile():
    if not session.get("user", ""): 
        return redirect(url_for("show_login"))
    user = session.get("user")
    if len(user["roles"]) > 1:
        return redirect(url_for("show_choose_role"))
    return render_template("view_profile.html")


##############################
@app.get("/choose-role")
def show_choose_role():
    if not session.get("user", ""): 
        return redirect(url_for("show_login"))
    user = session.get("user")
    return render_template("view_choose_role.html")


def _________POST_________(): pass

##############################
@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("show_index"))


##############################
@app.post("/users")
def user_create():
    try:
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)

        user_pk = str(uuid.uuid4())
        user_created_at = int(time.time())

        db, cursor = x.db()
        q = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(q, (user_pk, user_name, user_last_name, user_email, hashed_password, user_created_at, 0, 0))
        db.commit()
    
        return """<template mix-redirect="/login"></template>"""
    
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        # My own exception
        if isinstance(ex, x.CustomException): return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code    
        # Database exception
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            if "users.user_email" in str(ex): return "<template>email not available</template>", 400
            return "<template>System upgrating</template>", 500        
        # Any other exception
        return "<template>System under maintenance</template>", 500    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/login")
def login():
    try:

        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = """ SELECT * FROM users 
                JOIN users_roles 
                ON user_pk = user_role_user_pk 
                JOIN roles
                ON role_pk = user_role_role_fk
                WHERE user_email = %s"""
        cursor.execute(q, (user_email,))
        rows = cursor.fetchall()
        if not rows:
            return """<template mix-target="#toast">user not registered</template>""", 400     
        if not check_password_hash(rows[0]["user_password"], user_password):
            return """<template mix-target="#toast">invalid credentials</template>""", 401
        roles = []
        for row in rows:
            roles.append(row["role_name"])
        user = {
            "user_pk": rows[0]["user_pk"],
            "user_name": rows[0]["user_name"],
            "user_last_name": rows[0]["user_last_name"],
            "user_email": rows[0]["user_email"],
            "roles": roles
        }
        ic(user)
        session["user"] = user
        return f"""<template mix-redirect="/profile"></template>"""
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        # My own exception
        if isinstance(ex, x.CustomException): return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code    
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





def _________PUT_________(): pass

##############################
@app.put("/users/block/<user_pk>")
def user_block(user_pk):
    try:
        # Check if user is logged
        if not session.get("user", ""): return redirect(url_for("show_login"))
        # Check if it is an admin
        if not "admin" in session.get("user")["roles"]: return redirect(url_for("show_login"))
        user_pk = x.validate_uuid4(user_pk)
        user_blocked_at = int(time.time())
        db, cursor = x.db()
        q = 'UPDATE users SET user_blocked_at = %s WHERE user_pk = %s'
        cursor.execute(q, (user_blocked_at, user_pk))
        db.commit()
        return """<template>user blocked</template>"""
    
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
            return "<template>Database error</template>", 500        
        # Any other exception
        return "<template>System under maintenance</template>", 500  
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


def _________DELETE_________(): pass


##############################
@app.delete("/users/<user_pk>")
def user_delete(user_pk):
    try:
        # Check if user is logged
        if not session.get("user", ""): return redirect(url_for("show_login"))
        # Check if it is an admin
        if not "admin" in session.get("user")["roles"]: return redirect(url_for("show_login"))
        user_pk = x.validate_uuid4(user_pk)
        user_deleted_at = int(time.time())
        db, cursor = x.db()
        q = 'UPDATE users SET user_deleted_at = %s WHERE user_pk = %s'
        cursor.execute(q, (user_deleted_at, user_pk))
        db.commit()
        return """<template>user deleted</template>"""
    
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
            return "<template>Database error</template>", 500        
        # Any other exception
        return "<template>System under maintenance</template>", 500  
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
# from routes_get.get_index import get_index
# from routes_get.get_users import get_users
# from routes_get.get_profile import get_profile
# from routes_get.get_logout import get_logout
# from routes_get.get_items_by_page import get_items_by_page

##############################
# from routes_post.post_create_user import post_create_user
# from routes_post.post_login import post_login

##############################


##############################
# app.register_blueprint(get_index)
# app.register_blueprint(get_users)
# app.register_blueprint(get_profile)
# app.register_blueprint(get_logout)
# app.register_blueprint(get_items_by_page)


# app.register_blueprint(post_create_user)
# app.register_blueprint(post_login)





















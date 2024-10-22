from flask import Blueprint, session, redirect, url_for

get_logout = Blueprint("get_logout", __name__)

##############################
@get_logout.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("get_index.show_index"))



















from flask import Blueprint, session, render_template, redirect, url_for

get_profile = Blueprint("get_profile", __name__)

##############################
@get_profile.get("/profile")
def show_profile():
    user = session.get("user", "")
    if not user:
        return redirect(url_for("get_index.show_index"))
    return render_template("profile.html", user=user)



















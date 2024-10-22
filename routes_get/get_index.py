from flask import Blueprint, render_template

get_index = Blueprint("get_index", __name__)

##############################
@get_index.get("/")
def show_index():
    name = "X"
    return render_template("view_index.html", name=name)
    return render_template("view_index.html", **locals())



















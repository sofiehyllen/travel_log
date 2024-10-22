from flask import Blueprint, render_template

get_users = Blueprint("get_users", __name__)

##############################
@get_users.get("/users")
def show_users():
    return "users"



















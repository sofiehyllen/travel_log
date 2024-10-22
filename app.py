from flask import Flask, session

app = Flask(__name__)

app.secret_key = "your_secret_key"

##############################
from routes_get.get_index import get_index
from routes_get.get_users import get_users
from routes_get.get_profile import get_profile
from routes_get.get_logout import get_logout

##############################
from routes_post.post_users import post_users
from routes_post.post_login import post_login

##############################


##############################
app.register_blueprint(get_index)
app.register_blueprint(get_users)
app.register_blueprint(get_profile)
app.register_blueprint(get_logout)


app.register_blueprint(post_users)
app.register_blueprint(post_login)





















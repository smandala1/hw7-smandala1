from crypt import methods
import email
import flask
import random
import json
import os
from dotenv import load_dotenv, find_dotenv

from flask_login import (
    login_user,
    current_user,
    LoginManager,
    UserMixin,
    login_required,
)
from flask_sqlalchemy import SQLAlchemy

from tmdb import get_movie_data
from wiki import get_link

load_dotenv(find_dotenv())


app = flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    def __repr__(self):
        return f"<User {self.email}>"

    def get_email(self):
        return self.email


class user_review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Comments = db.Column(db.Text())
    ratings = db.Column(db.Integer)
    Movie_Id = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"<user_review {self.Movie_Id}>"


if os.getenv("DATABASE_URL") is not None:
    db.create_all()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)


bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

# route for serving React page
@bp.route("/index")
def index():
    ratings = user_review.query.filter_by(email=current_user.username).all()
    Movie_ids = [a.Movie_Id for a in ratings]
    has_ratings_saved = len(Movie_ids) > 0
    if has_ratings_saved:
        Movie_id = random.choice(Movie_ids)
        # API calls
        access_token = get_access_token()
        (title, tagline, genreslist, picture) = get_movie_data(Movie_id, access_token)

        wiki_url = get_link(title)
    else:
        (title, tagline, genreslist, picture) = (None, None, None, None, None)

    data = json.dumps(
        {
            "email": current_user.username,
            "Movie_ids": Movie_ids,
            "has_ratings_saved": has_ratings_saved,
            "title": title,
            "tagline": tagline,
            "picture": picture,
        }
    )
    return flask.render_template("index.html", data=data)


@bp.route("/reviews", methods=["GET", "POST"])
@login_required
def reviews():
    user = current_user.username
    review_list = user_review.quert.filter_by(username=user).all()
    commentList = []
    for i in review_list:
        commentlist = {}

        commentlist["id"] = (i.id,)
        commentlist["ratings"] = (i.ratings,)
        commentlist["Comments"] = (i.comments,)
        commentlist["Movie_id"] = (i.Movie_id,)

        commentList.append(commentlist)

    return flask.jsonify(commentList)


app.register_blueprint(bp)


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    email = flask.request.form.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        pass
    else:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    return flask.render_template("login.html")


@app.route("/movies", methods=["GET", "POST"])
def movie_info():
    movieslist = [
        "566525",
        "634649",
        "299687",
        "476669",
        "299534",
        "396535",
        "496243",
        "568124",
        "299537",
        "284053",
    ]
    MOVIE = random.choice(movieslist)
    title, tagline, genreslist, picture = get_movie_data(MOVIE)
    wiki_url = get_link(title)
    return flask.render_template(
        "home.html",
        user=current_user,
        title=title,
        tagline=tagline,
        genreslist=genreslist,
        picture=picture,
        wiki_url=wiki_url,
    )


@app.route("/login", methods=["POST"])
def login_post():
    email = flask.request.form.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("bp.index"))

    return flask.jsonify({"status": 401, "reason": "Email or Password Error"})


@app.route("/")
def main():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("bp.index"))
    return flask.redirect(flask.url_for("login"))


@app.route("/logout")
@login_required
def logout():
    return flask.redirect(flask.url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
    )

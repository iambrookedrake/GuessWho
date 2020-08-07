from flask import Flask
from .model import db
def create_app():
    """Create and configure an instance of the Flask application"""

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\iambr\\Desktop\\Unit3\\GuessWho\\GuessWho.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)


    @app.route("/")
    def root():
        return "Welcome to GuessWho!"

    return app

if __name__ == '__main__':
    app.run(debug=True)


''' Make ^^^ That vvv This

add use
u1 = User(username='austen', follower_count=135000)
u1
db.session.add(u1)
db.session.commit()
u2 - User(username='bruno', follower_count=1)
db.session.add(u2)
db.session.commit()
User.query.all()
exit()
flask run

'''

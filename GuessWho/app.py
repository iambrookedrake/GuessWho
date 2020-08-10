from flask import Flask, render_template, request
from .model import db, User, Tweet
from .twitter import add_user_tweepy

def create_app():
    """Create and configure an instance of the Flask application"""

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\iambr\\Desktop\\Unit3\\GuessWho\\GuessWho\\GuessWho.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.route("/")
    def root():
        return render_template('base.html', title='Home', users=User.query.all())


    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_user_tweepy(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.username == name).one().tweet
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    return app

if __name__ == '__main__':
    app.run(debug=True)


''' Make ^^^ That vvv This

add use
u1 = User(username='austen', follower_count=135000)
u1
db.session.add(u1)
db.session.commit()
u2 = User(username='bruno', follower_count=1)
db.session.add(u2)
db.session.commit()
User.query.all()
exit()
flask run

'''

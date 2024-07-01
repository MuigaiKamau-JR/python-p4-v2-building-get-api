# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json_encoder.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def get_games():
    games = Game.query.all()
    return jsonify([game.to_dict() for game in games])

@app.route('/games/<int:id>')
def get_game(id):
    game = Game.query.get(id)
    if not game:
        return make_response(jsonify({"error": "Game not found"}), 404)
    return jsonify(game.to_dict())

@app.route('/games/users/<int:id>')
def get_users_for_game(id):
    game = Game.query.get(id)
    if not game:
        return make_response(jsonify({"error": "Game not found"}), 404)
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    return jsonify(users)

if __name__ == '__main__':
    app.run(port=5555, debug=True)


if __name__ == '__main__':
    app.run(port=5555, debug=True)


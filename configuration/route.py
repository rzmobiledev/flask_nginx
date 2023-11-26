from flask import Blueprint
from flask import jsonify, make_response, request
from .models import User, Article
from configuration.base import db, encrypt
import socket

router = Blueprint('router', __name__)



@router.route("/")
def home():
    return make_response(jsonify({'message': f'Welcome to our page with container id: {socket.gethostname()}'}, 200))


@router.route("/api/user", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        user = User(username=data["username"], email=data["email"], password=encrypt(data["password"]))
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User created.'}))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    
@router.route("/api/user", methods=["GET"])
def get_user():
    try:
        users = User.query.all()
        return make_response(
            jsonify(
                {
                    'users': [user.json() for user in users]
                }
            ), 200
        )
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@router.route("/api/article", methods=["POST"])
def create_article():
    try:
        data = request.get_json()
        article = Article(article=data['article'])
        db.session.add(article)
        db.session.commit()
        return make_response(jsonify({'message': 'Article created.'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}))
    

@router.route("/api/article", methods=["GET"])
def get_articles():
    try:
        articles = Article.query.all()
        return make_response(jsonify({'articles': [article.article for article in articles]}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}))


@router.route("/api/article/<int:id>", methods=["PUT"])
def change_user(id):
    try:
        article = Article.query.filter_by(id=id).first()
        if article:
            data = request.get_json()
            article['article'] = data['article']
            db.session.commit()
            return make_response(jsonify({'message': 'article updated.'}), 200)
        return make_response(jsonify({'error': "article not found."}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@router.route("/api/article/<int:id>")
def delete_article(id):
    try:
        article = Article.query.filter_by(id=id).first()
        if article:
            db.session.delete(article)
            db.session.commit()
            return make_response(jsonify({'message': 'article deleted.'}), 200)
        return make_response(jsonify({'error': 'article not found.'}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}))

from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, BookSchema, BookSchema, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'apples': 'bananas'}

# Insert book into database
@api.route('/books', methods = ['POST'])
@token_required
def create_book_data(current_user_token):
    title = request.json['title']
    author = request.json['author']
    genre = request.json['genre']
    length = request.json['length']
    ISBN = request.json['ISBN']
    user_token = current_user_token.token

    print(f'BIG TEST: {current_user_token.token}')

    book = Book(title, author, genre, length, ISBN, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# Retrieve all books like you're Belle from Beauty and the Beast
@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# Retrieve a single book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

# Update contact info
# 'PUT' is the replace command
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.title = request.json['title']
    book.author = request.json['author']
    book.genre = request.json['genre']
    book.length = request.json['length']
    book.ISBN = request.json['ISBN']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# Delete a book
# IMPORTANT: DELETE BY ID because otherwise you delete the whole database
# and get fired from your tech job
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)   
#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask import abort
from flask import request
from flask_cors import cross_origin

from flask_mysqldb import MySQL

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Get all books
# For testing: curl -i http://localhost:5000/books
@app.route('/books', methods=['GET'])
@cross_origin()
def get_books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from books")
    books = cur.fetchall()
    return jsonify({'books': books})

# Get one book by id
# For testing: curl -i http://localhost:5000/books/2
@app.route('/books/<int:book_id>', methods=['GET'])
@cross_origin()
def get_book(book_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from books WHERE id=" + str(book_id))
        book = cur.fetchall()

        if not book:
            # Raise an HTTP 404 error if the book is not found
            abort(404, description="Book not found")

        return jsonify({'book': book[0]})
    except Exception as e:
	# Log the exception for debugging purposes
        app.logger.error("Exception occurred: %s", str(e))
        # Create a JSON response with a "Bad Request" status (HTTP 400)
        response = jsonify({'error': str(e)})
        return make_response(response, 400)

# Add new book
# For testing: curl -i -H "Content-Type: application/json" -X POST -d '{"title":"El libro"}' http://localhost:5000/books
@app.route('/books', methods=['POST'])
@cross_origin()
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    title = request.json.get('title', "")
    description = request.json.get('description', "")
    author = request.json.get('author', "")
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO books(title,description,author) VALUES(%s,%s,%s)",(title,description,author))
    mysql.connection.commit()
    return jsonify({'book': request.json}), 201

# Edit a Book
# For testing: curl -i -H "Content-Type: application/json" -X PUT -d '{"author":"Jorgito"}' http://localhost:5000/books/2
@app.route('/books/<int:book_id>', methods=['PUT'])
@cross_origin()
def update_book(book_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books where id="+str(book_id))
    book = cur.fetchall()
    print(book[0])
    title = request.json.get('title', book[0]['title'])
    description = request.json.get('description', book[0]['description'])
    author = request.json.get('author', book[0]['author'])
    cur.execute("UPDATE books SET title =%s, description =%s ,author= %s WHERE id=%s",(title,description,author,book_id))
    mysql.connection.commit()
    return jsonify({'book': book[0]})

# Delete a Book
# For testing: curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/books/1
@app.route('/books/<int:book_id>', methods=['DELETE'])
@cross_origin()
def delete_book(book_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id="+str(book_id))
    mysql.connection.commit()
    return jsonify({'result': True})
    
if __name__ == '__main__':
    app.run(debug=True)

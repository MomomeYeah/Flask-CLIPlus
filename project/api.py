from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
api = Api(app, version='1.0', title='Author API',
    description='A simple Author API'
)

ns_author = api.namespace('authors', description='Author operations')
ns_book = api.namespace('books', description='Book operations')

author = api.model("Author", {
    'name': fields.String(required=True, description='The name of the author')
})

author_list = api.model('AuthorList', {
    'id':   fields.Integer(readOnly=True, description='Unique identifier'),
    'name': fields.String(required=True, description='The name of the author')
})

book = api.model("Book", {
    'author_id':        fields.Integer(readOnly=True, description='ID of this book''s author'),
    'title':            fields.String(required=True, description='Title of this book'),
    'published_year':   fields.Integer(required=True, description='Year this book was published')
})

book_list = api.model("BookList", {
    'id':               fields.Integer(readOnly=True, description='Unique identifier'),
    'author_id':        fields.Integer(readOnly=True, description='ID of this book''s author'),
    'title':            fields.String(required=True, description='Title of this book'),
    'published_year':   fields.Integer(required=True, description='Year this book was published')
})

class AuthorDAO(object):
    def __init__(self):
        self.counter = 0
        self.authors = []

    def get(self, id):
        for author in self.authors:
            if author['id'] == id:
                return author
        api.abort(404, "Author doesn't exist")

    def create(self, data):
        name = data.get("name")
        if not name:
            api.abort(404, "Invalid author details")

        author = data
        author['id'] = self.counter = self.counter + 1
        self.authors.append(author)
        return author

    def update(self, id, data):
        author = self.get(id)

        name = data.get("name")
        if not name:
            api.abort(404, "Invalid author details")

        author.update(data)
        return author

    def delete(self, id):
        author = self.get(id)
        self.authors.remove(author)

class BookDAO(object):
    def __init__(self):
        self.counter = 0
        self.books = []

    def get(self, id):
        for book in self.books:
            if book['id'] == id:
                return book
        api.abort(404, "Book doesn't exist")

    def get_by_author(self, author_id):
        books = []
        for book in self.books:
            if book['author_id'] == str(author_id):
                books.append(book)
        return books

    def create(self, data):
        author_id = data.get("author_id")
        title = data.get("title")
        published_year = data.get("published_year")
        if not author_id or not title or not published_year:
            api.abort(404, "Invalid book details")

        book = data
        book['id'] = self.counter = self.counter + 1
        self.books.append(book)
        return book

    def update(self, id, data):
        book = self.get(id)

        author_id = data.get("author_id")
        title = data.get("title")
        published_year = data.get("published_year")
        if not author_id and not title and not published_year:
            api.abort(404, "Invalid book details")

        book.update(data)
        return book

    def delete(self, id):
        book = self.get(id)
        self.books.remove(book)

ADAO = AuthorDAO()
ADAO.create({'name': 'Haruki Murakami'})
ADAO.create({'name': 'Ernest Hemingway'})
ADAO.create({'name': 'F. Scott Fitzgerald'})

BDAO = BookDAO()
BDAO.create({'author_id': '1', 'title': 'Kafka on the Shore', 'published_year': 2002})
BDAO.create({'author_id': '1', 'title': 'The Wind-Up Bird Chronicle', 'published_year': 1994})
BDAO.create({'author_id': '2', 'title': 'A Farewell to Arms', 'published_year': 1929})
BDAO.create({'author_id': '3', 'title': 'The Great Gatsby', 'published_year': 1925})

@ns_author.route('/')
class AuthorList(Resource):
    '''Shows a list of all authors, and lets you POST to add new ones'''
    @ns_author.doc('list_authors')
    @ns_author.marshal_list_with(author_list)
    def get(self):
        '''List all tasks'''
        return ADAO.authors

    @ns_author.doc('create_author')
    @ns_author.expect(author)
    @ns_author.marshal_with(author_list, code=201)
    def post(self):
        '''Create a new author'''
        return ADAO.create(api.payload), 201


@ns_author.route('/<int:id>')
@ns_author.response(404, 'Author not found')
@ns_author.param('id', 'The author identifier')
class Author(Resource):
    '''Show a single author item and lets you delete them'''
    @ns_author.doc('get_author')
    @ns_author.marshal_with(author_list)
    def get(self, id):
        '''Fetch a given resource'''
        return ADAO.get(id)

    @ns_author.doc('delete_author')
    @ns_author.response(204, 'Author deleted')
    def delete(self, id):
        '''Delete an author given its identifier'''
        ADAO.delete(id)
        return '', 204

    @ns_author.expect(author)
    @ns_author.marshal_with(author_list)
    def put(self, id):
        '''Update an author given its identifier'''
        return ADAO.update(id, api.payload)

author_article_list = api.model('AuthorArticleList', {
    'id':   fields.Integer(readOnly=True, description='Unique identifier'),
    'name': fields.String(required=True, description='The name of the article')
})
@ns_author.route('/<int:id>/publications/articles')
@ns_author.response(404, 'Author not found')
@ns_author.param('id', 'The author identifier')
class AuthorArticles(Resource):
    @ns_author.doc('get_author_articles')
    @ns_author.marshal_list_with(author_article_list)
    def get(self, id):
        '''Fetch a given resource'''
        return []

author_book_list = api.model('AuthorBookList', {
    'id':       fields.Integer(readOnly=True, description='Unique author identifier'),
    'author':   fields.String(required=True, description='Author name'),
    'title':    fields.String(required=True, description='Book title')
})
@ns_author.route('/<int:id>/publications/books')
@ns_author.response(404, 'Author not found')
@ns_author.param('id', 'The author identifier')
class AuthorBooks(Resource):
    @ns_author.doc('get_author_books')
    @ns_author.marshal_list_with(author_book_list)
    def get(self, id):
        '''Fetch a given resource'''
        book_list = BDAO.get_by_author(id)
        for book in book_list:
            book["author"] = ADAO.get(id).get('name')
        return book_list

author_short_story_list = api.model('AuthorShortStoryList', {
    'id':   fields.Integer(readOnly=True, description='Unique identifier'),
    'name': fields.String(required=True, description='The name of the short story')
})
@ns_author.route('/<int:id>/publications/short-stories')
@ns_author.response(404, 'Author not found')
@ns_author.param('id', 'The author identifier')
class AuthorShortStories(Resource):
    @ns_author.doc('get_author_short_stories')
    @ns_author.marshal_list_with(author_short_story_list)
    def get(self, id):
        '''Fetch a given resource'''
        return []

@ns_book.route('/')
class BookList(Resource):
    '''Shows a list of all books, and lets you POST to add new ones'''
    @ns_book.doc('list_books')
    @ns_book.marshal_list_with(book_list)
    def get(self):
        '''List all books'''
        return BDAO.books

    @ns_book.doc('create_book')
    @ns_book.expect(book)
    @ns_book.marshal_with(book_list, code=201)
    def post(self):
        '''Create a new book'''
        return BDAO.create(api.payload), 201


@ns_book.route('/<int:id>')
@ns_book.response(404, 'Book not found')
@ns_book.param('id', 'The book identifier')
class Book(Resource):
    '''Show a single book item and lets you delete them'''
    @ns_book.doc('get_book')
    @ns_book.marshal_with(book_list)
    def get(self, id):
        '''Fetch a given resource'''
        return BDAO.get(id)

    @ns_book.doc('delete_book')
    @ns_book.response(204, 'Book deleted')
    def delete(self, id):
        '''Delete a book given its identifier'''
        BDAO.delete(id)
        return '', 204

    @ns_book.expect(book)
    @ns_book.marshal_with(book_list)
    def put(self, id):
        '''Update a book given its identifier'''
        return BDAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5123)

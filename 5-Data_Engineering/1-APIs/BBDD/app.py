from flask import Flask, jsonify, request
from datos_dummy import books

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# 1.Ruta para obtener todos los libros
@app.route('/api/v0/resources/books/all', methods=['GET'])
def get_all():
    return jsonify(books)

# 2.Ruta para obtener un libro concreto mediante su id como parámetro en la llamada
@app.route('/api/v0/resources/book', methods=['GET'])
def book_id():
    results = []
    if 'id' in request.args:
        id = int(request.args['id'])
        for book in books:
            if book['id']==id:
                results.append(book)
        if results == []:
            return "Book not found with the id requested"    
        else:
            return jsonify(results)
    else:
        return "No id field provided"


# 3.Ruta para obtener un libro concreto mediante su título como parámetro en la llamada de otra forma
@app.route('/api/v0/resources/book/<string:title>', methods=['GET'])
def book_title(title):
    results = []

    for book in books:
        if book['title']==title:
            results.append(book)
    if results == []:
        return "Book not found with the title requested"    
    else:
        return jsonify(results)



# 4.Ruta para obtener un libro concreto mediante su título dentro del cuerpo de la llamada
@app.route('/api/v1/resources/book', methods=['GET'])
def book_test():
    title = request.get_json().get("title")
    results = []

    for book in books:
        if book['title']==title:
            results.append(book)
    if results == []:
        return "Book not found with the title requested"    
    else:
        return jsonify(results)
    

    


# 5.Ruta para añadir un libro mediante parámetros en la llamada
@app.route('/api/v1/resources/book/add', methods=['POST'])
def add_book_args():
    book = request.args

    books.append(book)

    return books



# 6.Ruta para añadir un libro de otra forma 1
@app.route('/api/v1/resources/book/add_parameters', methods=['POST'])
def add_book_body():
    book = request.get_json()

    books.append(book)

    return books


# 7.Ruta para modificar un libro
@app.route('/api/v1/resources/book/update', methods=['PUT'])
def modify():
    old_title = request.args.get("title")
    new_book = request.get_json()
    print("old_title: ", old_title)
    for book in books:
        print("book_title", book["title"])
        print("----------")
        if book["title"] == old_title:
            old_id  = book["id"]
            new_book["id"] = old_id
            indice = books.index(book)
            books.pop(indice)
            books.insert(indice, new_book)
            return books
        
    return "book not found"
    

# 8.Ruta para eliminar un libro
# @app.route('/api/v1/resources/book/delete', methods=['DELETE'])


app.run()
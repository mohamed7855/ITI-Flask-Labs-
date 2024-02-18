from flask import Flask
from flask import request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime


app = Flask(__name__)  # initialize the application in the main of the current module

"sqllite_"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db= SQLAlchemy(app)  # create instance folder---> contain project.db

# use db object ---> create model ---> used later in create table and crud
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    no_of_pages = db.Column(db.Integer)
    price = db.Column(db.Integer)
    image = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)



    def __str__(self):
        return f"{self.title}"
    
@app.route("/", endpoint='homePage')
def home():
    return render_template('index.html')

@app.route("/books",endpoint='books.index')
def books_index():
    books=Book.query.all()
    return render_template('books/index.html',books=books)

@app.route("/books/<int:id>", endpoint="book.details")
def book_details(id):
    book = Book.query.get_or_404(id)
    return render_template("books/details.html", book=book)

@app.route("/books/delete/<int:id>", endpoint="book.delete")
def book_delete(id):
    print("==========>>>>>>>>", id)
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books.index'))

@app.route("/books/create",methods =['GET', 'POST'], endpoint='book.create')
def create_book():
    ## post
    print(request.form)
    if request.method == 'POST':
        
        book = Book(title=request.form['title'], no_of_pages=request.form['nPages'],
                    price=request.form['price'])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.index'))

    ## get
    return render_template("books/create.html")


@app.route("/books/update/<int:id>",methods =['GET', 'POST'], endpoint="book.update")
def book_update(id):
    if request.method == 'POST':
        book = Book.query.get_or_404(id)
        book.title = request.form['title']
        book.no_of_pages = request.form['nPages']
        book.price = request.form['price']
        db.session.commit()
        return redirect(url_for('books.index'))
        
    ## get
    book = Book.query.get_or_404(id)
    return render_template("books/update.html", book=book)








@app.route("/home")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
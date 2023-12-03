import mysql.connector
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'user',
    'password': 'password',
    'database': 'library'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/initialize_db', methods=['POST'])
def create_tables():
    try:
        initialize_db()
        return jsonify({"message": "Database initialized and tables created successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def initialize_db():
    connection = get_db_connection()
    cur = connection.cursor()

    # Create Authors Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Authors (
                    authorID INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    bio VARCHAR(255))''')

    # Create Genres Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Genres (
                    genreID INTEGER PRIMARY KEY AUTO_INCREMENT,
                    genreName VARCHAR(255) NOT NULL)''')

    # Create Publishers Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Publishers (
                    publisherID INTEGER PRIMARY KEY AUTO_INCREMENT,
                    publisherName VARCHAR(255) NOT NULL,
                    contactInfo VARCHAR(255),
                    INDEX (publisherName))''')

    # Create Books Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Books (
                    bookID INTEGER PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(255) NOT NULL,
                    publicationDate VARCHAR(255),
                    publisherID INTEGER,
                    availabilityStatus TINYINT(1) DEFAULT TRUE,
                    bookCount INTEGER DEFAULT 1,
                    FOREIGN KEY (publisherID) REFERENCES Publishers(publisherID),
                    INDEX (title),
                    INDEX (publicationDate),
                    INDEX (publisherID))''')

    # Create Users Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                    userID INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    contactDetails VARCHAR(255),
                    borrowingHistory VARCHAR(255),
                    preferences VARCHAR(255),
                    INDEX (name),
                    INDEX (contactDetails))''')

    # Create Transactions Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Transactions (
                    transactionID INTEGER PRIMARY KEY AUTO_INCREMENT,
                    userID INTEGER,
                    bookID INTEGER,
                    borrowDate VARCHAR(255),
                    returnDate VARCHAR(255),
                    FOREIGN KEY (userID) REFERENCES Users(userID),
                    FOREIGN KEY (bookID) REFERENCES Books(bookID),
                    INDEX (userID),
                    INDEX (bookID))''')

    # Create Book_Authors Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Book_Authors (
                    bookID INTEGER,
                    authorID INTEGER,
                    PRIMARY KEY (bookID, authorID),
                    FOREIGN KEY (bookID) REFERENCES Books(bookID),
                    FOREIGN KEY (authorID) REFERENCES Authors(authorID),
                    INDEX (bookID),
                    INDEX (authorID))''')

    # Create Book_Genres Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Book_Genres (
                    bookID INTEGER,
                    genreID INTEGER,
                    PRIMARY KEY (bookID, genreID),
                    FOREIGN KEY (bookID) REFERENCES Books(bookID),
                    FOREIGN KEY (genreID) REFERENCES Genres(genreID),
                    INDEX (bookID),
                    INDEX (genreID))''')

    # Create Cart Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Cart (
                        cartID INTEGER PRIMARY KEY AUTO_INCREMENT,
                        userID INTEGER,
                        FOREIGN KEY (userID) REFERENCES Users(userID),
                        INDEX (userID))''')

    # Create Cart_Items Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Cart_Items (
                        cartID INTEGER,
                        bookID INTEGER,
                        bookName VARCHAR(255),
                        PRIMARY KEY (cartID, bookID),
                        FOREIGN KEY (cartID) REFERENCES Cart(cartID),
                        FOREIGN KEY (bookID) REFERENCES Books(bookID),
                        INDEX (cartID),
                        INDEX (bookID))''')

    connection.commit()
    connection.close()
    print("Database initialized and tables created")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/populate_db', methods=['POST'])
def populate_db():
    try:
        insert_data()
        return jsonify({"message": "Data inserted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def insert_data():
    connection = get_db_connection()
    cur = connection.cursor()

    # Inserting Authors
    authors = [
        ('J.K. Rowling', 'British author known for the Harry Potter series.'),
        ('George R.R. Martin', 'American novelist known for the A Song of Ice and Fire series.'),
        ('Rick Riordan', 'American author known for the Percy Jackson & the Olympians series.'),
        ('Suzanne Collins', 'American author known for The Hunger Games series.'),
        ('Markus Zusak', 'Australian author known for The Book Thief.')
    ]
    cur.executemany("INSERT INTO Authors (name, bio) VALUES (%s, %s)", authors)

    # Inserting Genres
    genres = [('Fantasy',), ('Adventure',), ('Dystopian',), ('Historical Fiction',)]
    cur.executemany("INSERT INTO Genres (genreName) VALUES (%s)", genres)

    # Inserting Publishers
    publishers = [
        ('Bloomsbury', 'London, UK'),
        ('Bantam Books', 'New York, USA'),
        ('Disney Hyperion', 'New York, USA'),
        ('Scholastic', 'Pennsylvania, USA'),
        ('Picador', 'London, UK')
    ]
    cur.executemany("INSERT INTO Publishers (publisherName, contactInfo) VALUES (%s, %s)", publishers)

    # Inserting Books
    books = [
        ('Harry Potter and the Philosopher\'s Stone', '1997-06-26', 1),
        ('Harry Potter and the Chamber of Secrets', '1998-07-02', 1),
        ('Harry Potter and the Prisoner of Azkaban', '1999-07-08', 1),
        ('Harry Potter and the Goblet of Fire', '2000-07-08', 1),
        ('Harry Potter and the Order of the Phoenix', '2003-06-21', 1),
        ('Harry Potter and the Half-Blood Prince', '2005-07-16', 1),
        ('Harry Potter and the Deathly Hallows', '2007-07-21', 1),
        ('A Game of Thrones', '1996-08-01', 2),
        ('A Clash of Kings', '1998-11-16', 2),
        ('A Storm of Swords', '2000-08-08', 2),
        ('A Feast for Crows', '2005-10-17', 2),
        ('A Dance with Dragons', '2011-07-12', 2),
        ('The Lightning Thief', '2005-06-28', 3),
        ('The Sea of Monsters', '2006-04-03', 3),
        ('The Titan\'s Curse', '2007-05-01', 3),
        ('The Battle of the Labyrinth', '2008-05-06', 3),
        ('The Last Olympian', '2009-05-05', 3),
        ('The Hunger Games', '2008-09-14', 4),
        ('Catching Fire', '2009-09-01', 4),
        ('Mockingjay', '2010-08-24', 4),
        ('The Book Thief', '2005-03-14', 5)
    ]
    cur.executemany("INSERT INTO Books (title, publicationDate, publisherID) VALUES (%s, %s, %s)", books)

    # Committing the changes
    connection.commit()
    connection.close()


@app.route('/populate_associations', methods=['POST'])
def populate_associations():
    try:
        populate_book_genres()
        populate_book_authors()
        return jsonify({"message": "Book_Genres and Book_Authors tables populated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def populate_book_genres():
    connection = get_db_connection()
    cur = connection.cursor()

    # Assuming the genre IDs are 1: Fantasy, 2: Adventure, 3: Dystopian, 4: Historical Fiction
    # Assuming the book IDs are in the order they were inserted
    cur.executemany("INSERT INTO Book_Genres (bookID, genreID) VALUES (%s, %s)", [
        (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),  # Harry Potter series
        (8, 1), (9, 1), (10, 1), (11, 1), (12, 1),  # Game of Thrones series
        (13, 1), (13, 2), (14, 1), (14, 2), (15, 1), (15, 2), (16, 1), (16, 2), (17, 1), (17, 2),
        # Percy Jackson series
        (18, 2), (18, 3), (19, 2), (19, 3), (20, 2), (20, 3),  # Hunger Games series
        (21, 4)  # The Book Thief
    ])

    connection.commit()
    connection.close()


def populate_book_authors():
    connection = get_db_connection()
    cur = connection.cursor()

    # Assuming the author IDs are 1: J.K. Rowling, 2: George R.R. Martin, 3: Rick Riordan, 4: Suzanne Collins, 5: Markus Zusak
    # Assuming the book IDs are in the order they were inserted
    cur.executemany("INSERT INTO Book_Authors (bookID, authorID) VALUES (%s, %s)", [
        (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),  # Harry Potter series
        (8, 2), (9, 2), (10, 2), (11, 2), (12, 2),  # Game of Thrones series
        (13, 3), (14, 3), (15, 3), (16, 3), (17, 3),  # Percy Jackson series
        (18, 4), (19, 4), (20, 4),  # Hunger Games series
        (21, 5)  # The Book Thief
    ])

    connection.commit()
    connection.close()


@app.route('/books/all', methods=['GET'])
def get_all_books():
    connection = None
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("SELECT * FROM Books")
        books = cur.fetchall()  # Fetches all rows of a query result
        connection.close()
        books_list = [dict(zip([column[0] for column in cur.description], book)) for book in books]
        return jsonify({"books": books_list})
    except Exception as e:
        # Error handling
        if connection:
            connection.close()
        return jsonify({"error": str(e)}), 500


@app.route('/books/add', methods=['POST'])
def add_new_book():
    title = request.form.get('title')
    publication_date = request.form.get('publicationDate')
    publisher_id = request.form.get('publisherID')
    availability_status = request.form.get('availabilityStatus')

    if not all([title, publication_date, publisher_id, availability_status]):
        return jsonify({"error": "Please input all book information."}), 400

    connection = None
    try:
        connection = get_db_connection()
        cur = connection.cursor()

        # Check if the publisher exists
        cur.execute("SELECT publisherID FROM Publishers WHERE publisherID=%s", (publisher_id,))
        if not cur.fetchone():
            raise ValueError(f"Publisher with ID {publisher_id} does not exist.")

        cur.execute("SELECT bookID, bookCount FROM Books WHERE title=%s", (title,))
        existing_book = cur.fetchone()

        if existing_book:
            new_count = existing_book[1] + 1
            cur.execute("UPDATE Books SET bookCount = %s WHERE bookID = %s", (new_count, existing_book[0]))
            message = "Book count incremented successfully."
        else:
            cur.execute(
                "INSERT INTO Books (title, publicationDate, publisherID, availabilityStatus) VALUES (%s, %s, %s, %s)",
                (title, publication_date, publisher_id, availability_status))
            message = "Book added successfully."

        connection.commit()
        return jsonify({"message": message}), 201

    except mysql.connector.Error as db_err:
        if connection:
            connection.rollback()
        return jsonify({"error": "Database error: " + str(db_err)}), 500
    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
    finally:
        if connection:
            connection.close()


@app.route('/books/remove', methods=['POST'])
def remove_book():
    book_id = request.form.get('bookID')

    if not book_id:
        return jsonify({"error": "Book ID is required."}), 400

    connection = get_db_connection()
    try:
        cur = connection.cursor()
        # Check if the book exists
        cur.execute("SELECT * FROM Books WHERE bookID=%s", (book_id,))
        book = cur.fetchone()
        if not book:
            return jsonify({"error": "Book not found."}), 404

        # Delete the book from the database
        cur.execute("DELETE FROM Books WHERE bookID=%s", (book_id,))
        connection.commit()
        return jsonify({"message": "Book removed successfully."}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"error": "An error occurred: " + str(e)}), 500
    finally:
        connection.close()


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    connection = get_db_connection()
    cur = connection.cursor()

    # Get book details
    cur.execute("SELECT * FROM Books WHERE bookID=%s", (book_id,))
    book = cur.fetchone()

    # Get authors of the book
    cur.execute('''SELECT a.name FROM Authors a
                   JOIN Book_Authors ba ON a.authorID = ba.authorID
                   WHERE ba.bookID=%s''', (book_id,))
    authors = [author[0] for author in cur.fetchall()]

    # Get genres of the book
    cur.execute('''SELECT g.genreName FROM Genres g
                   JOIN Book_Genres bg ON g.genreID = bg.genreID
                   WHERE bg.bookID=%s''', (book_id,))
    genres = [genre[0] for genre in cur.fetchall()]

    connection.close()
    return jsonify({
        "book": book,
        "authors": authors,
        "genres": genres
    })


@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form.get('name')
    contact_details = request.form.get('contactDetails')

    if not name or not contact_details:
        return jsonify({"error": "Missing name or contact details in request."}), 400

    connection = None
    try:
        connection = get_db_connection()
        cur = connection.cursor()

        cur.execute("SELECT * FROM Users WHERE contactDetails=%s", (contact_details,))
        if cur.fetchone():
            return jsonify({"error": "Email ID already registered."}), 409

        cur.execute("INSERT INTO Users (name, contactDetails) VALUES (%s, %s)", (name, contact_details))
        connection.commit()
        return jsonify({"message": "User registered successfully!"}), 201

    except mysql.connector.Error as db_err:
        if connection:
            connection.rollback()
        return jsonify({"error": "Database error: " + str(db_err)}), 500
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
    finally:
        if connection and connection.is_connected():
            connection.close()


@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form.get('userID')
    name = request.form.get('userName')
    contact_details = request.form.get('contactDetails')

    connection = get_db_connection()
    try:
        cur = connection.cursor()
        # Update user details
        cur.execute("UPDATE Users SET name=%s, contactDetails=%s WHERE userID=%s",
                    (name, contact_details, user_id))
        if cur.rowcount == 0:
            return jsonify({"error": "User not found."}), 404
        connection.commit()
        return jsonify({"message": "User updated successfully."}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"error": "An error occurred: " + str(e)}), 500
    finally:
        connection.close()


@app.route('/create_cart', methods=['POST'])
def create_cart():
    user_id = request.form.get('userID')

    connection = None
    try:
        connection = get_db_connection()
        cur = connection.cursor()

        # Start transaction
        connection.start_transaction()

        # Check if the user exists for the provided userID
        cur.execute("SELECT * FROM Users WHERE userID=%s", (user_id,))
        user = cur.fetchone()
        if not user:
            connection.rollback()
            return jsonify({"error": "User not found. Please register before creating a cart."}), 404

        # Check if the cart already exists for the provided userID
        cur.execute("SELECT * FROM Cart WHERE userID=%s", (user_id,))
        existing_cart = cur.fetchone()
        if existing_cart:
            connection.rollback()
            return jsonify({"error": "A cart already exists for this user."}), 409

        cur.execute("INSERT INTO Cart (userID) VALUES (%s)", (user_id,))
        connection.commit()
        return jsonify({"message": "Cart created successfully for the user."}), 201

    except mysql.connector.Error as err:
        # Error Handling
        if connection:
            connection.rollback()
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection:
            connection.close()


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    cart_id = request.form.get('cartID')
    book_id = request.form.get('bookID')

    connection = get_db_connection()
    cur = connection.cursor()

    print("Cart ID:", cart_id)
    print("Book ID:", book_id)

    # Check if the cart exists for the provided cartID
    cur.execute("SELECT * FROM Cart WHERE cartID=%s", (cart_id,))
    cart = cur.fetchone()
    if not cart:
        print("No cart found for Cart ID:", cart_id)
        connection.close()
        return jsonify({"error": "Cart not found. Please create a cart first."}), 404

    # Check if the cart exists for the provided cartID
    cur.execute("SELECT * FROM Cart WHERE cartID=%s", (cart_id,))
    cart = cur.fetchone()
    if not cart:
        connection.close()
        return jsonify({"error": "Cart not found. Please create a cart first."}), 404

    # Fetch the book's name
    cur.execute("SELECT title FROM Books WHERE bookID=%s", (book_id,))
    book_result = cur.fetchone()
    if not book_result:
        connection.close()
        return jsonify({"error": "Book not found."}), 404
    book_name = book_result[0]

    # Insert into Cart_Items
    cur.execute("INSERT INTO Cart_Items (cartID, bookID, bookName) VALUES (%s, %s, %s)", (cart_id, book_id, book_name))

    connection.commit()
    connection.close()

    return jsonify({"message": "Book added to cart successfully!"}), 201


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Access form data instead of JSON
    cart_id = request.form.get('cartID')
    book_id = request.form.get('bookID')

    connection = get_db_connection()
    try:
        cur = connection.cursor()
        # Check if the book is in the cart
        cur.execute("SELECT * FROM Cart_Items WHERE cartID=%s AND bookID=%s", (cart_id, book_id))
        item = cur.fetchone()
        if not item:
            return jsonify({"error": "Book not found in the cart."}), 404

        # Remove the book from the cart
        cur.execute("DELETE FROM Cart_Items WHERE cartID=%s AND bookID=%s", (cart_id, book_id))
        connection.commit()
        return jsonify({"message": "Book removed from cart successfully."}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"error": "An error occurred: " + str(e)}), 500
    finally:
        connection.close()


@app.route('/view_cart', methods=['GET'])
def view_cart():
    cart_id = request.args.get('cartID')
    if not cart_id:
        return jsonify({"error": "Cart ID is required."}), 400

    connection = None
    try:
        connection = get_db_connection()
        cur = connection.cursor()

        # Check if the cart exists for the provided cartID
        cur.execute("SELECT * FROM Cart WHERE cartID=%s", (cart_id,))
        cart = cur.fetchone()
        if not cart:
            return jsonify({"error": "Cart not found."}), 404

        # Retrieve the books in the cart
        cur.execute('''SELECT b.title FROM Books b
                       JOIN Cart_Items ci ON b.bookID = ci.bookID
                       WHERE ci.cartID=%s''', (cart_id,))
        books_in_cart = [book[0] for book in cur.fetchall()]
        return jsonify({"books_in_cart": books_in_cart})
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500
    finally:
        if connection:
            connection.close()


@app.route('/reports/advanced', methods=['GET'])
def advanced_report():
    connection = None
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('''
            SELECT 
                Users.name AS user_name,
                Books.title AS book_title,
                COUNT(Transactions.bookID) AS loan_count,
                Publishers.publisherName AS publisher_name,
                (SELECT COUNT(*) FROM Cart_Items WHERE Cart_Items.bookID = Books.bookID) AS cart_count
            FROM 
                Users
            JOIN 
                Transactions ON Users.userID = Transactions.userID
            JOIN 
                Books ON Transactions.bookID = Books.bookID
            JOIN 
                Publishers ON Books.publisherID = Publishers.publisherID
            GROUP BY 
                Users.name, Books.title, Publishers.publisherName, Books.bookID
            ORDER BY 
                loan_count DESC, cart_count DESC
            LIMIT 10;
        ''')
        report_data = cur.fetchall()
        connection.close()

        # Format the report data into a JSON-friendly structure
        report = [
            {
                "user_name": row[0],
                "book_title": row[1],
                "loan_count": row[2],
                "publisher_name": row[3],
                "cart_count": row[4]
            }
            for row in report_data
        ]

        return jsonify(report)
    except Exception as e:
        if connection:
            connection.close()
        return jsonify({"error": str(e)}), 500


@app.route('/checkout', methods=['POST'])
def checkout():
    user_name = request.form.get('userName')
    cart_id = request.form.get('cartID')

    connection = None

    try:
        connection = get_db_connection()
        cur = connection.cursor()

        cur.execute("SELECT userID FROM Users WHERE name=%s", (user_name,))
        user_result = cur.fetchone()
        if not user_result:
            return jsonify({"error": "User not found."}), 404

        cur.execute("SELECT bookID FROM Cart_Items WHERE cartID=%s", (cart_id,))
        cart_items = cur.fetchall()
        if not cart_items:
            return jsonify({"error": "Cart is empty or does not exist."}), 400

        for item in cart_items:
            book_id = item[0]
            cur.execute("SELECT bookCount FROM Books WHERE bookID=%s AND availabilityStatus=1", (book_id,))
            book = cur.fetchone()
            if not book or book[0] <= 0:
                raise Exception(f"Book ID {book_id} is not available for checkout.")

            cur.execute("UPDATE Books SET bookCount = bookCount - 1 WHERE bookID=%s", (book_id,))
            cur.execute("INSERT INTO Transactions (userID, bookID, borrowDate) VALUES (%s, %s, NOW())", (user_result[0], book_id))

        cur.execute("DELETE FROM Cart_Items WHERE cartID=%s", (cart_id,))
        connection.commit()
        return jsonify({"message": "Checkout successful."}), 200

    except mysql.connector.Error as db_err:
        connection.rollback()
        return jsonify({"error": "Database error: " + str(db_err)}), 500
    except Exception as e:
        connection.rollback()
        return jsonify({"error": "An error occurred during checkout: " + str(e)}), 500
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(port=5040)

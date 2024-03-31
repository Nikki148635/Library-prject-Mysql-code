from flask import Flask, render_template
from flask import jsonify, make_response
import mysql.connector

app = Flask(__name__)

# def handle_error(message, status_code=400): 
#     return jsonify({"error": message}), status_code

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Abhishek@123',
    'database': 'nikki_db'
}

def fetch_data():   
    
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)  
    except mysql.connector.Error as err:
        return jsonify({'error': f'Database connection error: {err}'}), 500
    try:
        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()
        print(data)
        book_data = []
        for document in data: 
            document['_id'] = str(document['_id'])
            book_data.append(document)
            print(book_data)
            return make_response(jsonify(book_data), 200)
    except mysql.connector.Error as err:
        return jsonify({'error': f'Query execution error: {err}'}), 500
    finally:
        if connection.is_connected():
            connection.close()
    # Convert data to JSON
    # json_data = jsonify(data)

@app.route('/data')
def display_data():
    tempdata=fetch_data()     
    json_all_data = jsonify({'my_books': tempdata})
    print(json_all_data)
    return json_all_data

# Route for index page
@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/books", methods=["GET"])
# def search_books():
#     getbook = request.get_json()
#     print(getbook)
#     if not getbook:
#         return jsonify ({'error': 'No data provided'}), 400
#     book_id = getbook.get('Book_id')
#     print(book_id)
#     title = getbook.get('title')
#     print(title)
#     author = getbook.get('Author') # Validate data
#     print(author)
#     sql = "INSERT INTO books (book_id, Title, Author) VALUES (%s, %s, %s)"
#     val = (book_id, title, author)   
#     cursor.execute(sql, val)
#     if not title or not author:
#         return jsonify({'error': 'Missing required fields'}), 400
# # Process data (store in database, etc. ) #
#     return jsonify({'message': 'Book added success fully '}), 201

# # Commit the changes
# connection.commit()

# # Close the connection
# connection.close()


if __name__ == "__main__":
    app.run(debug=True)
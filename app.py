from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "caircocoders-ednalan"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "search"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ajaxlivesearch', methods=["POST"])
def ajaxlivesearch():
    cursor = mysql.connection.cursor()
    search_results = []
    total_results = 0

    if request.method == "POST":
        search_word = request.form.get('query')
        print(search_word)

        if search_word == '':
            query = "SELECT * FROM search ORDER BY id"
            cursor.execute(query)
            search_results = cursor.fetchall()
        else:
            query = """SELECT * FROM search 
                       WHERE genre LIKE %s OR performer LIKE %s OR title LIKE %s 
                       ORDER BY id DESC LIMIT 20"""
            search_pattern = f"%{search_word}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            search_results = cursor.fetchall()

        total_results = cursor.rowcount
        print(total_results)

    cursor.close()
    return jsonify({'resulthtml': render_template('result.html', search=search_results, rows=total_results)})


if __name__ == "__main__":
    app.run(debug=True)

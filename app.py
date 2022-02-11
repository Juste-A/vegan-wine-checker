from flask import Flask, render_template, request, url_for, redirect, abort
import sqlite3 as sql

app = Flask(__name__)

# connect to database
def wines_db():
    conn = sql.connect('wines.db')
    conn.row_factory = sql.Row
    return conn

# link to the home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/wine_list')
def wine_list():
    conn = wines_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wine_list")

    get_wines = cursor.fetchall()
    return render_template('wine_list.html', title = 'Wine List', retrieveWines = get_wines)

@app.route('/add_wine.html', methods=['GET', 'POST'])
def add_wine():
    if request.method == 'POST':
        name = request.form['Name']
        producer = request.form['Producer']
        origin = request.form['Origin']
        vegan = request.form['Vegan']

        conn = wines_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO wine_list (Name, Producer, Origin, Vegan) VALUES (?,?,?,?)", (name, producer, origin, vegan))
        conn.commit()
        conn.close()
        return redirect(url_for('wine_list'))
    return render_template('add_wine.html', title = 'Add wine to the list')

@app.route("/update_wine/<string:wine_id>", methods=['POST', 'GET'])
def update_wine(wine_id):
    if request.method == 'POST':
        name = request.form['Name']
        producer = request.form['Producer']
        origin = request.form['Origin']
        vegan = request.form['Vegan']

        conn = wines_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE wine_list SET Name=?, Producer=?, Origin=?, Vegan=? WHERE WineID=?", (name, producer, origin, vegan, wine_id))
        conn.commit()
        return redirect(url_for("wine_list"))
    conn = wines_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wine_list WHERE WineID=?", (wine_id,))
    get_wines = cursor.fetchone()
    return render_template("update_wine.html", retrieveWines = get_wines)

@app.route("/delete_wine/<string:wine_id>", methods = ['GET'])
def delete_wine(wine_id):
    conn = wines_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wine_list WHERE WineID=?", (wine_id,))
    conn.commit()
    return redirect(url_for("wine_list"))

@app.route('/search_wines', methods=['GET', 'POST'])
def search_wines():
    if request.method == 'POST':
        search_value = request.form['search_input']
        search = "%{}%".format(search_value)

        conn = wines_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wine_list WHERE Name LIKE ? OR Producer LIKE ? OR Origin LIKE ?", (search, search, search))
        results = cursor.fetchall()
        if results == ():
            print("Nothing found")
        return render_template('search_wines.html', title = 'Search results', searchWines = results)
    else:
        return redirect ('index')









if __name__ == '__main__':
    app.run(debug=True)

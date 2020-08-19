#  TODO: finish the dummy_add_product function
import sqlite3
import flask
from product import Product
from wtforms import Form

app = flask.Flask(__name__)         # setting up API app
app.config["DEBUG"] = True          # debugging is on

try:
    conn = sqlite3.connect('products_offers.db')  # creation or connection to database named "products_offer.db"; can
    # be: "conn = sqlite3.connect(':memory:')", it will start fresh database every time this script will be run,
    # good for testing

    curs = conn.cursor()  # creating object cursor, which executes sql commands

    curs.execute("""CREATE TABLE products       
                    (
                        id int,
                        price int,
                        name text,
                        description text
                    );
                        """)  # creating a table with SQL query

    curs.execute("""INSERT INTO products VALUES             
            (1, 25, 'banana', 'fruit') 
            (2, 40, 'yogurt', 'healthy breakfast'),
            (3, 100, 'beef', 'dinner dish'),
            (4, 59, 'milk', 'breakfast drink'),
            (5, 3, 'apple', 'keeps the doctor away'),
            (6, 55, 'cheese', 'nice'),
            (7, 32, 'butter', 'perfect with bread'),
            (8, 22, 'bread', 'perfect with butter'),
            (9, 20, 'beer', 'good after hard work'),
            (10, 35, 'eggs', 'great for omelet');        
            """)  # inserting initial values to products table
except:
    DEBUG = True

conn.commit()                   # committing the changes in products_offers.db


# curs.execute('SELECT * FROM products')      # selecting all rows from products table
# print(curs.fetchall())                      # printing them all
#
# conn.commit()                   # committing the changes in products_offers.db
# conn.close()                    # closing the connection with products_offers.db


@app.route('/', methods=['GET'])
def home():
    return flask.render_template("main.html")           # path is "venv/templates/main.html"


@app.route('/all', methods=['GET'])
def return_all():
    conn_1 = sqlite3.connect('products_offers.db')
    with conn_1:
        curs_1 = conn_1.cursor()
        all = curs_1.execute('SELECT * FROM products').fetchall()
    return flask.jsonify(all)


@app.errorhandler(404)                                                  # error handler to show code of the error
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# Example of usage:
# http://127.0.0.1:5000/all/API/products/filter?name=banana&?id=1

@app.route('/all/API/products/filter', methods=['GET'])
def api_filter():
    query_parameters = flask.request.args       # request all arguments like ?id from http query

    id_p = query_parameters.get('id')           # fetching arguments from http query
    price = query_parameters.get('price')
    name = query_parameters.get('name')

    query = "SELECT * FROM products WHERE "         # forming a query for products_offers.db
    to_filter = []                                  # empty list for filtering parameters
    conn_1 = sqlite3.connect('products_offers.db')  # forming a connection for local function
    with conn_1:
        curs_1 = conn_1.cursor()
        if id_p:
            query += "id = ? AND"
            to_filter.append(id_p)
        if price:
            query += "price = ? AND"
            to_filter.append(price)
        if name:
            query += "name = ? AND"
            to_filter.append(name)

    query = query[:-4]+";"                              # cutting the query
    all = curs_1.execute(query, to_filter).fetchall()   # fetching results from products_offers.db

    return flask.jsonify(all)


# class AddProductForm(Form):             # id of text fields is ids os inputs in add_product.html (?)
#     id = TextField('input_id')
#     price = TextField('input_price')
#     name = TextField('input_name')
#     desc = TextField('input_desc')


@app.route('/all/API/add', methods=['GET', 'POST'])
def dummy_add_product():
    conn_1 = sqlite3.connect('products_offers.db')
    if flask.request.method == "POST":
        pass
    return flask.render_template("add_product.html")


def add_product(product):
    with conn:  # "with .." statement allows automatically
        # close it, when action is done
        curs.execute("""INSERT INTO products VALUES
        (?, ?, ?, ?)
        """, (product.id, product.price, product.name, product.desc))  # inserting the row with SQL query,
        # with usage of "?", actual values should be in tupple


def delete_product(type_s, value):                          # to delete the product, you should type in which product,
    if type_s == "id":                                      # you need to delete, you can delete product by id, price,
        with conn:                                          # name. "type_s" is type of the deleting(by id, name...)
            curs.execute("""DELETE FROM products WHERE       
            id = ?
            """, (value,))                                  # "value" is initial id, name or price of item, you want to
                                                            # delete
    if type_s == "price":
        with conn:
            curs.execute("""DELETE FROM products WHERE 
            price = ?
            """, (value,))
    if type_s == "name":
        with conn:
            curs.execute("""DELETE FROM products WHERE 
            name = ?
            """, (value,))

# Example of usage:
# update_product("<search by>", "<what to update>", "<new value>")


def update_product(type_s, value, type_u, new_value):
    query = """
    UPDATE products SET 
    """
    if type_s == "id":
        query += type_u
        query += " = ? WHERE id = ?"
        with conn:
            curs.execute(query, (new_value, value))
    if type_s == "price":
        query += type_u
        query += " = ? WHERE price = ?"
        with conn:
            curs.execute(query, (new_value, type_u))
    if type_s == "name":
        query += type_u
        query += " = ? WHERE name = ?"
        with conn:
            curs.execute(query, (new_value, type_u))
    if type_s == "description":
        query += type_u
        query += " = ? WHERE description = ?"
        with conn:
            curs.execute(query, (new_value, type_u))


# Example of usage:
# add_product(Product(11, 228, "ganja", "noice"))
# update_product("id", 11, "id", 12)
# delete_product("id", 12)


# curs.execute('SELECT * FROM products')      # selecting all rows from products table
# print(curs.fetchall())                      # printing them all
#
# conn.commit()                   # committing the changes in products_offers.db
# conn.close()                    # closing the connection with products_offers.db


app.run()
conn.close()                    # closing the connection with products_offers.db

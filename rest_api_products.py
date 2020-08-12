import sqlite3
import flask
from product import Product

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
conn.close()                    # closing the connection with products_offers.db

# curs.execute('SELECT * FROM products')      # selecting all rows from products table
# print(curs.fetchall())                      # printing them all
#
# conn.commit()                   # committing the changes in products_offers.db
# conn.close()                    # closing the connection with products_offers.db


@app.route('/', methods=['GET'])
def home():
    return """
    <title>Test API</title>
    <h1> This is test API for products database </h1>
    <p>this is prototype API</p>
    """


@app.route('/all', methods=['GET'])
def return_all():
    conn_1 = sqlite3.connect('products_offers.db')
    with conn_1:
        curs_1 = conn_1.cursor()
        all = curs_1.execute('SELECT * FROM products').fetchall()
    return flask.jsonify(all)

#  TODO: methods for add, delete, update; Filter the results by id, price ....


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

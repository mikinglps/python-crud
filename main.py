from sql_connection import get_sql_connection
from flask import Flask, request, make_response, jsonify
#import mysql.connector

app = Flask(__name__)

bd = get_sql_connection()

@app.route('/', methods=['GET'])
def get_all_products():
    cursor = bd.cursor()
    query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name "
            "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id")
    cursor.execute(query)

    results = cursor.fetchall()
    cursor.close()
    bd.close()
    return make_response(
        jsonify(
            mensagem='Sucesso!',
            data=results
        )
    )

@app.route('/add', methods=['POST'])
def add_new_product():
    product = request.json
    cursor = bd.cursor()
    data = (None, product['product_name'], product['uom'], product['price_per_unit'])
    query = ("INSERT INTO products VALUES (?, ?, ?, ?)")
    try:
        cursor.execute(query, data)
        bd.commit()
        return make_response(jsonify(
            mensagem='Cadastrado com sucesso!',
            produto=product
        ))
    except Exception:
        bd.rollback()
        cursor.close()
        bd.close()
        return make_response(jsonify(
            mensagem='Erro!'
        ))

@app.route('/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    cursor = bd.cursor()
    ##sqlite3 uses ? instead of %s
    query = ("DELETE FROM products WHERE product_id = %s")
    try:
        #what defines a tuple is the comma, not the parenthesis.
        cursor.execute(query, (product_id,))
        bd.commit()
        cursor.close()
        bd.close()
        return make_response(
            jsonify(
                mensagem='Sucesso ao deletar produto!' 
            )
        )
    except:
        bd.rollback()
        cursor.close()
        bd.close()
        return make_response(
            jsonify(
                mensagem='Erro'
            )
        )

@app.route('/update/<product_id>', methods=['POST'])
def update_product(product_id):
    data = request.json
    cursor = bd.cursor()
    query = ("UPDATE products SET name = %s WHERE product_id = %s")
    try:
        cursor.execute(query, (data['name'], product_id))
        bd.commit()
        cursor.close();
        bd.close()
        return make_response(
            jsonify(
                mensagem='Sucesso ao editar produto'
            )
        )
    except:
        bd.rollback()
        return make_response(
            jsonify(
                mensagem='Erro!'
            )
        )

if __name__ == '__main__':
    app.run(debug=True)
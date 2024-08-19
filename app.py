from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import db as dbase  
from product import Product
from dotenv import load_dotenv

def crear_app():

    db = dbase.dbConnection()

    app = Flask(__name__)

    @app.route('/')
    def home():
        products = db['products']
        productsReceived = products.find()
        return render_template('index.html', products = productsReceived)

    @app.route('/products', methods=['POST'])
    def addProduct():
        products = db['products']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']

        if name and price and quantity:
            product = Product(name, price, quantity)
            products.insert_one(product.toDBCollection())
            response = jsonify({
                'name' : name,
                'price' : price,
                'quantity' : quantity
            })
            return redirect(url_for('home'))
        else:
            return notFound()

    @app.route('/delete/<string:product_name>')
    def delete(product_name):
        products = db['products']
        products.delete_one({'name' : product_name})
        return redirect(url_for('home'))

    @app.route('/edit/<string:product_name>', methods=['POST'])
    def edit(product_name):
        products = db['products']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']

        if name and price and quantity:
            products.update_one({'name' : product_name}, {'$set' : {'name' : name, 'price' : price, 'quantity' : quantity}})
            response = jsonify({'message' : 'Producto ' + product_name + ' actualizado correctamente'})
            return redirect(url_for('home'))
        else:
            return notFound()

    @app.errorhandler(404)
    def notFound(error=None):
        message ={
            'message': 'No encontrado ' + request.url,
            'status': '404 Not Found'
        }
        response = jsonify(message)
        response.status_code = 404
        return response
    
    return app


if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True, port=4000)
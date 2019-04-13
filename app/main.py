from flask import Flask

from app.goods import ProductManager, Product


def start():
    app = Flask(__name__)

    product_manager = ProductManager()

    product_manager.add(Product('IPhone 7 64GB', price=39_900, amount=10))
    product_manager.add(Product('IPhone X 128GB', price=61900, amount=2))
    product_manager.add(Product('IPhone X 64GB', price=58900, amount=2))
    product_manager.add(Product('IPhone XR 128GB', price=68900, amount=3))
    product_manager.add(Product('MacBook PRO', price=99900, amount=5))
    product_manager.add(Product('Apple Watch 3', price=17900, amount=7))





import uuid

from flask import Flask, request, render_template

from app.goods import ProductManager, Product, SaleManager


def start():
    app = Flask(__name__)

    product_manager = ProductManager()

    product_manager.add(Product('IPhone 7 64GB', price=39_900, amount=10))
    product_manager.add(Product('IPhone X 128GB', price=61900, amount=2))
    product_manager.add(Product('IPhone X 64GB', price=58900, amount=2))
    product_manager.add(Product('IPhone XR 128GB', price=68900, amount=3))
    product_manager.add(Product('MacBook PRO', price=99900, amount=5))
    product_manager.add(Product('Apple Watch 3', price=17900, amount=7))

    sale_manager = SaleManager()
    product_saved = False
    sale_alert = None

    @app.route('/')
    def index():
        sort_field = request.args.get('sort_order')
        if sort_field not in ['name', 'price', 'amount']:
            sort_field = 'name'

        sort_order = request.args.get('sort_order')
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        product_manager.sort_items(sort_field, sort_order)

        search = request.args.get('search')
        if search:
            products = product_manager.search_by_name(search)
        else:
            products = product_manager.items
            search = ''

        empty_id = uuid.UUID(int=0)

        return render_template('index.html', products=products, empty_id=empty_id, search=search,
                               sort_order=sort_order, sort_field=sort_field)



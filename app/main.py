import uuid
import csv
import io
import os
import waitress

from flask import Flask, request, render_template, url_for, make_response
from werkzeug.utils import redirect

from app.goods import ProductManager, Product, SaleManager, EmptyProduct, Sale


def start():
    app = Flask(__name__)

    product_manager = ProductManager()

    product_manager.add(Product('IPhone 7 64GB', price=39900, amount=10))
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
            items = product_manager.search_by_name(search)
        else:
            items = product_manager.items
            search = ''

        empty_id = uuid.UUID(int=0)

        return render_template('index.html', items=items, empty_id=empty_id, search=search,
                               sort_field=sort_field,
                               sort_order=sort_order)

    @app.route('/products/<item_id>/edit')
    def product_edit(item_id):
        nonlocal product_saved

        empty_id = str(uuid.UUID(int=0))
        if item_id == empty_id:
            item = EmptyProduct()
        else:
            item = product_manager.search_by_id(item_id)

        is_saved = product_saved
        product_saved = False
        return render_template('goods-edit.html', item=item, is_saved=is_saved)

    @app.route('/products/<item_id>/save', methods=['POST'])
    def product_save(item_id):
        nonlocal product_saved

        name = request.form['name']
        price = request.form['price']
        amount = request.form['amount']

        empty_id = str(uuid.UUID(int=0))
        if item_id == empty_id:
            item = Product(name, price=price, amount=amount)
            product_manager.add(item)
            item_id = item.id
        else:
            product_manager.update(item_id, name=name, price=price, amount=amount)

        product_saved = True
        return redirect(url_for('goods_edit', item_id=item_id))

    @app.route('/products/<item_id>/remove')
    def product_remove(item_id):
        product_manager.remove_by_id(item_id)
        return redirect(url_for('index'))

    @app.route('/product/<item_id>/sale')
    def product_sale(item_id):
        nonlocal sale_alert
        alert = sale_alert
        sale_alert = None

        item = product_manager.search_by_id(item_id)
        return render_template('goods-sale.html', item=item, alert=alert)

    @app.route('/sales')
    def sales():
        sales = sale_manager.items
        return render_template('sales.html', sales=sales)

    @app.route('/sales/add', methods=['POST'])
    def sale_add():
        nonlocal sale_alert

        item_id = request.form['product_id']
        amount = int(request.form['amount'])

        item = product_manager.search_by_id(item_id)

        if amount == 0:
            sale_alert = {'class': 'danger', 'msg': 'Amount must be more than 0'}
            return redirect(url_for('goods_sale', item_id=item_id))
        if amount > item.amount:
            sale_alert = {'class': 'danger', 'msg': 'Not enough goods in stock'}
            return redirect(url_for('goods_sale', item_id=item.id))

        item.amount -= amount

        sale = Sale(item, amount)
        sale_manager.add(sale)
        sale_alert = {'class': 'success', 'msg': 'Sale complete'}
        return redirect(url_for('goods_sale', item_id=item.id))

    @app.route('/products/import', methods=['POST'])
    def product_import():
        nonlocal product_manager
        if 'import-file' not in request.files:
            redirect(url_for('index'))

        import_file = request.files['import-file']
        content = io.StringIO(import_file.read().decode('utf8'))
        reader = csv.reader(content, delimiter=';')
        product_manager = ProductManager()
        for line in reader:
            product_manager.add(Product(line[0], price=line[1], amount=line[2]))
            return redirect(url_for('index'))

    @app.route('/products/export')
    def product_export():
        content = io.StringIO()
        writer = csv.writer(content, delimiter=';')
        items = product_manager.items
        for item in items:
            writer.writerow([item.name, item.price, item.amount])

        response = make_response(content.getvalue())
        response.headers['content-type'] = 'application/octet-stream'
        response.headers['content-disposition'] = 'inline; filename=exported.csv'
        return response

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9876, debug=True)


if __name__ == '__main__':
    start()




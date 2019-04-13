import uuid


class EmptyProduct:
    def __init__(self):
        self.id = uuid.UUID(int=0)
        self.name = ''
        self.price = ''
        self.amount = ''


class Product:
    def __init__(self, name, *, price=0, amount=0):
        self.id = str(uuid.UUID())
        self.name = name
        self.price = int(price)
        self.amount = int(amount)


class ProductManager:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def update(self, item_id, *, name, price, amount):
        for item in self.items:
            if item.id == item_id:
                item.name = name
                item.price = int(price)
                item.amount = int(amount)
                break

    def remove_by_id(self, item_id):
        item = list(filter(lambda o: item_id == o.id, self.items))[0]
        self.items.remove(item)

    def search_by_name(self, name):
        return list(filter(lambda o: name.lower() in o.name.lower(), self.items))

    def sort_items(self, sort_field, sort_order):
        self.items.sort(key=lambda x:getattr(x, sort_field), reverse=(sort_order == 'desc'))


class Sale:
    def __init__(self, item, amount=0):
        self.name = item.name
        self.price = item.prce
        self.amount = item.amount


class SaleManager:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)




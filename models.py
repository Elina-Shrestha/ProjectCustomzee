from datetime import datetime

# Base User class
class User:
    def __init__(self, userId, name, email, password):
        self.userId = userId
        self.name = name
        self.email = email
        self.password = password

    def login(self):
        print(f"{self.name} logged in.")

    def logout(self):
        print(f"{self.name} logged out.")


# Customer inherits from User
class Customer(User):
    def __init__(self, userId, name, email, password):
        super().__init__(userId, name, email, password)
        self.cart = Cart(self)
        self.orders = []

    def browseProducts(self, products):
        print("Available products:")
        for p in products:
            print(f"{p.productId}: {p.name} - ${p.price}")

    def placeOrder(self):
        order = Order(len(self.orders)+1, self)
        for item in self.cart.items:
            order.addProduct(item)
        self.orders.append(order)
        self.cart.clear()
        print(f"Order {order.orderId} placed!")
        return order


# Admin inherits from User
class Admin(User):
    def addProduct(self, product_list, name, description, price, category):
        productId = len(product_list)+1
        product = Product(productId, name, description, price, category)
        product_list.append(product)
        print(f"Product '{name}' added.")
        return product

    def removeProduct(self, product_list, productId):
        product_list[:] = [p for p in product_list if p.productId != productId]
        print(f"Product {productId} removed.")

    def updateProduct(self, product_list, productId, **kwargs):
        for p in product_list:
            if p.productId == productId:
                for key, value in kwargs.items():
                    setattr(p, key, value)
                print(f"Product {productId} updated.")
                return
        print(f"Product {productId} not found.")


# Product class
class Product:
    def __init__(self, productId, name, description, price, category):
        self.productId = productId
        self.name = name
        self.description = description
        self.price = price
        self.category = category


# Cart class
class Cart:
    def __init__(self, customer):
        self.cartId = customer.userId
        self.customer = customer
        self.items = []

    def addItem(self, product):
        self.items.append(product)
        print(f"{product.name} added to cart.")

    def removeItem(self, productId):
        self.items = [p for p in self.items if p.productId != productId]
        print(f"Product {productId} removed from cart.")

    def clear(self):
        self.items = []

    def checkout(self):
        order = Order(len(self.customer.orders)+1, self.customer)
        for item in self.items:
            order.addProduct(item)
        self.customer.orders.append(order)
        self.clear()
        print(f"Checkout complete. Order {order.orderId} created.")
        return order


# Order class
class Order:
    def __init__(self, orderId, customer):
        self.orderId = orderId
        self.customer = customer
        self.products = []
        self.date = datetime.now()
        self.status = "Pending"

    def addProduct(self, product):
        self.products.append(product)

    def calculateTotal(self):
        return sum(p.price for p in self.products)

import mysql.connector


class Vendor:
    def __init__(self, id, username, password, vendor_email, vendor_phone, address):
        self.id = id
        self.username = username
        self.password = password
        self.vendor_email = vendor_email
        self.vendor_phone = vendor_phone
        self.address = address


class Buyer:
    def __init__(self, id, username, password, buyer_email, buyer_phone, address):
        self.id = id
        self.username = username
        self.password = password
        self.buyer_email = buyer_email
        self.buyer_phone = buyer_phone
        self.address = address


class Product:
    def __init__(self, id, category_id, vendor_id, name, price, desc, product_pic, promotional_status,
                 promotional_start, promotional_end, promotional_price, like_amount, dislike_amount, modify_time):
        self.id = id
        self.category_id = category_id
        self.vendor_id = vendor_id
        self.name = name
        self.price = price
        self.desc = desc
        self.product_pic = product_pic
        self.promotional_status = promotional_status
        self.promotional_start = promotional_start
        self.promotional_end = promotional_end
        self.promotional_price = promotional_price
        self.like_amount = like_amount
        self.dislike_amount = dislike_amount
        self.modify_time = modify_time


class Like:
    def __init__(self, id, product_id, buyer_id, status):
        self.id = id
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.status = status


class ProductComment:
    def __init__(self, id, product_id, buyer_id, comment_status, content, create_time):
        self.id = id
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.comment_status = comment_status
        self.content = content
        self.create_time = create_time


class Category:
    def __init__(self, id, category_name):
        self.id = id
        self.category_name = category_name


class Cart:
    def __init__(self, id, buyer_id, product_id, product_amount):
        self.id = id
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.product_amount = product_amount


class Order:
    def __init__(self, id, vendor_id, buyer_id, product_id, product_amount, order_money, order_status, creat_time,
                 arrival_time):
        self.id = id
        self.vendor_id = vendor_id
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.product_amount = product_amount
        self.order_money = order_money
        self.order_status = order_status
        self.creat_time = creat_time
        self.arrival_time = arrival_time

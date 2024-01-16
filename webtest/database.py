import mysql.connector
from structures import Vendor, Buyer, Product, Like, ProductComment, Category, Cart, Order

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def database_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="lixudong",
        database="wad"
    )


# # Login, registration function
def add_buyer(buyer):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO buyer (username, password, buyer_email, buyer_phone, address) VALUES (%s, %s, %s, %s, %s)",
        (buyer.username, buyer.password, buyer.buyer_email, buyer.buyer_phone, buyer.address))
    conn.commit()
    cursor.close()
    conn.close()


def add_vendor(vendor):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vendor (username, password, vendor_email, vendor_phone, address) VALUES (%s, %s, %s, %s, %s)",
        (vendor.username, vendor.password, vendor.vendor_email, vendor.vendor_phone, vendor.address))
    conn.commit()
    cursor.close()
    conn.close()


def get_buyer(username):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM buyer WHERE username = %s", (username,))
    check_password = cursor.fetchone()
    cursor.close()
    conn.close()
    if check_password:
        return check_password[0]
    else:
        return None


def get_buyer_id(username):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM buyer WHERE username = %s", (username,))
    buyer_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return buyer_id[0]


def get_vendor(username):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM vendor WHERE username = %s", (username,))
    check_password = cursor.fetchone()
    cursor.close()
    conn.close()
    if check_password:
        return check_password[0]
    else:
        return None


def get_vendor_id(username):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM vendor WHERE username = %s", (username,))
    vendor_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return vendor_id[0]


# index
def big_sale_product():
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_pic, name, price, promotional_price FROM product "
                   "WHERE promotional_status = %s", (1,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


def search_results(content):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_pic, name, price, promotional_price FROM product "
                   "WHERE name LIKE %s", ('%' + content + '%',))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


# show product detail
def show_product(product_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return product


def show_product_category(category_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
    category_name = cursor.fetchone()
    cursor.close()
    conn.close()
    return category_name


def products_in_category(category_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE category_id = %s", (category_id,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


def specified_products(category_id, content):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE category_id = %s and name Like %s", (category_id, '%' + content + '%'))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


def show_product_vendor(vendor_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM vendor WHERE id = %s", (vendor_id,))
    vendor_name = cursor.fetchone()
    cursor.close()
    conn.close()
    return vendor_name


# like function
def point_favor(like_amount, dislike_amount, product_id):
    conn = database_conn()
    cursor = conn.cursor()
    print(like_amount, dislike_amount, product_id)
    cursor.execute("UPDATE product SET like_amount = %s, dislike_amount = %s WHERE id = %s",
                   (like_amount, dislike_amount, product_id))
    conn.commit()
    cursor.close()
    conn.close()


def check_like(product_id, buyer_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM `like` WHERE product_id = %s and buyer_id = %s", (product_id, buyer_id))
    like_status = cursor.fetchone()
    cursor.close()
    conn.close()
    if like_status:
        return like_status[0]
    else:
        return None


def upload_like(like):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `like` (product_id, buyer_id, status)"
                   "values (%s, %s, %s)",
                   (like.product_id, like.buyer_id, like.status))
    conn.commit()
    cursor.close()
    conn.close()


def update_like(status, product_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE `like` SET status = %s WHERE product_id = %s", (status, product_id))
    conn.commit()
    cursor.close()
    conn.close()


# comment function
def show_comments(product_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT p.content, p.create_time, b.username FROM product_comment p, buyer b  "
                   "WHERE product_id = %s and p.buyer_id = b.id", (product_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments


def submit_comment(comment):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product_comment (product_id, buyer_id, comment_status, content, create_time) "
                   "values (%s, %s, %s, %s, %s)",
                   (comment.product_id, comment.buyer_id, comment.comment_status, comment.content, comment.create_time))
    conn.commit()
    cursor.close()
    conn.close()


# Center
def get_cart(buyer_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart WHERE buyer_id = %s", (buyer_id,))
    cart_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return cart_list


def buyer_information(buyer_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT username, address FROM buyer WHERE id = %s", (buyer_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders[0]


def new_cart(cart):
    conn = database_conn()
    cursor = conn.cursor()
    print(cart.product_amount)
    cursor.execute("INSERT INTO cart (buyer_id, product_id, product_amount) VALUES (%s, %s, %s)",
                   (cart.buyer_id, cart.product_id, cart.product_amount))
    conn.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    cart_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return cart_id


def cart_amount_update(cart_id, amount):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE cart SET product_amount = %s WHERE id = %s",
                   (amount, cart_id))
    conn.commit()
    cursor.close()
    conn.close()


def remove_cart(cart_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE id = %s", (cart_id,))
    conn.commit()
    cursor.close()
    conn.close()


def buy_product_cart(order):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `order`(vendor_id, buyer_id, product_id, product_amount, order_money, order_status,"
                   "create_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (order.vendor_id, order.buyer_id, order.product_id, order.product_amount, order.order_money,
                    order.order_status, order.creat_time))
    conn.commit()
    cursor.close()
    conn.close()


def get_cart_info(cart_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart WHERE id = %s", (cart_id,))
    cart_list = cursor.fetchone()
    cursor.close()
    conn.close()
    return cart_list


def show_all_orders_buyer(buyer_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `order` WHERE buyer_id = %s order BY "
                   "CASE order_status WHEN 1 THEN 1 WHEN 0 THEN 2 ELSE 3 END", (buyer_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders


# Management --- product
def show_all_products(vendor_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE vendor_id = %s", (vendor_id,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


def show_all_category():
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories


def new_product(product):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO product (category_id, vendor_id, name, price, `desc`, product_pic, promotional_status, "
        "promotional_start, promotional_end, promotional_price, modify_time)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (product.category_id, product.vendor_id, product.name, product.price, product.desc, product.product_pic,
         product.promotional_status,
         product.promotional_start, product.promotional_start, product.promotional_price, product.modify_time))
    print(product.modify_time)
    conn.commit()
    cursor.close()
    conn.close()


def update_product(product, product_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE product SET category_id=%s, vendor_id=%s, `name`=%s, price=%s, `desc`=%s, product_pic=%s, "
        "promotional_status=%s, promotional_start=%s, promotional_end=%s, promotional_price=%s, like_amount=%s, "
        "dislike_amount=%s, modify_time=%s WHERE id = %s",
        (product.category_id, product.vendor_id, product.name, product.price, product.desc, product.product_pic,
         product.promotional_status, product.promotional_start, product.promotional_start,
         product.promotional_price, product.like_amount, product.dislike_amount,
         product.modify_time, product_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_product(product_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()


# management ------ order
def show_all_orders_vendor(vendor_id):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `order` WHERE vendor_id = %s ORDER BY order_status asc ", (vendor_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders


def update_order(order_id, status, time):
    conn = database_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE `order` SET order_status = %s, arrival_time = %s WHERE id = %s", (status, time, order_id))
    conn.commit()
    cursor.close()
    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

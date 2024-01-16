from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, session
from structures import Vendor, Buyer, Product, Like, ProductComment, Category, Cart, Order
from database import add_vendor, add_buyer, get_buyer, get_vendor, big_sale_product, get_buyer_id, get_vendor_id, \
    search_results, show_product, show_product_category, show_product_vendor, show_comments, submit_comment, \
    show_all_products, show_all_orders_vendor, allowed_file, new_product, update_product, show_all_category, \
    delete_product, point_favor, check_like, upload_like, update_like, update_order, show_all_orders_buyer, \
    buyer_information, get_cart, new_cart, remove_cart, get_cart_info, buy_product_cart, products_in_category, \
    specified_products, cart_amount_update


def secure_filename(filename):
    _, ext = os.path.splitext(filename)
    new_filename = ''.join(c if c.isalnum() or c in ['-', '_'] else '_' for c in filename)
    return new_filename + ext


app = Flask(__name__)
app.secret_key = 'QQ1525'

UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    if 'type' in session:
        return redirect(url_for('product_management'))
    products = big_sale_product()
    categories = show_all_category()
    all_products = []
    # print(products_in_category(3))
    # all_products.append(products_in_category(1))
    # all_products.append(products_in_category(3))
    # print(all_products)
    # print(all_products[1] == [])
    for c in categories:
        c_id = c[0]
        all_products.append(products_in_category(c_id))
        # print(all_products[0][0])

    return render_template('index.html', products=products, username=session.get('username'), id=session.get('id'),
                           categories=categories, all_products=all_products)


# Login, registration function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pwd')
        user_type = request.form.get('user_type')
        if user_type == 'buyer':
            check_password = get_buyer(username)
            if password == check_password:
                session['username'] = username
                user_id = get_buyer_id(username)
                session['id'] = user_id
                return redirect(url_for('index'))
        elif user_type == 'vendor':
            check_password = get_vendor(username)
            if password == check_password:
                session['username'] = username
                vendor_id = get_vendor_id(username)
                session['id'] = vendor_id
                session['type'] = 'vendor'
                return redirect(url_for('product_management'))
        error_message = 'Incorrect username or password'
        return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register_buyer', methods=['GET', 'POST'])
def register_buyer():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd_db = get_buyer(username)
        if pwd_db is None:
            password = request.form.get('pwd')
            buyer_email = request.form.get('email')
            buyer_phone = request.form.get('phone')
            address = request.form.get('address')
            buyer = Buyer(None, username, password, buyer_email, buyer_phone, address)
            add_buyer(buyer)
            return redirect(url_for('login'))
        else:
            error_message = 'The username already exit'
            return render_template('register_buyer.html', error_message=error_message)
    return render_template('register_buyer.html')


@app.route('/register_vendor', methods=['GET', 'POST'])
def register_vendor():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd_db = get_vendor(username)
        if pwd_db is None:
            password = request.form.get('pwd')
            vendor_email = request.form.get('email')
            vendor_phone = request.form.get('phone')
            address = request.form.get('address')
            vendor = Vendor(None, username, password, vendor_email, vendor_phone, address)
            add_vendor(vendor)
            return redirect(url_for('login'))
        else:
            error_message = 'The username already exit'
            return render_template('register_buyer.html', error_message=error_message)
    return render_template('register_vendor.html')


# buyer function
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        categories = show_all_category()
        content = request.form.get('search', '')
        products = search_results(content)
        return render_template('search.html', products=products, username=session.get('username'),
                               categories=categories)
    else:
        categories = show_all_category()
        content = ''
        products = search_results(content)
        return render_template('search.html', products=products, username=session.get('username'),
                               categories=categories)


@app.route('/category/<category_id>', methods=['GET', 'POST'])
def category(category_id):
    if request.method == 'GET':
        products = products_in_category(category_id)
        categories = show_all_category()
        # print(category_id)
        # print(products)
        return render_template('category.html', products=products, username=session.get('username'),
                               categories=categories, category_id=int(category_id))

    elif request.method == 'POST':
        category_id = category_id
        content = request.form.get('search', '')
        categories = show_all_category()
        # print(category_id)
        # print(category_id)
        products = specified_products(category_id, content)
        # print(products)
        return render_template('category.html', products=products, username=session.get('username'),
                               categories=categories, category_id=int(category_id))


@app.route('/product/<product_id>')
def product_info(product_id):
    product_detail = show_product(product_id)
    categories = show_product_category(product_detail[1])
    # print(categories)
    vendor_name = show_product_vendor(product_detail[2])
    comments = show_comments(product_id)
    # print(product_detail)
    # print(categories)
    # print(comments)
    if 'id' in session:
        buyer_id = session['id']
        status = check_like(product_id, buyer_id)
        return render_template('product.html', product_detail=product_detail, categories=categories,
                               vendor_name=vendor_name, comments=comments, username=session.get('username'),
                               status=status)
    return render_template('product.html', product_detail=product_detail, categories=categories,
                           vendor_name=vendor_name, comments=comments, username=session.get('username'))


@app.route('/product/<product_id>/like')
def like_function(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    buyer_id = session['id']
    product = show_product(product_id)
    status = check_like(product_id, buyer_id)
    # print(status)
    like_amount = product[11]
    dislike_amount = product[12]
    if status is not None:
        if status == 0:
            status = 2
            update_like(status, product_id)
            like_amount += 1
            point_favor(like_amount, dislike_amount, product_id)
        elif status == 1:
            status = 2
            update_like(status, product_id)
            like_amount += 1
            dislike_amount -= 1
            point_favor(like_amount, dislike_amount, product_id)
        elif status == 2:
            status = 0
            update_like(status, product_id)
            like_amount -= 1
            point_favor(like_amount, dislike_amount, product_id)
        return redirect(f'/product/{product_id}')

    else:
        status = 2
        like = Like(None, product_id, buyer_id, status)
        like_amount += 1
        # print(dislike_amount)
        point_favor(like_amount, dislike_amount, product_id)
        upload_like(like)
        return redirect(f'/product/{product_id}')


@app.route('/product/<product_id>/dislike')
def dislike_function(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    buyer_id = session['id']
    status = check_like(product_id, buyer_id)
    # print(status)
    product = show_product(product_id)
    like_amount = product[11]
    dislike_amount = product[12]
    if status is not None:
        if status == 0:
            status = 1
            update_like(status, product_id)
            dislike_amount += 1
            point_favor(like_amount, dislike_amount, product_id)
        elif status == 1:
            status = 0
            update_like(status, product_id)
            dislike_amount -= 1
            point_favor(like_amount, dislike_amount, product_id)
        elif status == 2:
            status = 1
            update_like(status, product_id)
            like_amount -= 1
            dislike_amount += 1
            point_favor(like_amount, dislike_amount, product_id)
        return redirect(f'/product/{product_id}')

    else:
        status = 1
        like = Like(None, product_id, buyer_id, status)
        dislike_amount += 1
        point_favor(like_amount, dislike_amount, product_id)
        upload_like(like)
        return redirect(f'/product/{product_id}')


@app.route('/product/<product_id>/comment', methods=['POST'])
def send_comment(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    content = request.form.get('content')
    buyer_id = session['id']
    create_time = datetime.now()
    comment = ProductComment(None, product_id, buyer_id, 1, content, create_time)
    submit_comment(comment)
    return redirect(f'/product/{product_id}')


@app.route('/center')
def center():
    if 'username' not in session:
        return redirect(url_for('login'))
    buyer_id = session['id']
    cart_list = get_cart(buyer_id)
    cart_products = []
    buyer_info = buyer_information(buyer_id)
    # print()
    for c in cart_list:
        product = show_product(c[2])
        cart_products.append(product)
    orders = show_all_orders_buyer(buyer_id)
    order_products = []
    for o in orders:
        product = show_product(o[3])
        print(show_product(1))
        order_products.append(product)
    return render_template('center.html', username=session.get('username'), orders=orders, cart_products=cart_products,
                           cart_list=cart_list, order_products=order_products, buyer_info=buyer_info)


@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    buyer_id = session['id']
    cart_list = get_cart(buyer_id)
    products = []
    buyer_info = buyer_information(buyer_id)
    # print()
    for c in cart_list:
        product = show_product(c[2])
        products.append(product)
    return render_template('cart.html', username=session.get('username'), products=products, cart_list=cart_list,
                           buyer_info=buyer_info)


@app.route('/cart/<cart_id>/up')
def up_amount(cart_id):
    cart_info = get_cart_info(cart_id)
    amount = cart_info[3] + 1
    cart_amount_update(cart_id, amount)
    return redirect(url_for("cart"))


@app.route('/cart/<cart_id>/down')
def down_amount(cart_id):
    cart_info = get_cart_info(cart_id)
    amount = cart_info[3] - 1
    if amount > 0:
        cart_amount_update(cart_id, amount)
    return redirect(url_for("cart"))


@app.route('/add_cart/<product_id>')
def add_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    buyer_id = session['id']
    amount = request.args.get('amount')
    print(amount)
    cart_info = Cart(None, buyer_id, product_id, amount)
    new_cart(cart_info)
    return redirect(f'/product/{product_id}')


@app.route('/delete_cart/<cart_id>')
def delete_cart(cart_id):
    remove_cart(cart_id)
    return redirect(url_for('cart'))


@app.route('/buy/<cart_id>')
def buy(cart_id):
    buyer_id = session['id']
    cart_info = get_cart_info(cart_id)
    # print(cart_id)
    product_id = cart_info[2]
    product_amount = cart_info[3]
    # print(product_amount)
    product = show_product(product_id)
    vendor_id = product[2]
    if product[7] == 1:
        order_money = product[10] * product_amount
    else:
        order_money = product[4] * product_amount
    order_status = 0
    creat_time = datetime.now()
    order = Order(None, vendor_id, buyer_id, product_id, product_amount, order_money, order_status, creat_time, None)
    buy_product_cart(order)
    remove_cart(cart_id)
    return redirect(url_for('cart'))


@app.route('/buy_cart/<cart_id>')
def buy_cart(cart_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    cart_info = get_cart_info(cart_id)
    product_id = cart_info[2]

    product = show_product(product_id)
    return render_template('buy_product.html', product=product, cart=cart_info)


@app.route('/buy_direct/<product_id>')
def buy_direct(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    buyer_id = session['id']
    # print(product_amount)
    product = show_product(product_id)
    product_amount = request.args.get('amount')
    cart_info_tmp = Cart(None, buyer_id, product_id, product_amount)
    cart_id = new_cart(cart_info_tmp)
    cart_info = get_cart_info(cart_id)
    return render_template('buy_product.html', product=product, cart=cart_info)
    # vendor_id = product[2]
    # if product[7] == 1:
    #     order_money = product[10] * int(product_amount)
    # else:
    #     order_money = product[4] * int(product_amount)
    # order_status = 0
    # creat_time = datetime.now()
    # order = Order(None, vendor_id, buyer_id, product_id, product_amount, order_money, order_status, creat_time, None)
    # buy_product_cart(order)
    # return redirect(url_for('order_list'))


@app.route('/order')
def order_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    buyer_id = session['id']
    orders = show_all_orders_buyer(buyer_id)
    buy_info = buyer_information(buyer_id)
    products = []
    for o in orders:
        product = show_product(o[3])
        print(show_product(1))
        products.append(product)
    return render_template('order.html', username=session.get('username'), orders=orders,
                           products=products, buy_info=buy_info)


@app.route('/order/<order_id>')
def confirm_product(order_id):
    time = datetime.now()
    update_order(order_id, 2, time)
    return redirect(url_for('order_list'))


# vendor function
@app.route('/vendor_product')
def product_management():
    vendor_id = session['id']
    products = show_all_products(vendor_id)
    categories = []
    for p in products:
        category_name = show_product_category(p[1])
        categories.append(category_name)
    # print(category[0])
    return render_template('product_vendor.html', products=products, username=session.get('username'),
                           id=session.get('id'), category=categories)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'GET':
        categories = show_all_category()
        return render_template('add_product.html', categories=categories)
    elif request.method == 'POST':
        category_id = request.form.get('category_id')
        vendor_id = session['id']
        name = request.form.get('name')
        price = request.form.get('price')
        desc = request.form.get('desc')
        image = request.files.get('product_pic')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.static_folder, 'upload', filename))
            product_pic = os.path.join('static', 'upload', filename)
        else:
            product_pic = ''

        promotional_status = request.form.get('promotional_status', 0)
        promotional_start = request.form.get('promotional_start')
        if promotional_start == '':
            promotional_start = None
        promotional_end = request.form.get('promotional_end')
        if promotional_end == '':
            promotional_end = None
        promotional_price = request.form.get('promotional_price')
        if promotional_price == '':
            promotional_price = None
        if not name or not price or not desc or not image:
            return redirect(url_for('add_product'))
        modify_time = datetime.now()
        product = Product(None, category_id, vendor_id, name, price, desc, product_pic, promotional_status,
                          promotional_start, promotional_end, promotional_price, 0, 0, modify_time)
        print(product)
        new_product(product)
        return redirect(url_for('product_management'))


@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit(product_id):
    if request.method == 'GET':
        product = show_product(product_id)
        # print(product)
        categories = show_all_category()
        return render_template('edit.html', categories=categories, product=product)

    elif request.method == 'POST':
        product = show_product(product_id)
        category_id = request.form.get('category_id')
        vendor_id = session['id']
        name = request.form.get('name')
        price = request.form.get('price')
        desc = request.form.get('desc')
        image = request.files.get('product_pic')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.static_folder, 'upload', filename))
            product_pic = os.path.join('static', 'upload', filename)
        else:
            product_pic = product[6]

        promotional_status = request.form.get('promotional_status')

        promotional_start = request.form.get('promotional_start')
        if promotional_start == '':
            promotional_start = None

        promotional_end = request.form.get('promotional_end')
        if promotional_end == '':
            promotional_end = None

        promotional_price = request.form.get('promotional_price')
        if promotional_price == '':
            promotional_price = None

        like_amount = product[11]
        dislike_amount = product[12]
        modify_time = datetime.now()
        if not name or not price or not desc:
            return redirect(url_for('add_product'))
        product_insert = Product(None, category_id, vendor_id, name, price, desc, product_pic, promotional_status,
                                 promotional_start, promotional_end, promotional_price, like_amount, dislike_amount,
                                 modify_time)

        update_product(product_insert, product_id)
        return redirect(url_for('product_management'))


@app.route('/delete/<product_id>')
def delete(product_id):
    delete_product(product_id)
    return redirect(url_for('product_management'))


@app.route('/vendor_order')
def order_management():
    vendor_id = session['id']
    orders = show_all_orders_vendor(vendor_id)
    products = []
    buyers = []
    for order in orders:
        product = show_product(order[3])
        products.append(product)
        buyer_info = buyer_information(order[2])
        buyers.append(buyer_info)
    return render_template('order_vendor.html', orders=orders, products=products, buyers=buyers,
                           username=session.get('username'), id=session.get('id'))


@app.route('/vendor_order/<order_id>')
def supply(order_id):
    update_order(order_id, 1, None)
    print(order_id)
    return redirect(url_for('order_management'))


if __name__ == '__main__':
    app.run()

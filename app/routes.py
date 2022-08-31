import os

from app import app

from app import db

from flask import render_template, redirect, request, url_for, flash, session
from utils import send_reset_email

from forms import *

from models import *

from flask_login import LoginManager, current_user, login_required, login_user, logout_user




@app.route('/', methods=['GET', 'POST'])
def index():
    brands = Brand.query.all()
    return render_template('index.html', brands=brands)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Вы вышли из учетной записи!', category='success')
    return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    brands = Brand.query.all()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        
        login_user(user) #логинит пользователя автомотически
        return redirect(url_for('index'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
    
    
    return render_template('register.html', form=form, brands=brands)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    
    form = LoginForm()
    brands = Brand.query.all()
    
    if form.validate_on_submit():
        if '@' in form.usernameoremail.data:
            user = User.query.filter_by(email=form.usernameoremail.data).first() 
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            user = User.query.filter_by(username=form.usernameoremail.data).first()
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('profile', username=user.username))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
        
    return render_template('login.html', form=form, brands=brands) #страница login и передаем все формы


@app.route('/profile/')
def profile_():
    return redirect(url_for('login'))


@app.route('/profile/<username>/', methods=['GET', 'POST'])
@login_required
def profile(username):
    form = Profileform()
    brands = Brand.query.all()
    user = User.query.filter_by(username=username).first()
    orders = Orders.query.filter_by(email=user.email)
    
    
    if current_user.id != user.id:
        flash('Это не ваш профиль!', category='error')
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        user.username, user.email, user.phone, user.city = form.username.data, form.email.data, form.phone.data, form.city.data
        db.session.commit()
        flash('Данные успешно изменены.', category="success")
        return redirect(url_for('profile', username = user.username))
    
    return render_template('profile.html', user=user, form=form, brands=brands, orders=orders)


@app.route('/user/reset_password/', methods=['GET', 'POST']) #страница для отправки письма на почту
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = RequestResetForm() #форма ввода email
    brands = Brand.query.all()
    
    if form.validate_on_submit(): #проверка существует ли такой email
        user = User.query.filter_by(email=form.email.data).first() #ищет юзера с такой почтой.
        send_reset_email(user) #вызывает функцию на этого user (utils.py)
        flash('На email отправлена инструкция', category='email_reset')
        return redirect(url_for('login'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
    
    return render_template('reset_request.html', form=form, brands=brands)


@app.route('/user/reset_password/<token>/', methods=['GET', 'POST'])   
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    brands = Brand.query.all()
    user = User.verify_reset_token(token) #узнает какому пользователю пренадлежит токен!
    if user is None: #если токена нет или просрочен то ошибка!
        flash('Просроченный токен', category='danger')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm() #фома для смены пароля
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data) #смена пароля
        db.session.commit()   
        flash('Ваш пароль был обновлен!', category='success')
        return redirect(url_for('login'))
    
    return render_template('reset_token.html', form=form, brands=brands)  

@app.route('/admin/')
@login_required
def admin():
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    brands = Brand.query.all()
    return render_template('admin.html', brands=brands)


@app.route('/admin/addbrand/', methods=['GET', 'POST'])
@login_required
def addbrand():
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    form = AddBrandForm()
    brands = Brand.query.all()
    
    if form.validate_on_submit():
        brand = Brand(name=form.name.data)
        db.session.add(brand)
        db.session.commit()
        flash(f'Вы добавили бренд {form.name.data}', category='success')
        return redirect(url_for('admin'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
   
    return render_template('addbrand.html', form=form, brands=brands) 


@app.route('/admin/deletebrand/', methods=['GET', 'POST'])
@login_required
def deletebrand():
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    form = DeleteBrandForm()
    brands = Brand.query.all()
    
    if form.validate_on_submit():
        brand = Brand.query.filter_by(name=form.name.data).first()
        db.session.delete(brand)
        db.session.commit()
        flash(f'Вы удалили бренд {form.name.data}', category='success')
        return redirect(url_for('admin'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
    
    return render_template('deletebrand.html', form=form, brands=brands) 


@app.route('/admin/deletecategory/', methods=['GET', 'POST'])
@login_required
def deletecategory():
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    form = DeleteCategoryForm()
    brands = Brand.query.all()
    
    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.name.data).first()
        db.session.delete(category)
        db.session.commit()
        flash(f'Вы удалили категорию {form.name.data}', category='success')
        return redirect(url_for('admin'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
    
    return render_template('deletecategory.html', form=form, brands=brands) 



@app.route('/admin/addcategory/', methods=['GET', 'POST'])
@login_required
def addcategory():
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    form = AddCategoryForm()
    brands = Brand.query.all()
    
    if form.validate_on_submit():
        brand = request.form.get('brand')
        category = Category(name=form.name.data, brand_id=brand)
        db.session.add(category)
        db.session.commit()
        flash(f'Вы добавили категорию {form.name.data}', category='success')
        return redirect(url_for('admin'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
   
   
    return render_template('addcategory.html', form=form, brands=brands) 
    


@app.route('/admin/addproduct/',  methods=['GET', 'POST'])
@login_required
def addproduct():
    
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    form = AddProductsForm()
    brands = Brand.query.all()
    categories = Category.query.all()
    
    if form.validate_on_submit():
        brand = request.form.get('brand')
        category = request.form.get('category')
        image = request.files['image']
    
        if category == 'None':
            product = Products(name=form.name.data, price=form.price.data, description=form.description.data, size=form.size.data, brand_id=brand)
        else:
            product = Products(name=form.name.data, price=form.price.data, description=form.description.data, size=form.size.data, brand_id=brand, category_id=category)
        db.session.add(product)
        db.session.commit()
        
        image.filename = f'{product.link}.jpg'
        image.save(os.path.join('static/img/products', image.filename))
        flash(f'Вы добавили продукт {form.name.data}', category='success')
        return redirect(url_for('admin'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
    
    
    return render_template('addproduct.html', form=form, brands=brands, categories=categories)


@app.route('/admin/editproduct/', methods=['GET', 'POST'])
@login_required
def editproduct():
    
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    form = EditProductsForm()
    products = Products.query.all()
    
    if form.validate_on_submit():
        productname = request.form.get('product')
        return redirect(url_for('editoneproduct', productname=productname))
        
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
    
    
    return render_template('editproduct.html', form=form, products=products)
    

@app.route('/admin/editproduct/<productname>/',  methods=['GET', 'POST'])
@login_required
def editoneproduct(productname):
    
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    product = Products.query.filter_by(name=productname).first()
    form = EditOneProductsForm()
    brands = Brand.query.all()
    categories = Category.query.all()
    
    if form.validate_on_submit():
        brand = request.form.get('brand')
        category = request.form.get('category')
        image = request.files['image']
        if category == 'None':
            product.name, product.price, product.description, product.size, product.brand_id = form.name.data, form.price.data, form.description.data, form.size.data, brand
        else:
            product.name, product.price, product.description, product.size, product.brand_id, product.category_id = form.name.data, form.price.data, form.description.data, form.size.data, brand, category
        product.link = str(form.name.data).replace(' ','-')
        db.session.commit()
        
        if image.filename != '':
            image.filename = f'{product.link}.jpg'
            try:
                os.remove(os.path.join('static/img/products', image.filename)) 
            except:
                pass
            image.save(os.path.join('static/img/products', image.filename))
            flash(f'Вы изменили продукт {form.name.data}', category='success')
            return redirect(url_for('admin'))

    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
    
    
    return render_template('editoneproduct.html', form=form, brands=brands, categories=categories, product=product)




@app.route('/admin/deleteproduct/',  methods=['GET', 'POST'])
@login_required
def deleteproduct():
    
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    form = DeleteProductsForm()
    brands = Brand.query.all()
    
    if form.validate_on_submit():
        product = Products.query.filter_by(name=form.name.data).first()
        db.session.delete(product)
        db.session.commit()
        image_filename = f'{product.link}.jpg'
        if os.path.isfile('../app/static/img/products/' + image_filename):
            os.remove('../app/static/img/products/' + image_filename)
        else:
            pass
        
        flash(f'Вы удалили продукт {form.name.data}', category='success')
        return redirect(url_for('admin'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
    
    
    return render_template('deleteproduct.html', form=form, brands=brands)


@app.route('/admin/allbrand/')
@login_required
def allbrand():
    
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))

    
    brands = Brand.query.all()
    return render_template('allbrand.html', brands=brands)    


@app.route('/admin/allcategory/')
@login_required
def allcategory():
    
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))

    brands = Brand.query.all()
    categorys = Category.query.all()
    return render_template('allcategory.html', categorys=categorys, brands=brands)   


@app.route('/admin/allproduct/')
@login_required
def allproduct():
    
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))

    brands = Brand.query.all()
    products = Products.query.all()
    return render_template('allproduct.html', products=products, brands=brands)   





@app.route('/product/brand/<brandname>/<brandid>')
def brand(brandid, brandname):
    brands = Brand.query.all()
    categorys = Category.query.filter_by(brand_id=brandid)
    products = Products.query.filter_by(brand_id=brandid)
    page = request.args.get('page')
    
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    
    pages = products.paginate(page=page, per_page=9)
    
    return render_template('productbrand.html', brands=brands, products=products, brandname=brandname, categorys=categorys, brandid=brandid, pages = pages)


@app.route('/product/allproduct')
def allproductuser():
    brands = Brand.query.all()
    
    page = request.args.get('page')
    search = request.args.get('search')
    
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if search:
        search = str(search) 
        products = Products.query.filter(Products.name.contains(search) | Products.name.contains(search.lower()) | Products.name.contains(search.title()) | Products.name.contains(search.upper()))
    else:
        products = Products.query.order_by(Products.created) #сначало идут старые
    
    pages = products.paginate(page=page, per_page=9)
    
    return render_template('allproductuser.html', products=products, brands=brands, pages = pages)


@app.route('/product/brand/<brandname>/<brandid>/<categoryid>')
def categorybrand(brandname, brandid, categoryid):
    category = Category.query.filter_by(id=categoryid).first()
    brands = Brand.query.all()
    products = Products.query.filter_by(category_id=categoryid)
    page = request.args.get('page')
    
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    
    pages = products.paginate(page=page, per_page=9)
    
    return render_template('categorybrand.html', brands=brands, products=products, category=category, brandname=brandname, brandid=brandid, pages = pages)


@app.route('/product/<productname>/<productid>', methods=['GET', 'POST'])
def productpage(productname, productid):
        product = Products.query.filter_by(id=productid).first()
        brands = Brand.query.all()
        sizes = product.size.split(' ')
        
        if request.method == 'POST':
            product_size = request.form['size']
            product_qty = request.form['qty']
            if 'cart' not in session:
                session['cart'] = []
            if not session.modified:
                session.modified = True
            
            matching = [d for d in session['cart'] if d['id'] == product.id]
            if matching:
                matching[0]['qty'] += int(product_qty)
                flash('Вы добавили еще один товар в корзину', category='success')
                return redirect(url_for('productpage', productname=productname, productid=productid))
            else:
                session['cart'].append(dict( {'id': int(product.id), 'size': int(product_size), 'price': int(product.price), 'qty': int(product_qty), 'name': product.name, 'link': product.link}))
                flash('Вы добавили товар в корзину ', category='success')
                return redirect(url_for('productpage', productname=productname, productid=productid))
            
        print(session)
        return render_template('productpage.html', product=product,  brands=brands, sizes=sizes)


@app.route('/product/cart/', methods=['GET', 'POST'])
def cart():
    if 'cart' not in session:
        return redirect(url_for('index'))
    
    products = session['cart']
    summa = []
    for i in products:
        summa.append(i['price'])
        
    
    if request.method == 'POST':
        session.pop('cart')
        return redirect(url_for('index'))
    
    sumprice = sum(summa)
    return render_template('cart.html', products=products, sumprice=sumprice)


@app.route('/cart/order/', methods=['GET', 'POST'])
def order():
    form = DeliveryForm()
    products = session['cart']
    
    summa = []
    for i in products:
        summa.append(i['price'])
    
    if form.validate_on_submit():
        product = []
        for i in products:
            product.append(i['name'])
        delivery = request.form['delivery']
        pay = request.form['pay']
        order = Orders(username=form.username.data, email=form.email.data, phone=form.phone.data, city=form.city.data, address=form.address.data, index=form.index.data, delivery=delivery, pay=pay, products=product)
        db.session.add(order)
        db.session.commit()
        session.pop('cart')
        flash('Ваш заказ одобрен! Ждите звонка нашего менеджера.', category='success')
        return redirect(url_for('index'))
    
    sumprice = sum(summa)
    return render_template('order.html', products=products, form=form, sumprice=sumprice)



@app.route('/admin/allorders/')
def allorders():
    
    if current_user.admin_role != 1 :
        flash('Вам не доступна эта страница', category='success')
        return redirect(url_for('index'))
    
    orders = Orders.query.filter_by()
    
    
    return render_template('allorders.html', orders=orders)

    

    
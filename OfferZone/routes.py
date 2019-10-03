import os
from flask import render_template, url_for, flash, redirect, request, abort
from OfferZone import app,db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from OfferZone.models import User,Mall,Shop,Product
from PIL import Image
from OfferZone.forms import RegistrationForm,LoginForm,AccountForm,MallRegistrationForm,ShopRegistrationForm,ProductRegistrationForm




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
def account():
    form=AccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

def save_picture(form_picture):
    random_hex = os.urandom(8).encode('hex')
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(appoot_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/mall/new", methods=['GET', 'POST'])
def new_mall():
    form=MallRegistrationForm()
    if form.validate_on_submit():
        mall = Mall(name=form.name.data, desc=form.desc.data, addr1=form.addr1.data,addr2=form.addr2.data)
        db.session.add(mall)
        db.session.commit()
        flash('Mall has been created!', 'success')
    saved_malls=Mall.query.all()
    return render_template('mall.html', title='New Mall',form=form,malls=saved_malls)

@app.route("/mall/<int:mall_id>/update", methods=['GET', 'POST'])
def update_mall(mall_id):
    mall = Mall.query.get_or_404(mall_id)
    form = MallRegistrationForm()
    if form.validate_on_submit():
        
        mall.name = form.name.data
        mall.desc=form.desc.data
        mall.addr1=form.addr1.data
        mall.addr2=form.addr2.data
        db.session.commit()
        flash('Mall has been updated!', 'success')
        return redirect(url_for('new_mall'))
    elif request.method == 'GET':
        
        form.name.data = mall.name
        form.desc.data= mall.desc
        form.addr1.data=mall.addr1
        form.addr2.data=mall.addr2
    saved_malls=Mall.query.all()
    return render_template('mall.html', title='Update Mall',
                           form=form,malls=saved_malls,action="modify",mall_id=mall_id)


@app.route("/mall/<int:mall_id>/delete", methods=['POST'])
@login_required
def delete_mall(mall_id):
    mall = Mall.query.get_or_404(mall_id)
    db.session.delete(mall)
    db.session.commit()
    flash('Mall has been deleted!', 'success')
    return redirect(url_for('new_mall'))



@app.route("/shop/new", methods=['GET', 'POST'])
def new_shop():
    form=ShopRegistrationForm()
    if form.validate_on_submit():
        shop = Shop(name=form.name.data, addr=form.addr.data, phoneno=form.phoneno.data,desc=form.desc.data)
        db.session.add(shop)
        db.session.commit()
        flash('Shop has been created!', 'success')
    saved_shop=Shop.query.all()
    return render_template('shop.html', title='New Shop',form=form,shops=saved_shop)


@app.route("/shop/<int:shop_id>/update", methods=['GET', 'POST'])
def update_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    form = ShopRegistrationForm()
    if form.validate_on_submit():
        
        shop.name = form.name.data
        shop.addr=form.addr.data
        shop.phoneno=form.phoneno.data
        shop.desc=form.desc.data
        
        db.session.commit()
        flash('shop has been updated!', 'success')
        return redirect(url_for('new_shop'))
    elif request.method == 'GET':
        
        form.name.data = shop.name
        form.addr.data= shop.addr
        form.phoneno.data=shop.phoneno
        form.desc.data=shop.desc
        
     
    saved_shop=Shop.query.all()
    return render_template('shop.html', title='Update shop',
                           form=form,shops=saved_shop,action="modify",shop_id=shop_id)



@app.route("/shop/<int:shop_id>/delete", methods=['POST'])
@login_required
def delete_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    db.session.delete(shop)
    db.session.commit()
    flash('Shop has been deleted!', 'success')
    return redirect(url_for('new_shop'))







@app.route('/shop/<o>',methods = ['GET','POST'])
def index(o):
    user=Shop.query.filter_by(name=o).first()
    if user is None:
        return '<h2>not found'
    else:
        return render_template('simple.html',ab=user.catag)


    

@app.route("/product/new",methods = ['GET','POST'])
def new_product():
    form=ProductRegistrationForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, company=form.company.data, price=form.price.data, desc=form.desc.data )
        db.session.add(product)
        db.session.commit()
        print(product)
        flash('product has been created')
    saved_product=Product.query.all()
    return render_template('product.html',form=form ,title='new product',products=saved_product)


    
@app.route("/product/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductRegistrationForm()
    if form.validate_on_submit():
        
        product.name = form.name.data
        product.company=form.company.data
        product.price=form.price.data
        product.desc=form.desc.data
        db.session.commit()
        flash('Product has been updated!', 'success')
        return redirect(url_for('new_product'))
    elif request.method == 'GET':
        
        form.name.data = product.name
        form.company.data= product.company
        form.price.data=product.price
        form.desc.data=product.desc
    saved_product=Product.query.all()
    return render_template('product.html', title='Update Product',
                           form=form,products=saved_product,action="modify",product_id=product_id)


    


@app.route("/product/<int:product_id>/delete", methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted!', 'success')
    return redirect(url_for('new_product'))





@app.route('/product/<k>',methods = ['GET','POST'])
def pro(k):
    user=Product.query.filter_by(name=k).first()
    if user is None:
        return '<h2>not found'
    else:
        return render_template('pro.html',ab=user.company,bc=user.price)



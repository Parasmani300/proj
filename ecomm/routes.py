from ecomm import app,db,auth,storage,UPLOAD_FOLDER
from flask import Flask, render_template, request, json, Response,redirect,flash,url_for,session,jsonify
# from flask_login import login_user,current_user,logout_user,login_required
from ecomm.models import User,Products
from ecomm.forms import LoginForm,RegisterForm
from werkzeug.utils import secure_filename
import os

##############################################################

#########################################
user = None
def validate_session():
    try:
        if(session['usr']):
            token = session['usr']
            user = auth.get_account_info(token)
            return user
    except:
        return None

@app.route('/',methods=["GET","POST"])
def index():
    user = validate_session()
    if user:
        if request.form.get('prod_id'):
            print(user)
            prod_id = request.form.get('prod_id')
            user_key = user['users'][0]['localId']
            db.child("user").child(user_key).child("cart").push(prod_id)
    beer = db.child("products").child("Beer").get()
    whiskey = db.child("products").child("Whiskey").get()
    vodaka = db.child("products").child("Vodaka").get()
    return render_template('index.html',beers=beer,whiskeys=whiskey,vodakas = vodaka,user=user)

@app.route('/buy_now',methods = ['GET','POST'])
def buy_now():
    user = validate_session()
    prod_id = request.args.get('prod_id')
    print(prod_id)
    product = db.child("products").get().val()[prod_id]
    if user == None:
        return redirect(url_for('login'))
    return render_template('buynow.html',product=product,user=user)

@app.route('/login',methods=['GET','POST'])
def login():
    session['usr'] = None
    if session['usr']:
        return redirect(url_for('index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            try:
                user = auth.sign_in_with_email_and_password(email,password)
                user = auth.refresh(user['refreshToken'])
                user_id = user['idToken']
                session['usr'] = user_id
                return redirect(url_for('index'))
            except:
                flash("Invalid Credentials","danger")
        return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        phone_no = form.phone_no.data
        if password == confirm_password:
            new_user = auth.create_user_with_email_and_password(email,password)
            print(new_user)
            token = new_user['idToken']
            data = {
            'user_id': new_user['localId'],
            'firstname': firstname,
            'lastname': lastname,
            'phone_no': phone_no,
            'role': 'Subscriber' }
            db.child("user").child(new_user['localId']).set(data)
            flash("User Registered Successfully")
    return render_template('register.html',form=form,category='success')

@app.route('/logout')
def logout():
    session['usr'] = None
    return redirect('/')


@app.route('/forgot_password',methods=["GET","POST"])
def forgot_password():
    if request.form.get('email'):
        email = request.form.get('email')
        reset_pwd = auth.send_password_reset_email(email)
        flash("Reset Password link sent check, Check in your registered email")
    return render_template('forgot_password.html')

@app.route('/my_cart',methods=["GET","POST"])
def my_cart():
    user = validate_session()
    product_list = []
    cart_items = None
    total_price = 0
    if user:
        user_key = user['users'][0]['localId']
        try:
            cart_items = db.child("user").child(user_key).child("cart").get()
        except:
            cart_items = None
        if cart_items:
            try:
                for v in cart_items.each():
                    product_id = v.val()
                    item = db.child("products").child(product_id).get().val()
                    p_item = dict(item)
                    p_item['prod_id'] = product_id
                    total_price = total_price + int(p_item['price'])
                    product_list.append(p_item)
            except:
                pass
        
        if request.args.get('delete_prod_id'):
            delete_id = request.args.get('delete_prod_id')
            key_to_delete = None
            for v in cart_items.each():
                if v.val() == delete_id:
                    key_to_delete = v.key()
                    break
            if key_to_delete:
                db.child("user").child(user_key).child("cart").child(key_to_delete).remove()
            return redirect(url_for('my_cart'))
    return render_template('my_cart.html',product_list=product_list,user=user,total_price=total_price)

@app.route('/profile')
def profile():
    user = validate_session()
    send_profile = None
    if user:
        user_key = user["users"][0]["localId"]
        display_profile = db.child("user").child(user_key).get()
        send_profile = dict(display_profile.val())
        print(send_profile)
    return render_template("profile.html",user=user,send_profile=send_profile)


#######################################################################################################################################
## Admin not to be includes with the website, to be used locally as an app ############################################################
@app.route('/admin',methods=["GET","POST"])
def admin():
    user = validate_session()
    if user:
        user_key = user["users"][0]["localId"]
        admin_privelege = db.child("user").child(user_key).get()
        admin = dict(admin_privelege.val())
        if admin['role'] != 'Admin':
            return redirect(url_for('logout'))
        ################## Users ####################
        if request.args.get('view_user'):
            all_user = db.child("user").get()
            user_detail = dict(all_user.val())
            return render_template('view_user.html',user_detail=user_detail,user=user)
        elif request.args.get('add_user'):
            return render_template('add_user.html',user=user)
        elif request.args.get('delete_user'):
            return render_template('delete_user.html',user=user)
        elif request.args.get('update_user'):
            return render_template('update_user.html',user=user)

        if request.args.get('add_products'):
            if request.method == "POST":
                upload_image = request.files['upload_image']
                fname = secure_filename(upload_image.filename)
                upload_image.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
                upload_path = os.path.join(upload_path,'uploads')
                upload_path = os.path.join(upload_path,fname)
                try:
                    storage.child("images/"+ fname).put(upload_path)
                except:
                    fash("Upload Error")

                image_url = storage.child("images/"+ fname).get_url(session['usr'])
                product_name = request.form.get('product_name')
                product_description = request.form.get('product_description')
                product_quantity = request.form.get('product_quantity')
                product_price = request.form.get('product_price')
                product_brand = request.form.get('product_brand')
                product_category = request.form.get('product_category')

                add_product = {
                    'name': product_name,
                    'description': product_description,
                    'quantity': product_quantity,
                    'price': product_price,
                    'brand': product_brand,
                    'image_url': image_url,
                    'trending': False
                }
                try:
                    db.child("products").child(product_category).push(add_product)
                    flash("Upload Successfull")
                except:
                    flash("Some Error Occured")
            return render_template('add_products.html',user=user)
        if request.args.get('delete_products'):
            return render_template('delete_products.html',user=user)
    
    return render_template('admin_home.html',user=user)
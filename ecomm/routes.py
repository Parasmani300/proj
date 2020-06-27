from ecomm import app,db,auth
from flask import Flask, render_template, request, json, Response,redirect,flash,url_for,session,jsonify
# from flask_login import login_user,current_user,logout_user,login_required
from ecomm.models import User,Products
from ecomm.forms import LoginForm,RegisterForm

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
    prod = db.child("products").get()
    return render_template('index.html',products=prod,user=user)

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
            'phone_no': phone_no }
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
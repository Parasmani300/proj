from ecomm import app
from flask import Flask, render_template, request, json, Response,redirect,flash,url_for,session
from flask_login import login_user,current_user,logout_user,login_required

from ecomm.models import User,Products
from ecomm.forms import LoginForm,RegisterForm

products = [{
        'id': '0',
        'name': 'Royal Stag',
        'description': 'Hey this is Royal in case you forgot',
        'price': '600'
    },
    {
        'id': '1',
        'name': 'Bag Piper',
        'description': 'Hey this is Royal in case you forgot',
        'price': '900'
    },
    {
        'id': '2',
        'name': 'Whiskey',
        'description': 'Hey this is Royal in case you forgot',
        'price': '1200'
    }
    ]

@app.route('/',methods=["GET","POST"])
def index():
    print(current_user)
    if request.form.get('prod_id'):
        prod_id = request.form.get('prod_id')
        print(prod_id)
    prod = Products.objects.all()
    return render_template('index.html',products=prod)

@app.route('/buy_now',methods = ['GET','POST'])
@login_required
def buy_now():
    prod_id = request.args.get('prod_id')
    prod = {}
    for product in products:
        if product['id'] == prod_id:
            prod = product
            break
    
    return render_template('buynow.html',product=product)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email)
        print(password)
        user = User.objects(email=email).first()
        print(user)
        if user and user.get_password(password):
            login_user(user)
            flash(f'{current_user.firstname},Welcome','success')
            next = request.args.get('next')
            return redirect(next or url_for('index'))
        else:
            flash("Invalid Credentials",'warning')    
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
            user = User(user_id=email,firstname=firstname,lastname=lastname,email=email,password=password,phone_no=phone_no)
            user.set_password(password)
            user.save()
            flash('User Registered Successfully','success')
            return redirect('/')
    return render_template('register.html',form=form,category='success')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/user',methods=['GET','POST'])
def user():
    # User(user_id=1,firstname="Paras",lastname="Mani",password="123456",phone_no="9546539823",email="parasmani300@gmail.com").save()
    # User(user_id=2,firstname="AB",lastname="CD",password="123456",phone_no="9546539823",email="parasmani300@gmail.com").save()
    user = User.objects.all()
    print(user[0].firstname)
    return render_template('base.html')

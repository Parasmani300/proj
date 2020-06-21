from ecomm import app
from flask import Flask, render_template, request, json, Response,redirect,flash,url_for,session
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
    if request.form.get('prod_id'):
        prod_id = request.form.get('prod_id')
        print(prod_id)
    prod = Products.objects.all()
    return render_template('index.html',products=prod)

@app.route('/buy_now',methods = ['GET','POST'])
def buy_now():
    prod_id = request.args.get('prod_id')
    prod = {}
    for product in products:
        if product['id'] == prod_id:
            prod = product
            break
    
    return render_template('buynow.html',product=product)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html',form=form)

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html',form=form)

@app.route('/user',methods=['GET','POST'])
def user():
    # User(user_id=1,firstname="Paras",lastname="Mani",password="123456",phone_no="9546539823",email="parasmani300@gmail.com").save()
    # User(user_id=2,firstname="AB",lastname="CD",password="123456",phone_no="9546539823",email="parasmani300@gmail.com").save()
    user = User.objects.all()
    print(user[0].firstname)
    return render_template('base.html')

from ecomm import app
from flask import Flask, render_template, request, json, Response,redirect,flash,url_for

products = [{
        'id': '0',
        'name': 'Royal Stag',
        'description': 'Hey this is Royal in case you forgot'
    },
    {
        'id': '1',
        'name': 'Bag Piper',
        'description': 'Hey this is Royal in case you forgot'
    },
    {
        'id': '2',
        'name': 'Whiskey',
        'description': 'Hey this is Royal in case you forgot'
    }
    ]

@app.route('/')
def index():
    return render_template('index.html',products=products)

@app.route('/buy_now',methods = ['GET','POST'])
def buy_now():
    prod_id = request.args.get('prod_id')
    prod = {}
    for product in products:
        if product['id'] == prod_id:
            prod = product
            break
    
    return render_template('buynow.html',product=product)
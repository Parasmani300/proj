
class User:
    user_id = ""
    firstname = ""
    lastname = ""
    password = ""
    phone_no = ""
    email = ""

    def __init__(self,user_id,firstname,lastname,password,phone_no,email):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.phone_no = phone_no
        self.email = email
    def tojson(self):
        return {'user_id':self.user_id,'firstname':self.firstname,'lastname':self.lastname,'password':self.password,'phone_no':self.phone_no,'email':self.email}

class Products():
    id = ""
    name= ""
    description = ""
    price = ""
    quantity = 0
    trending = False

    def __init__(self,id,name,description,price,trending,quantity):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.trending = trending
        self.quantity = quantity
    def tojson(self):
        return {'id':self.id,'name':self.name,'description':self.description,'price':self.price,'trending':self.trending,'quantity':self.qunatity} 


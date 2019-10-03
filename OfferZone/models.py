from OfferZone import db,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return self.username+","+self.email




class Mall(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    desc = db.Column(db.String(200))
    addr1 = db.Column(db.String(100))
    addr2 = db.Column(db.String(100))
    addr3 = db.Column(db.String(100))
    phone=db.Column(db.String(25))
    open_time=db.Column(db.String(10))
    close_time=db.Column(db.String(10))
    latitude = db.Column(db.String(40))
    Logitude = db.Column(db.String(40))
    image_file = db.Column(db.String(50), nullable=False, default='default.jpg')
   

    

    def __repr__(self):
        return self.name+","+self.addr1


class Shop(db.Model,UserMixin):
        shoptypes = [('Textails','Textails'),('jewllery','jewllery'),('super market','super market')]
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(40), unique=False, nullable=False)
        
        addr = db.Column(db.String(100))
        phoneno=db.Column(db.String(25))
        desc = db.Column(db.String(200))
       
      
       
        


class Product(db.Model,UserMixin):
     id = db.Column(db.Integer,primary_key=True)
     name = db.Column(db.String(40),unique=False,nullable=False)
     company = db.Column(db.String(40))
     price = db.Column(db.Integer)
     desc = db.Column(db.String(199))
   

     
   
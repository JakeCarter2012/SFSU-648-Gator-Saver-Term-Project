from datetime import datetime
from sfsuListings import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


class Posts(db.Model):
    name = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
    author = db.Column(db.String(80), unique=False, nullable=True, primary_key=False)
    price = db.Column(db.REAL, unique=False, nullable=False, primary_key=False)
    description = db.Column(db.String(300), unique=False, nullable=False, primary_key=False)
    image = db.Column(db.String(80), unique=False, nullable=True, primary_key=False)
    id = db.Column(db.INTEGER, unique=True, nullable=False, primary_key=True)
    category = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    approval = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Name: {}>".format(self.name)
        return "<Author: {}".format(self.author)
        return "<id: {}".format(self.id)
        return "<price: {}".format(self.price)
        return "<image: {}".format(self.image)
        return "<category: {}".format(self.category)


class Admin(db.Model):
    AdminName = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    password_hash = db.Column(db.String(96), unique=False, nullable=False, primary_key=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Username: {}>".format(self.UserName)
        return "<Hashed Password: {}".format(self.password_hash)


class Messages(db.Model):
    id = db.Column(db.INTEGER, unique=True, nullable=False, primary_key=True)
    sentFrom = db.Column(db.String(30), unique=False, nullable=False, primary_key=False)
    sentTo = db.Column(db.String(30), unique=False, nullable=False, primary_key=False)
    postId = db.Column(db.INTEGER, unique=False, nullable=False, primary_key=False)
    postTitle = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    message = db.Column(db.String(300), unique=False, nullable=False, primary_key=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "sentFrom: {}".format(self.sentFrom)
        return "sentTo: {}".format(self.sentTo)
        return "postId: {}".format(self.postId)
        return "message: {}".format(self.message)

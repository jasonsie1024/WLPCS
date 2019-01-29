from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64))
    
    def __repr__(self):
        return '<User %r>' % self.username

class Message(db.Model):
    __table_name = 'messages'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text(200))
    t = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Message %r>" % self.content

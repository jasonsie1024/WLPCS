from . import db, login_manager
from flask_login import UserMixin
from markdown import markdown
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
import bleach

class Setting(db.Model):
    __tablename__ = 'settings'
    setting = db.Column(db.String, primary_key = True, index = True)
    value = db.Column(db.Text)

    def __repr__(self):
        return '<Setting %r>' % self.setting
    
    def get_or_create(**kwargs):
        instance = Setting.query.filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = Setting(**kwargs)
            instance.value = ''
            db.session.add(instance)
            db.session.commit()
            return instance

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), index = True)
    password_hash = db.Column(db.String(128))
    status = db.Column(db.String)
    score = db.Column(db.Integer)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text(200))
    content_html = db.Column(db.Text)
    t = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    

    def __repr__(self):
        return "<Message %r>" % self.content
    
    @staticmethod
    def on_change_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'u;', 'h1', 'h2', 'h3', 'br', 'p']
        target.content_html = bleach.linkify(bleach.clean(markdown(value, output_format = 'html'), tags = allowed_tags))
    
db.event.listen(Message.content, 'set', Message.on_change_content)

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key = True)
    pid = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    code = db.Column(db.Text)
    code_hash = db.Column(db.String)
    time = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    verdict = db.Column(db.String(10))
    score = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Submission %r>' % id
    
    @staticmethod
    def on_change_code(target, value, oldvalue, initiator):
        target.code_hash = md5(value.encode()).hexdigest()
    
db.event.listen(Submission.code, 'set', Submission.on_change_code)
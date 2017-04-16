from app import db


class User(db.Model):
    username = db.Column(db.String(64), primary_key=True, index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=False)
    name = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    phoneno = db.Column(db.String(20), index=True, unique=True)

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % (self.username)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(64), index=True, unique=False)
    author = db.Column(db.String(64),index=True, unique=False)
    content = db.Column(db.String(200), index=True, unique=False)

    def __repr__(self):
        return '<User %r>: %r' %(self.username,self.content,)




import secrets
from . import db 
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    tasks = db.relationship('Task', backref='user')
    token = db.Column(db.String, index=True, unique=True)
    token_expiration = db.Column(db.DateTime(timezone=True))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs.get('password', ''))
        

    def set_password(self, plaintext_password):
        self.password = generate_password_hash(plaintext_password)
        self.save()

    def check_password(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)


    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "username": self.username,
            "email": self.email,
            "dateCreated": self.date_created
        }    
    
    def get_token(self):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(tzinfo=timezone.utc) > now + timedelta(minutes=1):
            return {"token": self.token, "tokenExpiration": self.token_expiration.isoformat()}
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(hours=1)
        self.save()
        return {"token": self.token, "tokenExpiration": self.token_expiration.isoformat()}
        
    def find_by_token(token):
        return User.query.filter_by(token=token).filter(User.token_expiration > datetime.now(timezone.utc)).first()

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    created_at =db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()
        
    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'complete': self.complete,
            'due_date': self.due_date.strftime('%Y-%m-%d %H:%M:%S') if self.due_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
            
        }
    
    def update(self, **kwargs):
        allowed_fields = {'title', 'description'}

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        self.save()    
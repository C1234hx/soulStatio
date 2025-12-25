from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True, max_length=50)
    email = StringField(required=True, unique=True, max_length=100)
    age = IntField(min_value=0, max_value=150)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'users',
        'ordering': ['-created_at']
    }

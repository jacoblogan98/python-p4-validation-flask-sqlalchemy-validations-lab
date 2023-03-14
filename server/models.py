from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String)

    posts = db.relationship('Post', backref='author')

    @validates('name')
    def validate_name(self, key, name):
        names = db.session.query(Author.name).all()
        if not name:
            raise ValueError("Name field is required.")
        elif name in names:
            raise ValueError("Name must be unique.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must be 10 characters.")
        
        return phone_number

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    summary = db.Column(db.String)
    category = db.Column(db.String)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    @validates('title')
    def validate_title(self, key, title):
        CLICKBAIT = ["Won't Believe", "Secret", "Top", "Guess"]

        if not any(substring in title for substring in CLICKBAIT):
            raise ValueError("No clickbait found.")
        
        return title
    
    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        
        return content
    
    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be a maximum of 250 characters.")
        
        return summary
    
    @validates("category")
    def validate_category(self, key, category):
        CATEGORIES = ["Fiction", "Non-Fiction"]

        if category not in CATEGORIES:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        
        return category
    
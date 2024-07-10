from app import *
with app.app_context():
    database.create_all()
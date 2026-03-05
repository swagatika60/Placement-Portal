import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-123'
    # This path works on any computer or server
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'placement.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

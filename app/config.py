import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'purple pandaz'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATION = True
    POSTS_PER_PAGE = 10
    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOAD_FOLDER')

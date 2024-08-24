import os
from dotenv import load_dotenv
import logging 

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # new attributes
    DEBUG = os.environ.get('FLASK_DEBUG') == '1'
    HOST = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_RUN_PORT', 5002))
    
    # Logging Configuration
    LOG_FOLDER = os.environ.get('LOG_FOLDER', 'logs')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')    
    LOG_PATH = os.path.join(LOG_FOLDER, LOG_FILE)    
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_MAX_SIZE = int(os.environ.get('LOG_MAX_SIZE', 10 * 1024 * 1024))  # 10 MB
    LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 5))
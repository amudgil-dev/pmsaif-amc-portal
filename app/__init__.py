from flask import Flask
from config import Config

from app.extensions import db, login_manager, csrf, mail
import logging
from logging.handlers import RotatingFileHandler
from app.cli import load_sample_data_command
import os
from app.helpers.helper_jinja import month_year_format

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.routes.route_home import bp_home
    from app.routes.route_txn import bp_txn
    from app.routes.route_auth import bp_auth
    from app.routes.route_pms import bp_pms
    from app.routes.route_stocks import bp_stocks
    from app.routes.route_sectors import bp_sectors     
    from app.routes.route_nav import bp_nav      
    from app.routes.route_admin import bp_admin                
    
    
    
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_txn)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_pms)
    app.register_blueprint(bp_stocks)
    app.register_blueprint(bp_sectors)
    app.register_blueprint(bp_nav)    
    app.register_blueprint(bp_admin)        
    

    # Set up logging
    # logging.basicConfig(filename='app.log', level=logging.INFO)

    # Set up logging
    # if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
    if not os.path.exists(app.config['LOG_FOLDER']):
        os.makedirs(app.config['LOG_FOLDER'])
    
    file_handler = RotatingFileHandler(app.config['LOG_PATH'],
                                        maxBytes=app.config['LOG_MAX_SIZE'],
                                        backupCount=app.config['LOG_BACKUP_COUNT'])
    file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    file_handler.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(file_handler)

    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.info('Application startup')


    # For detailed logging specially exceptions creating custom handler
    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     app.logger.error('Unhandled Exception: %s', str(e), exc_info=True)
    #     # Return appropriate error response
    #     print('retuning error...')
    #     return str(e)
    
    
    # Register the custom filter
    app.jinja_env.filters['month_year_format'] = month_year_format
    
    # Register CLI command
    app.cli.add_command(load_sample_data_command)    
    


    return app
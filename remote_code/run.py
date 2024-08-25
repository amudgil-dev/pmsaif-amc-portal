from app import create_app, db
from app.models.models import User1, Transaction
from config import Config
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User1, 'Transaction': Transaction}

if __name__ == '__main__':
     app.run(
        debug=Config.DEBUG if hasattr(Config, 'DEBUG') else os.getenv('FLASK_DEBUG') == '1',
        host=Config.HOST if hasattr(Config, 'HOST') else os.getenv('FLASK_RUN_HOST', '0.0.0.0'),
        port=int(Config.PORT if hasattr(Config, 'PORT') else os.getenv('FLASK_RUN_PORT', 5002))
    )
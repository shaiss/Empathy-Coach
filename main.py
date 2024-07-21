import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO
from modules import database
from routes import init_routes

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
socketio = SocketIO(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Reduce logging level for some noisy libraries
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)
logging.getLogger('socketio').setLevel(logging.WARNING)

# Database setup
db = database.get_db()

# Initialize routes
init_routes(app, socketio, db)

if __name__ == '__main__':
    socketio.run(app, debug=True)
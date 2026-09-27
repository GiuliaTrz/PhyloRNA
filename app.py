import threading
import os 
from dotenv import load_dotenv
from flask import Flask
import logging
from logging.handlers import TimedRotatingFileHandler
from routes.contacts import contact_bp
from routes.sources import sources_bp
from routes.tutorial import tutorial_bp
from routes.home import home_bp
from routes.phylorna import phylorna_bp

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(contact_bp, url_prefix="/contact")
app.register_blueprint(sources_bp, url_prefix="/sources")
app.register_blueprint(tutorial_bp, url_prefix="/tutorial")
app.register_blueprint(phylorna_bp, url_prefix="/phylorna")
app.register_blueprint(home_bp, url_prefix="/")

# Carica le environment variables dal file .env 
load_dotenv()

app.secret_key = os.getenv("secret_key") 

# Gestione logging errori
loggingFileHandler = TimedRotatingFileHandler("error.txt", when='midnight', interval=1, backupCount=7)
loggingFileHandler.setLevel(logging.ERROR)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s [%(name)s]: %(message)s (%(pathname)s:%(lineno)d)'
)
loggingFileHandler.setFormatter(formatter)
app.logger.addHandler(loggingFileHandler)

lock = threading.Lock()

if __name__ == '__main__':
    #sul server rimarrà a 5000 (nella mia versione in locale devo usare una porta come la 45001, la 5000 è occupata dal mac)
    # Cambiamo la porta a 45001 e attiviamo il debug per vedere gli errori in tempo reale
    app.run(host=os.getenv("host_address"), port=os.getenv("port"), debug=True)

import sys
import logging
logging.basicConfig(level=logging.DEBUG, filename='/var/www/GP_Cintioni_Falcone/website_management/website_management.log', format='%(asctime)s %(message)s')
sys.path.insert(0, '/var/www/GP_Cintioni_Falcone/website_management')
sys.path.insert(0, '/var/www/GP_Cintioni_Falcone/Flaskappenv/lib/python3.8/site-packges')
from app import app as application


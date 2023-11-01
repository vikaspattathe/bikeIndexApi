from api import app
import logging

FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
logging.basicConfig(filename='./logs/BikeIndexApp.log',format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info('Application started')
    app.run()

    


from hooyootracker.logger import Logger
from hooyootracker.webapp import app

logger = Logger()
logger.info("HooYooTracker has been started")

app.run()

import logging
import os

LOG_PATH = os.path.expanduser("~/smartlock.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)

logger = logging.getLogger("smartlock")

import logging

FORMATTER = "%(asctime)s - (%(filename)s) - [%(levelname)s] - %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMATTER)

logging.critical("crit")
logging.error("error")
logging.warning("warn")
logging.info(f"info:{'tutorial'}")
logging.debug("debug")

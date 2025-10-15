"""This module sets up the logger."""

from logging import DEBUG, ERROR, INFO, Formatter, StreamHandler, getLogger

logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Standard output handler
streamHandler = StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

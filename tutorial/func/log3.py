import logging

# create formatter(ログの出力形式)
FORMATTER = "%(asctime)s - (%(filename)s) - [%(levelname)s] - %(message)s"

logging.basicConfig(level=logging.INFO)

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# handler = logging.StreamHandler()
handler = logging.FileHandler("log/debug_handler.log", mode="w")
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(FORMATTER))
logger.addHandler(handler)

warn_handler = logging.FileHandler("log/info_handler.log", mode="w")
warn_handler.setLevel(logging.WARNING)
warn_handler.setFormatter(logging.Formatter(FORMATTER))
logger.addHandler(warn_handler)

logger.debug("ロガーで取得したデバッグログです。!!!!!!!!!!!!!")
logger.info("通常の挙動です。")
logger.warning("警告です。")
logger.error("ファイルが見つかりません。")
logger.critical("緊急事態です。")

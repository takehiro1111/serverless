import logging.config
import json

# JSON ファイルをロードしてロギング設定を適用
config_path = 'logging.json'
with open(config_path, 'r') as f:
    config = json.load(f)

logging.config.dictConfig(config)

# ログ出力テスト
logger = logging.getLogger()
logger.debug("This is a debug message.")
logger.info("Sensitive data: password=12345")
logger.warning("This is a warning message.")
logger.error("This is an error message.")

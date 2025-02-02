from logging import INFO, Formatter, StreamHandler, getLogger

# ログ定義
logger = getLogger(__name__)
logger.setLevel(INFO)
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 標準出力
streamHandler = StreamHandler()
streamHandler.setFormatter(formatter)

# ロガーにハンドラーを追加
logger.addHandler(streamHandler)

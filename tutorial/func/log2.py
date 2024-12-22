import logging
import os

# ログディレクトリ作成
os.makedirs('log', exist_ok=True)

# ログフォーマット
FORMATTER = '%(asctime)s - (%(filename)s) - [%(levelname)s] - %(message)s'

# ロガー作成
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# DEBUG ログ用ハンドラー
debug_handler = logging.FileHandler('log/debug_handler.log', mode='w')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(logging.Formatter(FORMATTER))
logger.addHandler(debug_handler)

# WARNING ログ用ハンドラー
warn_handler = logging.FileHandler('log/info_handler.log', mode='w')
warn_handler.setLevel(logging.WARNING)
warn_handler.setFormatter(logging.Formatter(FORMATTER))
logger.addHandler(warn_handler)

# ログ出力
logger.debug('ロガーで取得したデバッグログです。')
logger.info('通常の挙動です。')
logger.warning('警告です。')
logger.error('ファイルが見つかりません。')
logger.critical('緊急事態です。')

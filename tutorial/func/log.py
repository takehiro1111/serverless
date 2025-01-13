# import logging

# # create formatter(ログの出力形式)
# FORMATTER = logging.Formatter('%(asctime)s - (%(filename)s) - [%(levelname)s] - %(message)s')

# # logging.basicConfig(filename='test.log',encoding='utf-8', level=logging.INFO)
# logging.basicConfig(level=logging.INFO,format=FORMATTER)

# # create logger
# logger = logging.getLogger(__name__)

# # handler = logging.StreamHandler()
# handler = logging.FileHandler(
#   'log/debug_handler.log',mode='w'
#   )
# handler.setLevel(logging.DEBUG)
# handler.setFormatter(FORMATTER)

# warn_handler = logging.FileHandler(
#   'log/warn_handler.log',mode='w'
#   )
# warn_handler.setLevel(logging.WARNING)
# warn_handler.setFormatter(FORMATTER)

# logger.setLevel(logging.DEBUG)
# logger.addHandler(handler)
# logger.addHandler(warn_handler)

# logger.debug('ロガーで取得したデバッグログです。')
# logger.info('通常の挙動です。')
# logger.warning('警告です。')
# logger.error('ファイルが見つかりません。')
# logger.critical('緊急事態です。')


# logger.debug('ロガーでデバッグを設定しました。')

# create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# logging.critical('crit')
# logging.error('error')
# logging.warning('warn')
# logging.info(f'info:{'tutorial'}')
# logging.debug('debug')

# logging.info(f'info {'test'}')
# logging.info('info {}'.format('test'))
# logging.info('test %s %s','test','test2' ) # python2系で使用されていた書き方
# logging.info('test %s' % 'test' )
# logging.info('test %s-%s' % ('test','test2') )

import logging

# ロガーを作成
logger = logging.getLogger("example_logger")
logger.setLevel(logging.DEBUG)

# StreamHandler を作成
stream_handler = logging.StreamHandler()  # デフォルトは sys.stderr
# ロガーにハンドラーを追加
logger.addHandler(stream_handler)

# ログフォーマットを設定
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)


# ログフィルターの内容を定義
class LogFilter(logging.Filter):
    def filter(self, ignore):
        word = ignore.getMessage()
        return "password" not in word


# ログフィルターを設定
logger.addFilter(LogFilter())

# ログを出力
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("password = 'xxxx'")

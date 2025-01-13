import logging


class LogFilter(logging.Filter):
    def __init__(self, words=None):
        super().__init__()
        l = []
        self.words = words or l

    def filter(self, record):
        # メッセージに特定の単語が含まれている場合は False を返す
        return not any(word in record.getMessage() for word in self.words)

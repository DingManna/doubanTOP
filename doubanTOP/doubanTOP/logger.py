import logging
from logging import StreamHandler, FileHandler, Formatter
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import datetime
import sys
import traceback
import os


class LOG(object):
    Today = datetime.datetime.now()  # 取得现在的时间
    # filename='scrapy_{}_{}_{}.log'.format(Today.year,Today.month,Today.day)#以时间为文件名
    filename = '/Users/tanyou/Desktop/doubanTOP/doubanTOP/doubanTOP/douban.log'
    # filename = './douban.log'
    log_format = "%(asctime)s|%(levelname)s|%(filename)s|%(funcName)s|%(message)s|%(lineno)d"

    @classmethod
    def log_init(self):
        log = logging.getLogger(__name__)
        # handler1 = StreamHandler()  # 输出
        handler = FileHandler(self.filename + '_{}.log'.format(os.getpid()), encoding="utf-8")  # 写入
        log.setLevel(logging.INFO)
        # handler1.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
        format = Formatter(self.log_format)
        # handler1.setFormatter(format)
        handler.setFormatter(format)

        # 回滚
        # filehandler = logging.handlers.RotatingFileHandler(self.filename, maxBytes=5000, backupCount=5)
        filehandler = logging.handlers.TimedRotatingFileHandler(self.filename + '_{}.log'.format(os.getpid()), when='M',
                                                                interval=1, backupCount=3)
        filehandler.suffix = "%Y-%m-%d.log"  # 按天删
        filehandler.setFormatter(format)
        log.addHandler(filehandler)

        log.addHandler(handler)
        # log.addHandler(handler1)

        return log

    @classmethod
    def debug(self, message):
        log = self.log_init()
        log.debug(message)

    @classmethod
    def warning(self, message):
        log = self.log_init()
        log.warning(message)

    @classmethod
    def error(self, message):
        log = self.log_init()
        log.error(message)

    @classmethod
    def critical(self, message):
        log = self.log_init()
        log.critical(message)

    @classmethod
    def info(self, message):
        log = self.log_init()
        log.info(message)



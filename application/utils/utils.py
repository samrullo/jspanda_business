import datetime
import logging

to_yyyymmdd = lambda x: datetime.datetime.strftime(x, '%Y%m%d')


def get_logger():
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    return logging.getLogger(__file__)

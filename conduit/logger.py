import logging,os

from datetime import datetime
import logging,os
from typing import Any

class single:
    def __init__(self,cls) -> None:
        self.cls = cls
        self.cls.instance = None
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self.cls.instance:
            self.cls.instance = self.cls(*args, **kwds)
        return self.cls.instance
@single
class decorated_logger:
    def __init__(self) -> None:
        args = {
            'save_root': './log',
        }
        if not os.path.exists(args["save_root"]):
            os.makedirs(args['save_root'])
        self.time_str = datetime.strftime(datetime.now(), '%m%d-%H%M%S')
        self.logger = self.get_logger(os.path.join(args["save_root"], '{:s}.log'.format(self.time_str)))

    def get_logger(self, log_file):
        logger = logging.getLogger(log_file)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger
logger = decorated_logger().logger

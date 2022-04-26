import logging
import traceback


class IndentFormatter(logging.Formatter):
    """
    Custom logger adapted from https://code.activestate.com/recipes/412603-stack-based-indentation-of-formatted-logging/

    Warning: Using this logger might decrease performance.

    """

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.baseline = len(traceback.extract_stack())

    def format(self, rec):
        stack = traceback.extract_stack()
        rec.indent = "│ " * (len(stack) - self.baseline)
        out = logging.Formatter.format(self, rec)
        del rec.indent
        return out


logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = IndentFormatter(
    "[%(asctime)s:%(msecs)03d] %(levelname)-8s %(indent)s%(message)s",
    "%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

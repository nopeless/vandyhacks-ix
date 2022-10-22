import logging
import sys, os

fmt = "[%(asctime)s] %(relative_path)s:%(lineno)d %(levelname)s - %(message)s"

old_factory = logging.getLogRecordFactory()

cwd = os.getcwd()

# Hook
def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.relative_path = os.path.relpath(record.pathname, cwd)
    return record


logging.setLogRecordFactory(record_factory)

logging.basicConfig(
    filename="game.debug.log", level=logging.DEBUG, filemode="w", format=fmt
)
logging.info("loaded logger from config")

root = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

root.addHandler(handler)

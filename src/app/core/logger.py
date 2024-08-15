import logging
import logging.handlers
import os

formatter = logging.Formatter('%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

my_local = os.getenv('MY_LOCAL')
if my_local == '1':
    logging.basicConfig(
            level=logging.INFO,
            # format="%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s",
            handlers=[stream_handler]
        )
my_logger = logging.getLogger('SCP')
my_logger.setLevel(logging.INFO)
print(f"my_logger = {my_logger}")
print(f"my_logger_handlers = {my_logger.handlers}")

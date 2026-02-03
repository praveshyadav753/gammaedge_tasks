import logging
import json_logging
# json_logging.init_non_web(enable_json=True)
logging.basicConfig(format='%(levelname)s,%(asctime)s:%(message)s',level=logging.DEBUG,datefmt=' %I:%M: %S %p')
logger = logging.getLogger("my-logger")
logger.info("User login attempt", extra={'user_id': 123, 'status': 'failed'})

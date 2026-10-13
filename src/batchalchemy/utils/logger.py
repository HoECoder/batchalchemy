import logging
import sys

def setup_logger():
    logger = logging.getLogger("BatchAlchemy")
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler("rename_history.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler (for the UI console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

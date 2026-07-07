"""
Unified Logging Facility providing synchronized console and file telemetry.
"""
import logging
from config import LOG_FILE

def setup_logger(name: str = "NetMon") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        c_handler.setFormatter(formatter)
        
        # File Handler
        f_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(formatter)
        
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
    return logger
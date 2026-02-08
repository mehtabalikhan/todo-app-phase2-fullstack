import logging
from typing import Optional
from datetime import datetime
import json
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration"""
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def log_event(
    event_type: str,
    message: str,
    level: LogLevel = LogLevel.INFO,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
    **kwargs
):
    """Log a structured event"""
    logger = logging.getLogger(__name__)

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "message": message,
        "level": level.value,
        "user_id": user_id,
        "request_id": request_id,
        **kwargs
    }

    log_method = getattr(logger, level.value.lower())
    log_method(json.dumps(log_data))

def log_security_event(event_type: str, message: str, user_id: Optional[str] = None, **kwargs):
    """Log a security-related event"""
    log_event(
        event_type=f"SECURITY_{event_type}",
        message=message,
        level=LogLevel.WARNING if event_type == "FAILED_AUTH" else LogLevel.INFO,
        user_id=user_id,
        **kwargs
    )
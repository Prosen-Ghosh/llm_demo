import logging
import json
import time 
from typing import Any

logger = logging.getLogger("profile-enricher")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')  # We'll emit JSON manually
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_json(**kwargs: Any) -> None:
    # Minimal structured logging; in prod route through structured logger
    entry = {"ts": time.time(), **kwargs}
    logger.info(json.dumps(entry, default=str))

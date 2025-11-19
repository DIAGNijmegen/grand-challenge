import logging
import os
from pathlib import Path

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
SCRIPT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
PARTIALS_PATH = SCRIPT_PATH / "partials"
RESOURCES_PATH = SCRIPT_PATH / "resources"

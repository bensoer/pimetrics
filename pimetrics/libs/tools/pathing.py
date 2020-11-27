import os
from pathlib import Path

PROJECT_ROOT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent.absolute())
TEMP_DIR = "/tmp"
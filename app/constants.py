from pathlib import Path

TOKEN_LIFETIME = 3600
PASSWORD_MIN_LENGTH = 3
DEFAULT_INVESTED_AMOUNT = 0
NAME_MAX_LENGTH = 100
NAME_MIN_LENGTH = 1
BASE_DIR = Path(__file__).parent
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

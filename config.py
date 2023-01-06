from pathlib import Path

# User settings
db_type = 'sqlite'  # postgresql, oracle, .. || sqlite
driver = 'pymysql'  # psycopg2, cx_oracle, ..
db_name = 'vacancy_db'
host = 'localhost'
user = 'root'
password = ''
port = ''

# Auto settings
BASE_DIR = Path(__file__).resolve().parent
JSON_DIR = BASE_DIR / 'json'
if db_type != 'sqlite':
    if not port:
        URL = f"{db_type}+{driver}://{user}:{password}@{host}/{db_name}"
    else:
        URL = f"{db_type}+{driver}://{user}:{password}@{host}:{port}/{db_name}"
else:
    URL = f"{db_type}:///{db_name}"

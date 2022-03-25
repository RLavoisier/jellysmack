import os
from pathlib import Path

db_dir = os.path.join(
    Path(os.path.dirname(__file__)).parent.absolute(), "jellysmack.sqlite"
)
DB_PATH = os.path.abspath(db_dir)

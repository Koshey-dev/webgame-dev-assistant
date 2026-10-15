import os
import sys
import tempfile
from pathlib import Path

# Данные тестов — во временной папке: рабочая база сервера не трогается.
os.environ["WDA_DATA"] = tempfile.mkdtemp(prefix="wda-test-")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

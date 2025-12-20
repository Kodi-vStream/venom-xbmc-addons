import sys
from lib.directories import tests_dir, plugin_dir

def patch_path():
    mock_dir = tests_dir/'lib'/'mock'
    sys.path.insert(1, str(plugin_dir))
    sys.path.insert(1, str(mock_dir))

patch_path()
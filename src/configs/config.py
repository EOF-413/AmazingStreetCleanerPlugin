import os
import json


def get_config_path():
    app_data = os.getenv('APPDATA')
    if app_data is None:
        app_data = os.path.expanduser('~')
    config_dir = os.path.join(app_data, 'EOF413', 'AMT', 'plugins', 'bots', 'ASC')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return os.path.join(config_dir, 'config.json')


KEYS = ['SHIFT', 'CTRL', 'ALT', 'A', 'C', 'D', 'E', 'J', 'K', 'L', 'N', 'Q', 'R', 'S', 'W']

DEFAULT_CONFIG = {
    "HOLD": 1.25,
    "COOLDOWN": 0.75,
    "MIN_MATCH": 0.40
}


def load_config():
    config_path = get_config_path()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            if not config:
                save_config(DEFAULT_CONFIG)
                return DEFAULT_CONFIG.copy()
            for key, val in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = val
            return config
    except (FileNotFoundError, json.JSONDecodeError):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(data):
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

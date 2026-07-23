import os
import json


def get_appdata():
    appdata = os.environ.get('APPDATA')
    if appdata:
        return appdata
    userprofile = os.environ.get('USERPROFILE')
    if userprofile:
        return os.path.join(userprofile, 'AppData', 'Roaming')
    return os.path.expanduser('~')


def get_config_path():
    app_data = get_appdata()
    config_dir = os.path.join(app_data, 'EOF413', 'AMT', 'plugins', 'bots', 'ASC')
    os.makedirs(config_dir, exist_ok=True)
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

from time import sleep
from threading import Thread

import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Listener, Key

from amt_api import log
from src.configs.config import load_config, DEFAULT_CONFIG
from src.backend.matcher import Matcher
from src.backend.screen import get_region
from src.utils.keyboard import press_key, release_all


class App:
    def __init__(self):
        self.matcher = Matcher()
        self.region = get_region()
        self.enabled = False
        self.running = True
        self.loop_thread = None
        self.listener = None
        self.config = load_config()
        if self.config is None:
            self.config = DEFAULT_CONFIG.copy()

    def _log(self, text, color=None):
        log(text, color)

    def _loop(self):
        while self.running:
            if not self.enabled:
                sleep(0.05)
                continue
            try:
                self.config = load_config()
                if self.config is None:
                    self.config = DEFAULT_CONFIG.copy()
                screenshot = ImageGrab.grab(bbox=self.region)
                gray = np.array(screenshot.convert('L'), dtype=np.uint8)

                key, score = self.matcher.process(gray, self.config)

                if key:
                    self._log(f"Удерживается {key} ({score}%)", 'green')
                    press_key(key, self.config["HOLD"])
                else:
                    press_key('E', 0.2)
                    self._log(f"Нет совпадений ({score}%)", 'yellow')

                sleep(self.config["COOLDOWN"])
            except Exception as e:
                self._log(f"Ошибка в цикле: {e}", 'red')
                sleep(0.5)

    def _on_press(self, key):
        try:
            if key == Key.f9:
                self.toggle()
        except Exception:
            pass

    def start_listener(self):
        if self.listener is None or not self.listener.running:
            self.listener = Listener(on_press=self._on_press)
            self.listener.daemon = True
            self.listener.start()

    def start(self):
        if not self.enabled:
            self.enabled = True
            self._log("Запущено", 'green')
            if not self.loop_thread or not self.loop_thread.is_alive():
                self.loop_thread = Thread(target=self._loop, daemon=True)
                self.loop_thread.start()

    def stop(self):
        self.enabled = False
        release_all()
        self._log("Остановлено", 'red')

    def toggle(self):
        if self.enabled:
            self.stop()
        else:
            self.start()

    def cleanup(self):
        self.running = False
        self.enabled = False
        release_all()
        if self.listener and self.listener.running:
            self.listener.stop()

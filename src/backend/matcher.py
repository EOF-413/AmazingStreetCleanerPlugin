import os
import sys
import cv2


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)


class Matcher:
    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self):
        templates = {}
        keys = ['SHIFT', 'CTRL', 'ALT', 'A', 'C', 'D', 'E', 'J', 'K', 'L', 'N', 'Q', 'R', 'S', 'W']

        for key in keys:
            try:
                fpath = resource_path(os.path.join('templates', f'{key}.png'))
                img = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    templates[key] = img
            except Exception:
                pass
        return templates

    def process(self, gray, config=None):
        if config is None:
            config = {}

        best_key = None
        best_score = 0.0

        for key, tmpl in self.templates.items():
            try:
                if tmpl.shape[0] > gray.shape[0] or tmpl.shape[1] > gray.shape[1]:
                    continue

                result = cv2.matchTemplate(gray, tmpl, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                score = max_val

                if score > best_score:
                    best_score = score
                    best_key = key
            except Exception:
                continue

        if best_key is None:
            return None, round(best_score * 100, 1)

        threshold = config.get("MIN_MATCH", 0.40)

        if best_score >= threshold:
            return best_key, round(best_score * 100, 1)
        return None, round(best_score * 100, 1)

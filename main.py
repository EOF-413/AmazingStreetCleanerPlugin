import sys
import traceback
from time import sleep

from amt_api import log
from src.core import App


def main():
    log("Запуск Amazing Street Cleaner...", 'green')
    app = App()
    app.start_listener()
    log("Нажмите F9 для старта/остановки", 'blue')
    log("Готов к работе!", 'green')

    try:
        while app.running:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        app.cleanup()
        log("Amazing Street Cleaner завершён", 'red')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f"Критическая ошибка: {e}", 'red')
        log(traceback.format_exc(), 'red')
        sys.exit(1)

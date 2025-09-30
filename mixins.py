import json
from datetime import datetime


class CritMixin:
    """Миксин для критического урона"""

    def calculate_crit(self, base_damage, crit_chance=0.1):
        import random
        if random.random() < crit_chance:
            return base_damage * 1.5
        return base_damage


class LoggerMixin:
    """Миксин для логирования"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = []

    def add_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log.append(log_entry)
        print(log_entry)


class SilenceMixin:
    """Миксин для эффекта немоты"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_silenced = False

    @property
    def is_silenced(self):
        return self._is_silenced

    def set_silenced(self, value):
        self._is_silenced = value
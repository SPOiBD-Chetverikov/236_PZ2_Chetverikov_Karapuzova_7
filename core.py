from abc import ABC, abstractmethod
from descriptors import BoundedStat
from mixins import LoggerMixin


class Human:
    """Базовый класс для всех персонажей"""

    # Дескрипторы для характеристик
    hp = BoundedStat(0, 1000)
    mp = BoundedStat(0, 500)
    strength = BoundedStat(1, 100)
    agility = BoundedStat(1, 100)
    intellect = BoundedStat(1, 100)

    def __init__(self, name, level=1):
        self._name = name
        self._level = level
        self._hp = 100
        self._mp = 50
        self._strength = 10
        self._agility = 10
        self._intellect = 10

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return f"{self.name} (Lvl {self.level}) - HP: {self.hp}/{self._hp_max if hasattr(self, '_hp_max') else 100}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', level={self.level})"


class Character(Human, ABC):
    """Абстрактный класс для игровых персонажей"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._skills = []
        self._effects = []
        self._cooldowns = {}

        # Увеличиваем характеристики в зависимости от уровня
        self.hp = 100 + (level - 1) * 20
        self.mp = 50 + (level - 1) * 10
        self._hp_max = self.hp
        self._mp_max = self.mp

    @abstractmethod
    def basic_attack(self, target):
        """Базовая атака"""
        pass

    @abstractmethod
    def use_skill(self, skill_index, target):
        """Использование навыка"""
        pass

    def add_skill(self, skill):
        """Добавление навыка"""
        self._skills.append(skill)

    def add_effect(self, effect):
        """Добавление эффекта"""
        self._effects.append(effect)
        effect.apply(self)

    def remove_effect(self, effect):
        """Удаление эффекта"""
        if effect in self._effects:
            effect.remove(self)
            self._effects.remove(effect)

    def process_effects(self):
        """Обработка эффектов в начале хода"""
        for effect in self._effects[:]:
            effect.tick(self)
            if effect.duration <= 0:
                self.remove_effect(effect)

    @property
    def skills(self):
        return self._skills

    @property
    def effects(self):
        return self._effects
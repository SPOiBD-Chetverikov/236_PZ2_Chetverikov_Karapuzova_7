from core import Character
from skills import DamageSkill, HealSkill, BuffSkill
from mixins import SilenceMixin


class Warrior(Character, SilenceMixin):
    """Класс Воина"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        SilenceMixin.__init__(self)

        # Увеличиваем силу
        self.strength = 20 + (level - 1) * 3
        self.agility = 15 + (level - 1) * 2
        self.intellect = 5 + (level - 1) * 1

        # Навыки воина
        self.add_skill(DamageSkill("Удар мечом", 10, 0, 15))
        self.add_skill(DamageSkill("Мощный удар", 25, 2, 30))
        self.add_skill(BuffSkill("Боевой клич", 20, 3, {'strength': 10}, 3))

    def basic_attack(self, target):
        damage = self.strength * 0.8
        target.hp -= damage
        print(f"{self.name} атакует {target.name} и наносит {damage:.1f} урона!")
        return True

    def use_skill(self, skill_index, target):
        if 0 <= skill_index < len(self._skills):
            skill = self._skills[skill_index]
            return skill.execute(self, target)
        return False


class Mage(Character, SilenceMixin):
    """Класс Мага"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        SilenceMixin.__init__(self)

        # Увеличиваем интеллект
        self.strength = 5 + (level - 1) * 1
        self.agility = 10 + (level - 1) * 2
        self.intellect = 25 + (level - 1) * 3

        # Навыки мага
        self.add_skill(DamageSkill("Огненный шар", 15, 0, 20, "magic"))
        self.add_skill(DamageSkill("Ледяная стрела", 20, 1, 25, "magic"))
        from effects import PoisonEffect
        # Можно добавить навык с эффектом яда

    def basic_attack(self, target):
        damage = self.intellect * 0.6
        target.hp -= damage
        print(f"{self.name} атакует {target.name} магией и наносит {damage:.1f} урона!")
        return True

    def use_skill(self, skill_index, target):
        if 0 <= skill_index < len(self._skills):
            skill = self._skills[skill_index]
            return skill.execute(self, target)
        return False


class Healer(Character, SilenceMixin):
    """Класс Лекаря"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        SilenceMixin.__init__(self)

        # Сбалансированные характеристики
        self.strength = 8 + (level - 1) * 1
        self.agility = 12 + (level - 1) * 2
        self.intellect = 20 + (level - 1) * 3

        # Навыки лекаря
        self.add_skill(HealSkill("Лечение", 15, 0, 20))
        self.add_skill(HealSkill("Большое лечение", 30, 2, 40))
        from effects import RegenerationEffect
        # Можно добавить навык с регенерацией

    def basic_attack(self, target):
        damage = self.intellect * 0.4
        target.hp -= damage
        print(f"{self.name} атакует {target.name} и наносит {damage:.1f} урона!")
        return True

    def use_skill(self, skill_index, target):
        if 0 <= skill_index < len(self._skills):
            skill = self._skills[skill_index]
            return skill.execute(self, target)
        return False


class Boss(Character):
    """Класс Босса с фазами"""

    def __init__(self, name, level=1):
        super().__init__(name, level)

        # Мощные характеристики босса
        self.hp = 300 + (level - 1) * 50
        self.mp = 200 + (level - 1) * 30
        self.strength = 30 + (level - 1) * 5
        self.agility = 20 + (level - 1) * 3
        self.intellect = 25 + (level - 1) * 4

        self._hp_max = self.hp
        self._mp_max = self.mp

        # Стратегии босса
        self._strategies = {
            'normal': self._normal_strategy,
            'enraged': self._enraged_strategy,
            'desperate': self._desperate_strategy
        }
        self._current_strategy = 'normal'

    @property
    def phase(self):
        """Определение текущей фазы босса"""
        hp_percent = self.hp / self._hp_max

        if hp_percent > 0.6:
            return 'normal'
        elif hp_percent > 0.3:
            return 'enraged'
        else:
            return 'desperate'

    def basic_attack(self, target):
        damage = self.strength * 1.0
        target.hp -= damage
        print(f"{self.name} атакует {target.name} и наносит {damage:.1f} урона!")
        return True

    def use_skill(self, skill_index, target):
        # Босс автоматически выбирает стратегию
        self._current_strategy = self.phase
        strategy = self._strategies[self._current_strategy]
        return strategy(target)

    def _normal_strategy(self, target):
        """Нормальная стратегия - базовая атака"""
        return self.basic_attack(target)

    def _enraged_strategy(self, target):
        """Разъяренная стратегия - усиленные атаки"""
        damage = self.strength * 1.5
        target.hp -= damage
        print(f"{self.name} в ярости атакует {target.name} и наносит {damage:.1f} урона!")
        return True

    def _desperate_strategy(self, target):
        """Отчаянная стратегия - атака с эффектом"""
        damage = self.strength * 1.2
        target.hp -= damage

        # Добавляем эффект яда
        from effects import PoisonEffect
        poison = PoisonEffect(3, 5)
        target.add_effect(poison)

        print(f"{self.name} в отчаянии атакует {target.name}, наносит {damage:.1f} урона и отравляет его!")
        return True
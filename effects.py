class Effect:
    """Базовый класс эффектов"""

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def apply(self, target):
        """Применение эффекта"""
        pass

    def remove(self, target):
        """Удаление эффекта"""
        pass

    def tick(self, target):
        """Действие эффекта в начале хода"""
        self.duration -= 1

    def __str__(self):
        return f"{self.name} ({self.duration} ходов)"


class PoisonEffect(Effect):
    """Эффект яда"""

    def __init__(self, duration, damage_per_turn):
        super().__init__("Яд", duration)
        self.damage_per_turn = damage_per_turn

    def tick(self, target):
        super().tick(target)
        target.hp -= self.damage_per_turn
        print(f"{target.name} получает {self.damage_per_turn} урона от яда!")


class RegenerationEffect(Effect):
    """Эффект регенерации"""

    def __init__(self, duration, heal_per_turn):
        super().__init__("Регенерация", duration)
        self.heal_per_turn = heal_per_turn

    def tick(self, target):
        super().tick(target)
        target.hp = min(target.hp + self.heal_per_turn, target._hp_max)
        print(f"{target.name} восстанавливает {self.heal_per_turn} HP от регенерации!")


class StatBuffEffect(Effect):
    """Эффект усиления характеристики"""

    def __init__(self, name, duration, stat_bonus):
        super().__init__(name, duration)
        self.stat_bonus = stat_bonus
        self.original_stats = {}

    def apply(self, target):
        self.original_stats = {
            'strength': target.strength,
            'agility': target.agility,
            'intellect': target.intellect
        }

        target.strength += self.stat_bonus.get('strength', 0)
        target.agility += self.stat_bonus.get('agility', 0)
        target.intellect += self.stat_bonus.get('intellect', 0)

    def remove(self, target):
        target.strength = self.original_stats.get('strength', target.strength)
        target.agility = self.original_stats.get('agility', target.agility)
        target.intellect = self.original_stats.get('intellect', target.intellect)


class SilenceEffect(Effect):
    """Эффект немоты"""

    def __init__(self, duration):
        super().__init__("Немота", duration)

    def apply(self, target):
        if hasattr(target, 'set_silenced'):
            target.set_silenced(True)

    def remove(self, target):
        if hasattr(target, 'set_silenced'):
            target.set_silenced(False)
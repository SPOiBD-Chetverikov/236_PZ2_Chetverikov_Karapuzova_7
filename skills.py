from abc import ABC, abstractmethod
from mixins import CritMixin


class Skill(ABC, CritMixin):
    """Абстрактный класс для навыков"""

    def __init__(self, name, mp_cost, cooldown):
        self.name = name
        self.mp_cost = mp_cost
        self.cooldown = cooldown
        self.current_cooldown = 0

    @abstractmethod
    def execute(self, caster, target):
        """Выполнение навыка"""
        pass

    def is_available(self, caster):
        """Проверка доступности навыка"""
        return (caster.mp >= self.mp_cost and
                self.current_cooldown == 0 and
                not (hasattr(caster, 'is_silenced') and caster.is_silenced))

    def start_cooldown(self):
        """Начало перезарядки"""
        self.current_cooldown = self.cooldown

    def reduce_cooldown(self):
        """Уменьшение перезарядки"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def __str__(self):
        return f"{self.name} (MP: {self.mp_cost}, CD: {self.cooldown})"


class DamageSkill(Skill):
    """Навык нанесения урона"""

    def __init__(self, name, mp_cost, cooldown, base_damage, damage_type="physical"):
        super().__init__(name, mp_cost, cooldown)
        self.base_damage = base_damage
        self.damage_type = damage_type

    def execute(self, caster, target):
        if not self.is_available(caster):
            return False

        caster.mp -= self.mp_cost
        damage = self.calculate_crit(self.base_damage + caster.strength * 0.5)
        target.hp -= damage
        self.start_cooldown()

        print(f"{caster.name} использует {self.name} на {target.name} и наносит {damage:.1f} урона!")
        return True


class HealSkill(Skill):
    """Навык лечения"""

    def __init__(self, name, mp_cost, cooldown, base_heal):
        super().__init__(name, mp_cost, cooldown)
        self.base_heal = base_heal

    def execute(self, caster, target):
        if not self.is_available(caster):
            return False

        caster.mp -= self.mp_cost
        heal_amount = self.base_heal + caster.intellect * 0.8
        target.hp = min(target.hp + heal_amount, target._hp_max)
        self.start_cooldown()

        print(f"{caster.name} использует {self.name} на {target.name} и восстанавливает {heal_amount:.1f} HP!")
        return True


class BuffSkill(Skill):
    """Навык усиления"""

    def __init__(self, name, mp_cost, cooldown, stat_bonus, duration):
        super().__init__(name, mp_cost, cooldown)
        self.stat_bonus = stat_bonus
        self.duration = duration

    def execute(self, caster, target):
        if not self.is_available(caster):
            return False

        caster.mp -= self.mp_cost
        # Создаем эффект бафа
        from effects import StatBuffEffect
        effect = StatBuffEffect(f"Buff_{self.name}", self.duration, self.stat_bonus)
        target.add_effect(effect)
        self.start_cooldown()

        print(f"{caster.name} использует {self.name} на {target.name}!")
        return True
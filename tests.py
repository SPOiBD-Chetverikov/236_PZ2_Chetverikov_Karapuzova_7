import unittest
from characters import Warrior, Mage, Boss
from skills import DamageSkill
from effects import PoisonEffect
from battle import Battle


class TestGame(unittest.TestCase):

    def test_warrior_creation(self):
        """Тест создания воина"""
        warrior = Warrior("Тестовый воин")
        self.assertEqual(warrior.name, "Тестовый воин")
        self.assertTrue(warrior.is_alive)
        self.assertGreater(warrior.strength, 0)

    def test_boss_phases(self):
        """Тест фаз босса"""
        boss = Boss("Тестовый босс")

        # Нормальная фаза
        self.assertEqual(boss.phase, 'normal')

        # Разъяренная фаза
        boss.hp = boss._hp_max * 0.5
        self.assertEqual(boss.phase, 'enraged')

        # Отчаянная фаза
        boss.hp = boss._hp_max * 0.2
        self.assertEqual(boss.phase, 'desperate')

    def test_damage_skill(self):
        """Тест навыка урона"""
        warrior = Warrior("Воин")
        target = Warrior("Цель")

        initial_hp = target.hp
        skill = DamageSkill("Тестовая атака", 10, 1, 20)

        if skill.is_available(warrior):
            skill.execute(warrior, target)
            self.assertLess(target.hp, initial_hp)

    def test_poison_effect(self):
        """Тест эффекта яда"""
        character = Warrior("Тест")
        poison = PoisonEffect(3, 5)

        initial_hp = character.hp
        character.add_effect(poison)
        character.process_effects()

        self.assertLess(character.hp, initial_hp)
        self.assertEqual(poison.duration, 2)


if __name__ == "__main__":
    unittest.main()
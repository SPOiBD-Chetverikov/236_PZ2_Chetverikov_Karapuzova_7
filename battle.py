import random
import json
from datetime import datetime
from mixins import LoggerMixin  # Добавляем импорт LoggerMixin


class TurnOrder:
    """Итератор для определения порядка ходов"""

    def __init__(self, characters):
        self.characters = sorted(characters, key=lambda x: x.agility, reverse=True)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.characters):
            self.index = 0
            raise StopIteration

        character = self.characters[self.index]
        self.index += 1
        return character


class Battle(LoggerMixin):  # Теперь LoggerMixin доступен
    """Класс управления боем"""

    def __init__(self, party, boss, seed=None):
        super().__init__()
        self.party = party
        self.boss = boss
        self.round = 0
        self.is_active = True

        # Установка seed для повторяемости
        if seed is not None:
            random.seed(seed)

        self.add_log(f"Бой начинается! Пати: {[char.name for char in party]} против Босса: {boss.name}")

    def start_battle(self):
        """Запуск боя"""
        while self.is_active:
            self.round += 1
            self.add_log(f"\n--- Раунд {self.round} ---")

            # Создание порядка ходов
            all_characters = [char for char in self.party + [self.boss] if char.is_alive]
            if not all_characters:
                break

            turn_order = TurnOrder(all_characters)

            # Обработка ходов
            for character in turn_order:
                if not character.is_alive:
                    continue

                self._process_turn(character)

                # Проверка условий окончания боя
                if not self.boss.is_alive:
                    self.add_log(f"Пати победила босса {self.boss.name}!")
                    self.is_active = False
                    return "party_win"

                if all(not char.is_alive for char in self.party):
                    self.add_log(f"Босс {self.boss.name} победил пати!")
                    self.is_active = False
                    return "boss_win"

    def _process_turn(self, character):
        """Обработка хода персонажа"""
        self.add_log(f"Ход {character.name} (HP: {character.hp:.1f}, MP: {character.mp:.1f})")

        # Обработка эффектов
        character.process_effects()

        if not character.is_alive:
            self.add_log(f"{character.name} мёртв и пропускает ход")
            return

        # Уменьшение перезарядки навыков
        for skill in character.skills:
            skill.reduce_cooldown()

        # Логика хода в зависимости от типа персонажа
        if character in self.party:
            self._party_member_turn(character)
        else:
            self._boss_turn(character)

    def _party_member_turn(self, character):
        """Ход члена пати (упрощенная логика)"""
        # Простая ИИ логика для демонстрации
        available_skills = [skill for skill in character.skills if skill.is_available(character)]

        if available_skills and random.random() < 0.7:
            # Использование случайного навыка
            skill = random.choice(available_skills)
            target = self.boss
            skill.execute(character, target)
        else:
            # Базовая атака
            character.basic_attack(self.boss)

    def _boss_turn(self, character):
        """Ход босса"""
        # Выбор живой цели из пати
        alive_party = [char for char in self.party if char.is_alive]
        if not alive_party:
            return

        target = random.choice(alive_party)
        character.use_skill(0, target)

    def save_state(self, filename):
        """Сохранение состояния боя в JSON"""
        state = {
            'round': self.round,
            'party': [
                {
                    'name': char.name,
                    'class': char.__class__.__name__,
                    'hp': char.hp,
                    'mp': char.mp,
                    'level': char.level
                } for char in self.party
            ],
            'boss': {
                'name': self.boss.name,
                'hp': self.boss.hp,
                'mp': self.boss.mp,
                'level': self.boss.level
            },
            'log': self.log
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

        self.add_log(f"Состояние боя сохранено в {filename}")
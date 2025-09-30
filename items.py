class Item:
    """Базовый класс предметов"""

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, target):
        """Использование предмета"""
        pass

    def __str__(self):
        return f"{self.name}: {self.description}"


class HealthPotion(Item):
    """Зелье здоровья"""

    def __init__(self):
        super().__init__("Зелье здоровья", "Восстанавливает 50 HP")

    def use(self, target):
        if target.is_alive:
            heal_amount = 50
            old_hp = target.hp
            target.hp = min(target.hp + heal_amount, target._hp_max)
            actual_heal = target.hp - old_hp
            print(f"{target.name} использует {self.name} и восстанавливает {actual_heal} HP!")
            return True
        return False


class ManaPotion(Item):
    """Зелье маны"""

    def __init__(self):
        super().__init__("Зелье маны", "Восстанавливает 30 MP")

    def use(self, target):
        if target.is_alive:
            mana_amount = 30
            old_mp = target.mp
            target.mp = min(target.mp + mana_amount, target._mp_max)
            actual_mana = target.mp - old_mp
            print(f"{target.name} использует {self.name} и восстанавливает {actual_mana} MP!")
            return True
        return False


class Inventory:
    """Инвентарь персонажа"""

    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Добавление предмета в инвентарь"""
        self.items.append(item)

    def remove_item(self, item):
        """Удаление предмета из инвентаря"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def use_item(self, item_index, target):
        """Использование предмета по индексу"""
        if 0 <= item_index < len(self.items):
            item = self.items[item_index]
            if item.use(target):
                self.remove_item(item)
                return True
        return False

    def __str__(self):
        if not self.items:
            return "Инвентарь пуст"
        return "\n".join([f"{i}: {item}" for i, item in enumerate(self.items)])
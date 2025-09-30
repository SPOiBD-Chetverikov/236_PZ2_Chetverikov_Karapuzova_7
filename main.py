import random
from characters import Warrior, Mage, Healer, Boss
from battle import Battle
from items import HealthPotion, ManaPotion, Inventory


def create_party():
    """Создание пати персонажей"""
    party = []

    print("Создание пати:")
    classes = {
        '1': ('Воин', Warrior),
        '2': ('Маг', Mage),
        '3': ('Лекарь', Healer)
    }

    for i in range(3):
        print(f"\nПерсонаж {i + 1}:")
        for key, (name, _) in classes.items():
            print(f"{key}. {name}")

        while True:
            choice = input("Выберите класс: ")
            if choice in classes:
                name = input("Введите имя персонажа: ")
                char_class = classes[choice][1]
                party.append(char_class(name))
                break
            else:
                print("Неверный выбор!")

    return party


def main():
    """Основная функция игры"""
    print("=== Мини-игра 'Пати против Босса' ===")

    # Настройка боя
    seed = input("Введите seed для случайной генерации (или оставьте пустым): ")
    if seed:
        seed = int(seed)

    # Создание пати
    party = create_party()

    # Создание босса
    boss_level = 3
    boss = Boss("Дракон", boss_level)

    # Добавление предметов в инвентарь
    for char in party:
        char.inventory = Inventory()
        char.inventory.add_item(HealthPotion())
        char.inventory.add_item(ManaPotion())

    # Запуск боя
    battle = Battle(party, boss, seed)

    try:
        result = battle.start_battle()

        if result == "party_win":
            print("\n🎉 Поздравляем! Вы победили босса!")
        else:
            print("\n💀 К сожалению, босс оказался сильнее...")

        # Сохранение лога боя
        battle.save_state("battle_log.json")

    except KeyboardInterrupt:
        print("\nБой прерван пользователем")
        battle.save_state("battle_interrupted.json")


if __name__ == "__main__":
    main()
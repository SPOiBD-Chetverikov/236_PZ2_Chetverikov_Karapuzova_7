class BoundedStat:
    """Дескриптор для ограничения значений характеристик"""

    def __init__(self, min_val=0, max_val=100):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, self.min_val)

    def __set__(self, instance, value):
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"{self.name[1:]} must be between {self.min_val} and {self.max_val}")
        setattr(instance, self.name, value)
ERAS = [
    {"id": 1, "name": "Egito Antigo", "period": "2500 a.C.", "focus": "Danas"},
    {"id": 2, "name": "Grecia Antiga", "period": "seculo V a.C.", "focus": "Nardi"},
    {"id": 3, "name": "Roma Antiga", "period": "100 d.C.", "focus": "Arto"},
    {"id": 4, "name": "Europa Medieval", "period": "seculo XIII", "focus": "Danas"},
    {"id": 5, "name": "Grandes Navegacoes", "period": "seculo XVI", "focus": "Nardi"},
    {"id": 6, "name": "Velho Oeste", "period": "seculo XIX", "focus": "Henn"},
    {"id": 7, "name": "Revolucao Industrial", "period": "seculo XIX", "focus": "Arto"},
    {"id": 8, "name": "Anos 1920", "period": "1920-1929", "focus": "Danas e Nardi"},
    {"id": 9, "name": "Anos 1980", "period": "1980-1989", "focus": "Arto"},
    {"id": 10, "name": "Museu Original", "period": "presente", "focus": "Todos"},
]


class Campaign:
    def __init__(self):
        self.current_level = 1
        self.unlocked_level = 1
        self.fragments = []

    def complete_level(self, level_id):
        if level_id not in self.fragments:
            self.fragments.append(level_id)
        self.unlocked_level = min(10, max(self.unlocked_level, level_id + 1))
        self.current_level = self.unlocked_level

    def is_unlocked(self, level_id):
        return level_id <= self.unlocked_level

    def reset(self):
        self.current_level = 1
        self.unlocked_level = 1
        self.fragments.clear()

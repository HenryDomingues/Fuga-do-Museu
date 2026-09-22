INTRO_LINES = [
    "Certo dia...",
    "Quatro amigos visitaram um dos maiores museus do pais.",
    "O que parecia ser apenas uma visita...",
    "...acabaria se tornando uma viagem pela propria historia.",
]

EGYPT_LINES = [
    "EXPOSICAO: A HISTORIA DA HUMANIDADE",
    "Danas encontrou uma area restrita atras da galeria.",
    "Um artefato desconhecido pulsava entre os objetos.",
    "Ao toca-lo, o museu desapareceu.",
    "EGITO ANTIGO - 2500 a.C.",
]


class Dialogue:
    def __init__(self, lines):
        self.lines = lines
        self.index = 0

    @property
    def finished(self):
        return self.index >= len(self.lines)

    @property
    def current(self):
        return "" if self.finished else self.lines[self.index]

    def advance(self):
        if not self.finished:
            self.index += 1
        return self.finished

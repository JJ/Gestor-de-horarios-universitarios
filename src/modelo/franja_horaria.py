from dataclasses import dataclass
from datetime import time
from enum import Enum, auto


class DiaSemana(Enum):
    LUNES = auto()
    MARTES = auto()
    MIERCOLES = auto()
    JUEVES = auto()
    VIERNES = auto()


@dataclass(frozen=True)
class FranjaHoraria:
    dia: DiaSemana
    inicio: time
    fin: time

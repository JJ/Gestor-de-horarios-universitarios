from dataclasses import dataclass

from .clase import Clase


@dataclass(eq=False)
class HorarioEstudiante:
    clases: set[Clase]

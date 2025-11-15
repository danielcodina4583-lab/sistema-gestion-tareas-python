from abc import ABC, abstractmethod
from models.tarea import Tarea, Prioridad

class PrioridadStrategy(ABC):
    @abstractmethod
    def calcular_prioridad(self, tarea: Tarea) -> Prioridad:
        pass
    
    @abstractmethod
    def get_nombre(self) -> str:
        pass
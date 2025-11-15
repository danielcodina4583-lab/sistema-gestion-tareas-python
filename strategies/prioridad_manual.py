from .prioridad_strategy import PrioridadStrategy
from models.tarea import Tarea, Prioridad

class PrioridadManualStrategy(PrioridadStrategy):
    def calcular_prioridad(self, tarea: Tarea) -> Prioridad:
        return tarea.prioridad if tarea.prioridad else Prioridad.MEDIA
    
    def get_nombre(self) -> str:
        return "Prioridad Manual"
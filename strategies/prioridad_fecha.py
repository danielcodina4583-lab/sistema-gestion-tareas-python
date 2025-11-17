from .prioridad_strategy import PrioridadStrategy
from models.tarea import Tarea, Prioridad
from datetime import datetime

class PrioridadFechaStrategy(PrioridadStrategy):
    def calcular_prioridad(self, tarea: Tarea) -> Prioridad:
        if not tarea.fecha_limite:
            return Prioridad.BAJA
            
        ahora = datetime.now()
        diferencia = tarea.fecha_limite - ahora
        dias_restantes = diferencia.days
        horas_restantes = diferencia.total_seconds() / 3600
        
        if horas_restantes <= 24:  
            return Prioridad.ALTA
        elif dias_restantes <= 2: 
            return Prioridad.MEDIA
        else:
            return Prioridad.BAJA
        
    def get_nombre(self) -> str:  
        return "Estrategia por Fecha"
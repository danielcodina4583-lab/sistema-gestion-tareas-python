from .prioridad_strategy import PrioridadStrategy
from models.tarea import Tarea, Prioridad

class PrioridadCategoriaStrategy(PrioridadStrategy):
    def calcular_prioridad(self, tarea: Tarea) -> Prioridad:
        categorias_altas = ['universidad', 'trabajo', 'examen', 'urgente']
        categorias_medias = ['estudio', 'proyecto', 'personal']
        
        categoria = tarea.categoria.lower()
        
        if any(cat in categoria for cat in categorias_altas):
            return Prioridad.ALTA
        elif any(cat in categoria for cat in categorias_medias):
            return Prioridad.MEDIA
        else:
            return Prioridad.BAJA
    
    def get_nombre(self) -> str:
        return "Prioridad por Categoría"
from abc import ABC, abstractmethod
from typing import List
from models.tarea import Tarea

class PersistenceStrategy(ABC):
    
    @abstractmethod
    def guardar_tareas(self, tareas: List[Tarea], archivo: str) -> bool:
        pass
    
    @abstractmethod
    def cargar_tareas(self, archivo: str) -> List[Tarea]:
        pass
    
    @abstractmethod
    def get_nombre(self) -> str:
        pass

class PersistenceManager:
    
    def __init__(self, estrategia: PersistenceStrategy = None):
        self.estrategia = estrategia
    
    def establecer_estrategia(self, estrategia: PersistenceStrategy):
        self.estrategia = estrategia
    
    def guardar_tareas(self, tareas: List[Tarea], archivo: str) -> bool:
        if not self.estrategia:
            raise ValueError("No se ha establecido una estrategia de persistencia")
        return self.estrategia.guardar_tareas(tareas, archivo)
    
    def cargar_tareas(self, archivo: str) -> List[Tarea]:
        if not self.estrategia:
            raise ValueError("No se ha establecido una estrategia de persistencia")
        return self.estrategia.cargar_tareas(archivo)
    
    def get_estrategias_disponibles(self):
        from .json_persistence import JSONPersistence
        from .csv_persistence import CSVPersistence
        return [
            JSONPersistence(),
            CSVPersistence()
        ]
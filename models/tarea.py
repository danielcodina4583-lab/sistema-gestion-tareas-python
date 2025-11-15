from datetime import datetime
from enum import Enum

class EstadoTarea(Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"

class Prioridad(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

class Tarea:
    def __init__(self, titulo, descripcion="", categoria="general", 
                 fecha_limite=None, estado=EstadoTarea.PENDIENTE, prioridad=Prioridad.MEDIA):
        self.id = id(self)
        self.titulo = titulo
        self.descripcion = descripcion
        self.categoria = categoria
        self.fecha_limite = fecha_limite
        self.estado = estado
        self.prioridad = prioridad
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
    
    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.fecha_actualizacion = datetime.now()
    
    def actualizar_prioridad(self, nueva_prioridad):
        self.prioridad = nueva_prioridad
        self.fecha_actualizacion = datetime.now()
    
    def __str__(self):
        return f"{self.titulo} - {self.estado.value} - {self.prioridad.value}"
    
    def __repr__(self):
        return f"Tarea('{self.titulo}', '{self.estado.value}')"
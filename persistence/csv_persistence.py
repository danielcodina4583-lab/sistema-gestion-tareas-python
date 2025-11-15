import csv
from typing import List
from datetime import datetime
from models.tarea import Tarea, EstadoTarea, Prioridad
from .persistence_manager import PersistenceStrategy

class CSVPersistence(PersistenceStrategy):
    
    def guardar_tareas(self, tareas: List[Tarea], archivo: str) -> bool:
        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'id', 'titulo', 'descripcion', 'categoria', 
                    'fecha_limite', 'estado', 'prioridad',
                    'fecha_creacion', 'fecha_actualizacion'
                ])
                
                for tarea in tareas:
                    writer.writerow([
                        tarea.id,
                        tarea.titulo,
                        tarea.descripcion,
                        tarea.categoria,
                        tarea.fecha_limite.isoformat() if tarea.fecha_limite else '',
                        tarea.estado.value,
                        tarea.prioridad.value,
                        tarea.fecha_creacion.isoformat(),
                        tarea.fecha_actualizacion.isoformat()
                    ])
            
            return True
            
        except Exception as e:
            print(f"Error guardando CSV: {e}")
            return False
    
    def cargar_tareas(self, archivo: str) -> List[Tarea]:
        try:
            tareas = []
            with open(archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    tarea = Tarea(
                        titulo=fila['titulo'],
                        descripcion=fila['descripcion'],
                        categoria=fila['categoria'],
                        fecha_limite=datetime.fromisoformat(fila['fecha_limite']) if fila['fecha_limite'] else None,
                        estado=EstadoTarea(fila['estado']),
                        prioridad=Prioridad(fila['prioridad'])
                    )
                    tarea.id = int(fila['id'])
                    tarea.fecha_creacion = datetime.fromisoformat(fila['fecha_creacion'])
                    tarea.fecha_actualizacion = datetime.fromisoformat(fila['fecha_actualizacion'])
                    tareas.append(tarea)
            
            return tareas
            
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error cargando CSV: {e}")
            return []
    
    def get_nombre(self) -> str:
        return "CSV"
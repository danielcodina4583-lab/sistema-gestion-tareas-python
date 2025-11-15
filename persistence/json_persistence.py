import json
from typing import List
from datetime import datetime
from models.tarea import Tarea, EstadoTarea, Prioridad
from .persistence_manager import PersistenceStrategy

class JSONPersistence(PersistenceStrategy):
    
    def guardar_tareas(self, tareas: List[Tarea], archivo: str) -> bool:
        try:
            datos_tareas = []
            for tarea in tareas:
                tarea_dict = {
                    'id': tarea.id,
                    'titulo': tarea.titulo,
                    'descripcion': tarea.descripcion,
                    'categoria': tarea.categoria,
                    'fecha_limite': tarea.fecha_limite.isoformat() if tarea.fecha_limite else None,
                    'estado': tarea.estado.value,
                    'prioridad': tarea.prioridad.value,
                    'fecha_creacion': tarea.fecha_creacion.isoformat(),
                    'fecha_actualizacion': tarea.fecha_actualizacion.isoformat()
                }
                datos_tareas.append(tarea_dict)
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_tareas, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error guardando JSON: {e}")
            return False
    
    def cargar_tareas(self, archivo: str) -> List[Tarea]:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos_tareas = json.load(f)
            
            tareas = []
            for datos in datos_tareas:
                tarea = Tarea(
                    titulo=datos['titulo'],
                    descripcion=datos['descripcion'],
                    categoria=datos['categoria'],
                    fecha_limite=datetime.fromisoformat(datos['fecha_limite']) if datos['fecha_limite'] else None,
                    estado=EstadoTarea(datos['estado']),
                    prioridad=Prioridad(datos['prioridad'])
                )
                tarea.id = datos['id']
                tarea.fecha_creacion = datetime.fromisoformat(datos['fecha_creacion'])
                tarea.fecha_actualizacion = datetime.fromisoformat(datos['fecha_actualizacion'])
                tareas.append(tarea)
            
            return tareas
            
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error cargando JSON: {e}")
            return []
    
    def get_nombre(self) -> str:
        return "JSON"
from models.tarea import Tarea, EstadoTarea, Prioridad
from strategies.prioridad_strategy import PrioridadStrategy
from strategies.prioridad_fecha import PrioridadFechaStrategy
from typing import List, Optional
from datetime import datetime
from persistence.persistence_manager import PersistenceManager
from persistence.json_persistence import JSONPersistence

class GestorTareas:
    def __init__(self):
        self.tareas: List[Tarea] = []
        self.contador_id = 1
        self.estrategia_prioridad: PrioridadStrategy = PrioridadFechaStrategy()
        self.persistence_manager = PersistenceManager(JSONPersistence())
    
    def crear_tarea(self, titulo: str, descripcion: str = "", categoria: str = "general",
                   fecha_limite: Optional[datetime] = None, prioridad: Prioridad = Prioridad.MEDIA) -> Tarea:
        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            categoria=categoria,
            fecha_limite=fecha_limite,
            prioridad=prioridad
        )
        tarea.id = self.contador_id
        self.contador_id += 1
        self.tareas.append(tarea)
        return tarea
    
    def obtener_todas_tareas(self) -> List[Tarea]:
        return self.tareas.copy()
    
    def obtener_tarea_por_id(self, id_tarea: int) -> Optional[Tarea]:
        for tarea in self.tareas:
            if tarea.id == id_tarea:
                return tarea
        return None
    
    def actualizar_tarea(self, id_tarea: int, **kwargs) -> bool:
        tarea = self.obtener_tarea_por_id(id_tarea)
        if not tarea:
            return False
        
        campos_permitidos = ['titulo', 'descripcion', 'categoria', 'fecha_limite', 'estado', 'prioridad']
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                setattr(tarea, campo, valor)
        
        tarea.fecha_actualizacion = datetime.now()
        return True
    
    def eliminar_tarea(self, id_tarea: int) -> bool:
        tarea = self.obtener_tarea_por_id(id_tarea)
        if tarea:
            self.tareas.remove(tarea)
            return True
        return False
    
    def filtrar_por_estado(self, estado: EstadoTarea) -> List[Tarea]:
        return [tarea for tarea in self.tareas if tarea.estado == estado]
    
    def filtrar_por_categoria(self, categoria: str) -> List[Tarea]:
        return [tarea for tarea in self.tareas if tarea.categoria.lower() == categoria.lower()]
    
    def filtrar_por_prioridad(self, prioridad: Prioridad) -> List[Tarea]:
        return [tarea for tarea in self.tareas if tarea.prioridad == prioridad]
    
    def filtrar_por_fecha_limite(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Tarea]:
        return [tarea for tarea in self.tareas 
                if tarea.fecha_limite and fecha_inicio <= tarea.fecha_limite <= fecha_fin]
    
    def buscar_por_texto(self, texto: str) -> List[Tarea]:
        texto = texto.lower()
        return [tarea for tarea in self.tareas 
                if texto in tarea.titulo.lower() or texto in tarea.descripcion.lower()]
    
    def ordenar_por_fecha_creacion(self, ascendente: bool = True) -> List[Tarea]:
        return sorted(self.tareas, 
                     key=lambda x: x.fecha_creacion, 
                     reverse=not ascendente)
    
    def ordenar_por_fecha_limite(self, ascendente: bool = True) -> List[Tarea]:
        return sorted(self.tareas, 
                     key=lambda x: x.fecha_limite or datetime.max, 
                     reverse=not ascendente)
    
    def ordenar_por_prioridad(self) -> List[Tarea]:
        orden_prioridad = {Prioridad.ALTA: 1, Prioridad.MEDIA: 2, Prioridad.BAJA: 3}
        return sorted(self.tareas, 
                     key=lambda x: orden_prioridad.get(x.prioridad, 4))
    
    def ordenar_por_titulo(self, ascendente: bool = True) -> List[Tarea]:
        return sorted(self.tareas, 
                     key=lambda x: x.titulo.lower(), 
                     reverse=not ascendente)
    
    def ordenar_por_estado(self) -> List[Tarea]:
        orden_estado = {EstadoTarea.COMPLETADA: 1, EstadoTarea.EN_PROGRESO: 2, EstadoTarea.PENDIENTE: 3}
        return sorted(self.tareas, 
                     key=lambda x: orden_estado.get(x.estado, 4))
    
    def obtener_estadisticas(self) -> dict:
        total = len(self.tareas)
        completadas = len(self.filtrar_por_estado(EstadoTarea.COMPLETADA))
        pendientes = len(self.filtrar_por_estado(EstadoTarea.PENDIENTE))
        en_progreso = len(self.filtrar_por_estado(EstadoTarea.EN_PROGRESO))
        
        return {
            'total': total,
            'completadas': completadas,
            'pendientes': pendientes,
            'en_progreso': en_progreso,
            'porcentaje_completadas': (completadas / total * 100) if total > 0 else 0
        }
    
    def obtener_tareas_vencidas(self) -> List[Tarea]:
        ahora = datetime.now()
        return [tarea for tarea in self.tareas 
                if tarea.fecha_limite and tarea.fecha_limite < ahora 
                and tarea.estado != EstadoTarea.COMPLETADA]
    
    def limpiar_tareas_completadas(self) -> int:
        cantidad_inicial = len(self.tareas)
        self.tareas = [tarea for tarea in self.tareas if tarea.estado != EstadoTarea.COMPLETADA]
        return cantidad_inicial - len(self.tareas)
    
    def establecer_estrategia_prioridad(self, estrategia: PrioridadStrategy):
        self.estrategia_prioridad = estrategia

    def obtener_estrategias_disponibles(self) -> List[PrioridadStrategy]:
        from strategies.prioridad_fecha import PrioridadFechaStrategy
        from strategies.prioridad_categoria import PrioridadCategoriaStrategy
        from strategies.prioridad_manual import PrioridadManualStrategy
        
        return [
            PrioridadFechaStrategy(),
            PrioridadCategoriaStrategy(), 
            PrioridadManualStrategy()
        ]

    def aplicar_prioridad_inteligente(self, id_tarea: int = None) -> bool:
        if id_tarea:
            tarea = self.obtener_tarea_por_id(id_tarea)
            if tarea:
                nueva_prioridad = self.estrategia_prioridad.calcular_prioridad(tarea)
                tarea.prioridad = nueva_prioridad
                return True
            return False
        else:
            for tarea in self.tareas:
                nueva_prioridad = self.estrategia_prioridad.calcular_prioridad(tarea)
                tarea.prioridad = nueva_prioridad
            return True

    
    def guardar_tareas(self, archivo: str = "tareas.json") -> bool:
        return self.persistence_manager.guardar_tareas(self.tareas, archivo)


    def cargar_tareas(self, archivo: str = "tareas.json") -> bool:
        tareas_cargadas = self.persistence_manager.cargar_tareas(archivo)
        if tareas_cargadas:
            self.tareas = tareas_cargadas
            if self.tareas:
                self.contador_id = max(tarea.id for tarea in self.tareas) + 1
            return True
        return False

    def establecer_persistencia(self, tipo: str):
        if tipo.lower() == 'json':
            self.persistence_manager.establecer_estrategia(JSONPersistence())
        elif tipo.lower() == 'csv':
            from persistence.csv_persistence import CSVPersistence
            self.persistence_manager.establecer_estrategia(CSVPersistence())
        else:
            raise ValueError(f"Tipo de persistencia no soportado: {tipo}")

    def obtener_estrategias_persistencia(self):
        return self.persistence_manager.get_estrategias_disponibles()
# Sistema de Gestión de Tareas Académicas y Personales con Prioridades Inteligentes

##  Información del Proyecto

**Fecha de Entrega:** 18 de Noviembre 2025  
**Estado:** Funcionalidad completa implementada  
**Repositorio:** https://github.com/danielcodina4583-lab/sistema-gestion-tareas-python/tree/main  
**Materia:** Diseño De Software - Ingeniería de Software

##  Integrantes del Proyecto
| Nombre | Rol |
|--------|-----|
| **Daniel De Jesus Codina Ortiz** | Desarrollo del backend, estrategias de priorización y documentación técnica |
| **Ricardo Jose Valiente** | Desarrollo de la interfaz gráfica, lógica de integración y pruebas del sistema |

##  Descripción del Proyecto
Sistema desarrollado en Python para gestión organizada de tareas personales y académicas, incluyendo un sistema inteligente de prioridades que utiliza el Strategy Pattern para adaptarse a diferentes necesidades del usuario.

##  Interfaz Gráfica (Tkinter)

### Características Principales

**Panel de Creación de Tareas:**
- Formulario intuitivo para nueva tarea
- Campos: título, descripción, categoría, fecha límite
- Selector de prioridad (Alta, Media, Baja)
- Validación de formato de fecha (YYYY-MM-DD o YYYY-MM-DDTHH:MM)

**Sistema de Visualización:**
- Lista tabular con columnas: ID, Título, Estado, Prioridad, Categoría, Fecha Límite
- Código de colores: verde para completadas, naranja para vencidas
- Filas alternadas para mejor legibilidad

**Sistema de Filtros y Búsqueda:**
- Búsqueda en tiempo real por texto
- Filtrado por estado (Todos, Pendiente, En Progreso, Completada)
- Ordenamiento múltiple (ID, Fecha creación, Fecha límite, Prioridad, Título)

**Gestión de Persistencia:**
- Selector de formato (JSON/CSV)
- Campos personalizables para nombre de archivo
- Botones de Guardar/Cargar inmediatos

**Estrategias de Prioridad:**
- Selector desplegable de estrategias
- Aplicación en un clic con confirmación visual
- Actualización en tiempo real de prioridades

**Funcionalidades de Gestión:**
- **Doble clic** para ver detalles completos de tarea
- **Edición rápida** de título y descripción
- **Marcado como completada** con un clic
- **Eliminación** con confirmación
- **Limpieza masiva** de tareas completadas

##  Funcionalidades Implementadas

| Estado | Descripción |
|--------|-------------|
| ✅ | Registro y gestión completa de tareas (CRUD) |
| ✅ | Sistema de priorización inteligente con tres estrategias |
| ✅ | Persistencia de datos en formatos JSON y CSV |
| ✅ | Filtros avanzados por estado, categoría, prioridad y fecha |
| ✅ | Múltiples criterios de ordenamiento |
| ✅ | Interfaz gráfica desarrollada con Tkinter |
| ✅ | Gestión centralizada de identificadores únicos |

##  Patrones de Diseño Implementados

| Patrón | Archivo | Uso | Justificación |
|--------|---------|-----|---------------|
| **Strategy Pattern** | `prioridad_strategy.py` | Múltiples algoritmos de priorización | Permite cambiar comportamientos en tiempo de ejecución y facilita la extensión |
| **Strategy Pattern** | `persistence_strategy.py` | Múltiples formatos de persistencia | Permite cambiar entre JSON y CSV sin afectar la lógica del programa |

##  Flujo del Sistema
1. **El usuario crea una nueva tarea** con título, descripción, categoría y fecha límite.  
2. **El sistema asigna automáticamente** un identificador único y estado inicial.  
3. **Se aplica la estrategia de priorización activa** para determinar el nivel de importancia.  
4. **La tarea es almacenada** en el formato de persistencia seleccionado (JSON o CSV).  
5. **El usuario puede filtrar y ordenar** las tareas según diferentes criterios.  
6. **La tarea avanza a través de sus estados** hasta su finalización.

## Estrategias de Priorización Implementadas

### Prioridad por Fecha
- Calcula la urgencia basándose en la proximidad de la fecha límite.  
- Asigna mayor prioridad a tareas con fechas próximas a vencer.

### Prioridad por Categoría
- Evalúa la importancia según el tipo de tarea.  
- Categorías académicas o urgentes reciben mayor prioridad.

### Prioridad Manual
- Permite al usuario asignar directamente las prioridades.  
- Ofrece control total sobre la importancia de cada tarea.

##  Decisiones Técnicas del Desarrollo

### Strategy Pattern en Priorización

**Motivo de su elección:**
El Strategy Pattern fue implementado en el proyecto por su capacidad para encapsular diferentes algoritmos de priorización, permitiendo que el sistema se adapte a diversas necesidades del usuario sin modificar el código central.

**Ventajas principales:**
- Permite cambiar entre estrategias de priorización durante la ejecución
- Facilita la adición de nuevos algoritmos sin afectar el código existente
- Mantiene cada estrategia aislada y fácil de probar individualmente
- Cumple con el principio Open/Closed de SOLID

### Gestión de Estados de Tareas

**Implementación:**
Se diseñó un sistema de estados dentro de la clase Tarea, permitiendo controlar de forma estructurada el ciclo de vida de cada tarea.

**Flujo de estados:**
PENDIENTE → EN_PROGRESO → COMPLETADA

**Ventaja principal:**
Ofrece un control preciso sobre las transiciones de estado, evitando errores lógicos y garantizando un seguimiento coherente de la tarea desde su creación hasta su finalización.

## Arquitectura del Sistema

### Módulos Especializados
- **Models**: Encargado exclusivamente de gestionar los datos.  
- **Strategies**: Contiene la lógica de priorización.  
- **Persistence**: Maneja el guardado y carga de la información.  
- **GUI**: Gestiona la interacción con el usuario.

Esta separación facilita el entendimiento, mantenimiento y testing del sistema.

### Strategy Pattern para Prioridades
Se implementó el _Strategy Pattern_ para permitir cambiar la forma en que el sistema calcula las prioridades sin modificar el código principal.

Este enfoque permite:
- Cambiar estrategias de priorización en tiempo de ejecución.  
- Agregar nuevas formas de priorizar tareas en el futuro.  
- Mantener cada estrategia independiente y fácil de probar.

### Gestión Centralizada de IDs
El sistema asigna identificadores únicos a cada tarea mediante un mecanismo centralizado, evitando duplicaciones y asegurando consistencia al guardar y cargar información.

##  Principios de Ingeniería Aplicados

### Modularidad
Cada parte del sistema cumple una función específica y bien definida. Esto facilita:
- La comprensión del código.  
- La localización y corrección de errores.  
- La implementación de cambios y mejoras.

### Encapsulamiento
Los detalles internos de cada módulo están protegidos y aislados.  
Por ejemplo:
- El módulo de persistencia es el único que conoce el formato exacto en que se guardan los datos (JSON o CSV).  
- El resto del sistema simplemente invoca métodos de carga o guardado, desconociendo los detalles internos.

### Separación de Responsabilidades
Cada clase tiene una tarea clara dentro del sistema:
- **Task**: Solo almacena datos de la tarea.  
- **Strategies**: Calculan la prioridad utilizando distintos métodos.  
- **Persistence**: Maneja el almacenamiento y recuperación de información.  
- **GUI**: Se encarga de la visualización e interacción con el usuario.

Este enfoque nos ayuda en la parte de minimizar dependencias además de permitir que cada pieza se optimice o reemplace sin afectar al resto del sistema.

## Documentación Técnica

### Diagramas UML Incluidos
El proyecto incluye tres diagramas UML que explican visualmente el sistema:

#### Diagrama de Casos de Uso
- Muestra todas las acciones que puede realizar el usuario.  
- Ilustra la interacción entre el usuario y el sistema.

#### Diagrama de Secuencia
- Explica el flujo de operaciones al crear una tarea.  
- Detalla la comunicación entre los diferentes componentes.

#### Diagrama de Clases
- Presenta la estructura completa del código.  
- Muestra las relaciones entre todas las clases del sistema.

## Pruebas y Validación

El sistema implementa diversos mecanismos de validación para asegurar la consistencia, la integridad de los datos y el correcto funcionamiento del flujo de tareas.

### Aspectos Verificados Cumplidos en el proyecto
- Validación de fechas límite para evitar fechas pasadas.  
- Verificación de campos obligatorios como el título de la tarea.  
- Control de identificadores únicos para cada tarea.  
- Estados válidos dentro del flujo de tareas.  
- Integridad de datos en operaciones de persistencia.  
- Correcto funcionamiento de las estrategias de priorización.


**Proyecto Académico - Materia Diseño De Software - Ingeniería de Software**

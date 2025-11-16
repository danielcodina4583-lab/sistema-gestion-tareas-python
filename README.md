**Sistema de Gestión de Tareas Académicas y Personales con Prioridades Inteligentes**

Descripción del Proyecto

Este proyecto consiste en un programa desarrollado en el Lenguaje de progrmación Python el cual permite gestionar tareas personales y académicas de forma organizada. 
La aplicación incluye un sistema inteligente de prioridades que se adapta a diferentes necesidades del usuario, usando el Strategy Pattern para ofrecer múltiples formas de calcular la importancia de las tareas.

Integrantes del proyecto:

| Nombre | Rol |
|--------|-----|
| **Daniel De Jesus Codina Ortiz** | Desarrollo del backend, estrategias de priorización y documentación técnica |
| **Ricardo Jose Valiente** | Desarrollo de la interfaz gráfica, lógica de integración y pruebas del sistema |


 Patrón De Diseño implementado
 
| Patrón                 | Archivo                   | Uso                                    | Justificación                                                                 |
| :-----------------     | :-------------------------| :--------------------------------------| :---------------------------------------------------------------------------- |
| **Strategy Pattern**   | `prioridad_strategy.py`   | Múltiples algoritmos de priorización   | Permite cambiar comportamientos en tiempo de ejecución y facilita la extensión|
| **Strategy Pattern**   | `persistence_strategy.py` | Múltiples formatos de persistencia     | Permite cambiar entre JSON y CSV sin afectar la lógica del programa           |


##  **Decisiones Técnicas del Desarrollo:**

### Strategy Pattern en Priorización

**Motivo de su elección:**

El Strategy Pattern fue implementado en el proyecto por su capacidad para encapsular diferentes algoritmos de priorización, permitiendo que el sistema se adapte a diversas necesidades del usuario sin modificar el código central.

**Ventajas principales:**

-Permite cambiar entre estrategias de priorización durante la ejecución

-Facilita la adición de nuevos algoritmos sin afectar el código existente

-Mantiene cada estrategia aislada y fácil de probar individualmente

-Cumple con el principio Open/Closed de SOLID

-Gestión de Estados de Tareas


**Implementación:**
Se diseñó un sistema de estados dentro de la clase Tarea, permitiendo controlar de forma estructurada el ciclo de vida de cada tarea.


**Flujo de estados:**
PENDIENTE → EN_PROGRESO → COMPLETADA


Ventaja principal:
Ofrece un control preciso sobre las transiciones de estado, evitando errores lógicos y garantizando un seguimiento coherente de la tarea desde su creación hasta su finalización.

## Funcionalidades Implementadas

| Estado | Descripción                                                  |
|--------|--------------------------------------------------------------|
| ✅     | Registro y gestión completa de tareas (CRUD)                 |
| ✅     | Sistema de priorización inteligente con tres estrategias     |
| ✅     | Persistencia de datos en formatos JSON y CSV                 |
| ✅     | Filtros avanzados por estado, categoría, prioridad y fecha   |
| ✅     | Múltiples criterios de ordenamiento                          |
| ✅     | Interfaz gráfica desarrollada con Tkinter                    |
| ✅     | Gestión centralizada de identificadores únicos               |


##  **Flujo del Sistema**

El proceso general del sistema sigue una secuencia lógica que abarca desde la creación de la tarea hasta su finalización:

1. **El usuario crea una nueva tarea** con título, descripción, categoría y fecha límite.  
2. **El sistema asigna automáticamente** un identificador único y estado inicial.  
3. **Se aplica la estrategia de priorización activa** para determinar el nivel de importancia.  
4. **La tarea es almacenada** en el formato de persistencia seleccionado (JSON o CSV).  
5. **El usuario puede filtrar y ordenar** las tareas según diferentes criterios.  
6. **La tarea avanza a través de sus estados** hasta su finalización.


##  **Estrategias de Priorización Implementadas**

El sistema incluye tres estrategias de priorización, cada una fue diseñada para diferentes necesidades de organización:

### En Primera parte tenemos la Prioridad por Fecha
- Calcula la urgencia basándose en la proximidad de la fecha límite.  
- Asigna mayor prioridad a tareas con fechas próximas a vencer.

### En Segunda Parte Tenemos la Prioridad por Categoría
- Evalúa la importancia según el tipo de tarea.  
- Categorías académicas o urgentes reciben mayor prioridad.

###  Por Ultima Parte Tenemos la Prioridad Manual
- Permite al usuario asignar directamente las prioridades.  
- Ofrece control total sobre la importancia de cada tarea.


##  **Pruebas y Validación**

El sistema implementa diversos mecanismos de validación para asegurar la consistencia, la integridad de los datos y el correcto funcionamiento del flujo de tareas.

###  Aspectos Verificados

- Validación de fechas límite para evitar fechas pasadas.  
- Verificación de campos obligatorios como el título de la tarea.  
- Control de identificadores únicos para cada tarea.  
- Estados válidos dentro del flujo de tareas.  
- Integridad de datos en operaciones de persistencia.  
- Correcto funcionamiento de las estrategias de priorización.


##  **Documentación Técnica del Proyecto**

###  **Diagramas UML**

El proyecto incluye tres diagramas UML que explican visualmente el sistema:

####  Diagrama de Casos de Uso
- Muestra todas las acciones que puede realizar el usuario.  
- Ilustra la interacción entre el usuario y el sistema.

####  Diagrama de Secuencia
- Explica el flujo de operaciones al crear una tarea.  
- Detalla la comunicación entre los diferentes componentes.

####  Diagrama de Clases
- Presenta la estructura completa del código.  
- Muestra las relaciones entre todas las clases del sistema.


###  **Decisiones de Diseño**

####  Arquitectura por Módulos
El sistema está dividido en módulos especializados para una estructura clara y mantenible:

- **Models**: Encargado exclusivamente de gestionar los datos.  
- **Strategies**: Contiene la lógica de priorización.  
- **Persistence**: Maneja el guardado y carga de la información.  
- **GUI**: Gestiona la interacción con el usuario.

Esta separación facilita el entendimiento, mantenimiento y testing del sistema.


####  Strategy Pattern para Prioridades
Se implementó el _Strategy Pattern_ para permitir cambiar la forma en que el sistema calcula las prioridades sin modificar el código principal.

Este enfoque permite:
- Cambiar estrategias de priorización en tiempo de ejecución.  
- Agregar nuevas formas de priorizar tareas en el futuro.  
- Mantener cada estrategia independiente y fácil de probar.


####  Gestión Centralizada de IDs
El sistema asigna identificadores únicos a cada tarea mediante un mecanismo centralizado, evitando duplicaciones y asegurando consistencia al guardar y cargar información.


##  **Principios de Ingeniería Aplicados**

El diseño del sistema se basa en sólidas prácticas de ingeniería de software que garantizan calidad, mantenibilidad y escalabilidad.

###  Modularidad
Cada parte del sistema cumple una función específica y bien definida. Esto facilita:
- La comprensión del código.  
- La localización y corrección de errores.  
- La implementación de cambios y mejoras.


###  Encapsulamiento
Los detalles internos de cada módulo están protegidos y aislados.  
Por ejemplo:
- El módulo de persistencia es el único que conoce el formato exacto en que se guardan los datos (JSON o CSV).  
- El resto del sistema simplemente invoca métodos de carga o guardado, desconociendo los detalles internos.


###  Separación de Responsabilidades
Cada clase tiene una tarea clara dentro del sistema:

- **Task**: Solo almacena datos de la tarea.  
- **Strategies**: Calculan la prioridad utilizando distintos métodos.  
- **Persistence**: Maneja el almacenamiento y recuperación de información.  
- **GUI**: Se encarga de la visualización e interacción con el usuario.

Este enfoque nos ayuda en la parte de minimizar dependencias además de permitir que cada pieza se optimice o reemplace sin afectar al resto del sistema.


**Proyecto Académico Materia Diseño De Software -  Ingeniería de Software**

Fecha de Entrega: 18 de Noviembre 2025

Estado: Funcionalidad completa implementada.


Repositorio link:

https://github.com/danielcodina4583-lab/sistema-gestion-tareas-python/tree/main

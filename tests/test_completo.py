import unittest, sys, os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.gestor_tareas import GestorTareas
from models.tarea import EstadoTarea, Prioridad
from strategies.prioridad_fecha import PrioridadFechaStrategy
from strategies.prioridad_categoria import PrioridadCategoriaStrategy
from strategies.prioridad_manual import PrioridadManualStrategy

print("PRUEBAS SISTEMA GESTION TAREAS")
print("=" * 40)

class TestTarea(unittest.TestCase):
    def test_creacion_tarea(self):
        from models.tarea import Tarea
        tarea = Tarea("Test", "Desc", "universidad")
        self.assertEqual(tarea.titulo, "Test")
        print("Tarea - Creacion: OK")

class TestGestorTareas(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorTareas()
    
    def test_crear_obtener_actualizar_eliminar(self):
        tarea = self.gestor.crear_tarea("Test", "Desc", "general")
        self.assertEqual(tarea.titulo, "Test")
        
        tarea_encontrada = self.gestor.obtener_tarea_por_id(tarea.id)
        self.assertEqual(tarea.id, tarea_encontrada.id)
        
        resultado = self.gestor.actualizar_tarea(tarea.id, titulo="Actualizado")
        self.assertTrue(resultado)
        
        resultado = self.gestor.eliminar_tarea(tarea.id)
        self.assertTrue(resultado)
        print("Gestor - CRUD completo: OK")
    
    def test_filtros_busqueda(self):
        t1 = self.gestor.crear_tarea("Pendiente", "Test", "general")
        t2 = self.gestor.crear_tarea("Completada", "Test", "general")
        self.gestor.actualizar_tarea(t2.id, estado=EstadoTarea.COMPLETADA)
        
        completadas = self.gestor.filtrar_por_estado(EstadoTarea.COMPLETADA)
        self.assertEqual(len(completadas), 1)
        
        resultados = self.gestor.buscar_por_texto("Completada")
        self.assertEqual(len(resultados), 1)
        print("Gestor - Filtros y busqueda: OK")
    
    def test_operaciones_avanzadas(self):
        t1 = self.gestor.crear_tarea("Baja", "Test", "general", prioridad=Prioridad.BAJA)
        t2 = self.gestor.crear_tarea("Alta", "Test", "general", prioridad=Prioridad.ALTA)
        
        ordenadas = self.gestor.ordenar_por_prioridad()
        self.assertEqual(ordenadas[0].prioridad, Prioridad.ALTA)
        
        fecha_pasada = datetime.now() - timedelta(days=1)
        t3 = self.gestor.crear_tarea("Vencida", "Test", "general", fecha_pasada)
        vencidas = self.gestor.obtener_tareas_vencidas()
        self.assertEqual(len(vencidas), 1)
        print("Gestor - Operaciones avanzadas: OK")

class TestEstrategias(unittest.TestCase):
    def setUp(self):
        from models.tarea import Tarea
        self.tarea = Tarea("Test", "Desc", "universidad")
    
    def test_estrategia_fecha(self):
        estrategia = PrioridadFechaStrategy()
        
        self.assertEqual(estrategia.calcular_prioridad(self.tarea), Prioridad.BAJA)
        
        self.tarea.fecha_limite = datetime.now() + timedelta(days=10)
        self.assertEqual(estrategia.calcular_prioridad(self.tarea), Prioridad.BAJA)
        
        self.tarea.fecha_limite = datetime.now() + timedelta(days=2)
        self.assertEqual(estrategia.calcular_prioridad(self.tarea), Prioridad.MEDIA)
        print("Estrategia Fecha: OK")
    
    def test_estrategia_categoria(self):
        estrategia = PrioridadCategoriaStrategy()
        
        self.tarea.categoria = "universidad"
        self.assertEqual(estrategia.calcular_prioridad(self.tarea), Prioridad.ALTA)
        
        self.tarea.categoria = "trabajo"
        self.assertEqual(estrategia.calcular_prioridad(self.tarea), Prioridad.ALTA)
        
        self.tarea.categoria = "estudio"
        self.assertEqual(estrategia.calcular_prioridad(self.tarea), Prioridad.MEDIA)
        print("Estrategia Categoria: OK")
    
    def test_estrategia_manual(self):
        estrategia = PrioridadManualStrategy()
        self.tarea.prioridad = Prioridad.ALTA
        self.assertEqual(estrategia.calcular_prioridad(self.tarea), Prioridad.ALTA)
        print("Estrategia Manual: OK")

class TestPersistencia(unittest.TestCase):
    def test_json(self):
        gestor = GestorTareas()
        gestor.crear_tarea("Test JSON", "Desc", "general")
        
        self.assertTrue(gestor.guardar_tareas("test.json"))
        
        gestor.tareas = []
        self.assertTrue(gestor.cargar_tareas("test.json"))
        
        if os.path.exists("test.json"):
            os.remove("test.json")
        print("Persistencia JSON: OK")

def main():
    print("\nEJECUTANDO PRUEBAS...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestTarea))
    suite.addTests(loader.loadTestsFromTestCase(TestGestorTareas))
    suite.addTests(loader.loadTestsFromTestCase(TestEstrategias))
    suite.addTests(loader.loadTestsFromTestCase(TestPersistencia))
    
    runner = unittest.TextTestRunner(verbosity=0)
    resultado = runner.run(suite)
    
    print(f"\nRESUMEN: {resultado.testsRun} pruebas ejecutadas")
    print(f"Exitosas: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Fallidas: {len(resultado.failures)}")
    
    if not resultado.wasSuccessful():
        print("\nFALLOS:")
        for test, traceback in resultado.failures:
            print(f"- {test}")

if __name__ == '__main__':
    main()
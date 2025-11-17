import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime

# Asegurar que el paquete interno sea importable cuando `gui.py` está en la raíz
BASE = os.path.dirname(__file__)
INNER = os.path.join(BASE, 'sistema-gestion-tareas-python-main')
if os.path.isdir(INNER) and INNER not in sys.path:
    sys.path.insert(0, INNER)

from models.gestor_tareas import GestorTareas
from models.tarea import EstadoTarea, Prioridad


def formato_fecha(f):
    return f.strftime('%Y-%m-%d %H:%M') if f else ''


class TareasApp:
    def __init__(self, root):
        self.root = root
        root.title('Gestor de Tareas')
        root.geometry('980x620')

        # Paleta limpia y neutral (grises suaves)
        self.colors = {
            'bg': '#f5f6f7',        # fondo general very light gray
            'card': '#ffffff',      # tarjetas / fondo principal blanco
            'accent': '#607d8b',    # blue-gray accent (elegante)
            'accent_dark': '#455a64',
            'success': '#2e7d32',
            'danger': '#c62828',
            'muted': '#6b6b6b',
            'header': '#f0f2f3',    # header sutil
            'completed': '#eef7ee', # very light green
            'overdue': '#fff5f2',   # very light red/orange
            'row_even': '#fbfcfd',
            'row_odd': '#ffffff'
        }

        self.root.configure(bg=self.colors['bg'])

        # ttk Style
        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('Treeview', background=self.colors['card'], fieldbackground=self.colors['card'], foreground=self.colors['muted'], rowheight=26, font=('Segoe UI', 10))
        style.configure('Treeview.Heading', background=self.colors['header'], foreground=self.colors['muted'], font=('Segoe UI', 10, 'bold'))
        style.configure('TButton', padding=6, font=('Segoe UI', 9))
        style.configure('Accent.TButton', foreground='white')
        style.map('Accent.TButton', background=[('active', self.colors['accent_dark'])], foreground=[('disabled', '#aaaaaa')])
        style.configure('TLabel', font=('Segoe UI', 10))

        self.gestor = GestorTareas()

        self._build_ui()
        self._cargar_cache_estrategias()
        self.refresh_tree()

    def _build_ui(self):
        # Frames principales
        left = ttk.Frame(self.root, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        right = ttk.Frame(self.root, padding=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- LEFT: formulario crear/editar ---
        ttk.Label(left, text='Nueva / Editar tarea', font=('Segoe UI', 12, 'bold')).pack(anchor='w')

        ttk.Label(left, text='Título').pack(anchor='w', pady=(8, 0))
        self.entry_titulo = ttk.Entry(left, width=28)
        self.entry_titulo.pack()

        ttk.Label(left, text='Descripción').pack(anchor='w', pady=(6, 0))
        self.entry_descripcion = ttk.Entry(left, width=28)
        self.entry_descripcion.pack()

        ttk.Label(left, text='Categoría').pack(anchor='w', pady=(6, 0))
        self.entry_categoria = ttk.Entry(left, width=28)
        self.entry_categoria.pack()

        ttk.Label(left, text='Fecha límite (YYYY-MM-DD o YYYY-MM-DDTHH:MM)').pack(anchor='w', pady=(6, 0))
        self.entry_fecha = ttk.Entry(left, width=28)
        self.entry_fecha.pack()

        ttk.Label(left, text='Prioridad').pack(anchor='w', pady=(6, 0))
        self.prioridad_var = tk.StringVar(value=Prioridad.MEDIA.value)
        prioridades = [p.value for p in Prioridad]
        self.prio_menu = ttk.OptionMenu(left, self.prioridad_var, self.prioridad_var.get(), *prioridades)
        self.prio_menu.pack(fill='x')

        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=(10, 0))
        ttk.Button(btn_frame, text='Crear', command=self.create_from_form).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text='Limpiar', command=self.clear_form).grid(row=0, column=1, padx=4)

        # Persistencia pequeña
        ttk.Label(left, text='Persistencia (archivo)').pack(anchor='w', pady=(12, 0))
        self.entry_archivo = ttk.Entry(left, width=28)
        self.entry_archivo.insert(0, 'tareas.json')
        self.entry_archivo.pack()
        persist_frame = ttk.Frame(left)
        persist_frame.pack(pady=6)
        self.persist_var = tk.StringVar(value='JSON')
        ttk.OptionMenu(persist_frame, self.persist_var, self.persist_var.get(), 'JSON', 'CSV').grid(row=0, column=0)
        ttk.Button(persist_frame, text='Establecer', command=self.establecer_persistencia).grid(row=0, column=1, padx=6)
        ttk.Button(persist_frame, text='Guardar', command=self.guardar_tareas).grid(row=1, column=0, pady=4)
        ttk.Button(persist_frame, text='Cargar', command=self.cargar_tareas).grid(row=1, column=1, pady=4)

        # Estrategias
        ttk.Label(left, text='Estrategia prioridad').pack(anchor='w', pady=(12, 0))
        self.estr_var = tk.StringVar()
        self.estr_menu = ttk.OptionMenu(left, self.estr_var, '')
        self.estr_menu.pack(fill='x')
        ttk.Button(left, text='Aplicar estrategia', command=self.aplicar_estrategia).pack(pady=6)

        # --- RIGHT: filtros, búsqueda, treeview ---
        top_right = ttk.Frame(right)
        top_right.pack(fill='x')

        ttk.Label(top_right, text='Buscar:').pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        ttk.Entry(top_right, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=6)
        ttk.Button(top_right, text='Ir', command=self.refresh_tree).pack(side=tk.LEFT)

        ttk.Label(top_right, text='Estado:').pack(side=tk.LEFT, padx=(12, 0))
        estados = ['Todos'] + [e.value for e in EstadoTarea]
        self.estado_var = tk.StringVar(value='Todos')
        ttk.OptionMenu(top_right, self.estado_var, self.estado_var.get(), *estados).pack(side=tk.LEFT, padx=4)

        ttk.Label(top_right, text='Ordenar:').pack(side=tk.LEFT, padx=(12, 0))
        self.sort_var = tk.StringVar(value='id')
        ttk.OptionMenu(top_right, self.sort_var, 'id', 'id', 'fecha_creacion', 'fecha_limite', 'prioridad', 'titulo').pack(side=tk.LEFT)

        # Treeview
        cols = ('id', 'titulo', 'estado', 'prioridad', 'categoria', 'fecha_limite')
        self.tree = ttk.Treeview(right, columns=cols, show='headings', selectmode='browse')
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor='w')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        self.tree.bind('<Double-1>', lambda e: self.view_selected())
        # etiquetas para filas
        # etiquetas para filas: completada, vencida y zebra (par/impar)
        try:
            self.tree.tag_configure('completed', background=self.colors['completed'])
            self.tree.tag_configure('overdue', background=self.colors['overdue'])
            self.tree.tag_configure('odd', background=self.colors['row_odd'])
            self.tree.tag_configure('even', background=self.colors['row_even'])
        except Exception:
            pass

        # Actions
        action_bar = ttk.Frame(right)
        action_bar.pack(fill='x', pady=8)
        ttk.Button(action_bar, text='Ver', command=self.view_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(action_bar, text='Editar', command=self.edit_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(action_bar, text='Marcar completada', command=self.complete_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(action_bar, text='Eliminar', command=self.delete_selected).pack(side=tk.LEFT, padx=6)
        ttk.Button(action_bar, text='Limpiar completadas', command=self.limpiar_completadas).pack(side=tk.RIGHT, padx=6)

    # --- Form helpers ---
    def clear_form(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.prioridad_var.set(Prioridad.MEDIA.value)

    def create_from_form(self):
        titulo = self.entry_titulo.get().strip()
        if not titulo:
            messagebox.showwarning('Error', 'Título obligatorio')
            return
        descripcion = self.entry_descripcion.get().strip()
        categoria = self.entry_categoria.get().strip() or 'general'
        fecha_text = self.entry_fecha.get().strip()
        fecha_limite = None
        if fecha_text:
            try:
                fecha_limite = datetime.fromisoformat(fecha_text)
            except Exception:
                messagebox.showwarning('Error', 'Formato fecha inválido')
                return
        prioridad = Prioridad(self.prioridad_var.get())
        self.gestor.crear_tarea(titulo, descripcion, categoria, fecha_limite, prioridad)
        self.clear_form()
        self.refresh_tree()

    # --- Tree / selection helpers ---
    def _tree_items(self, tareas):
        for t in tareas:
            yield (t.id, t.titulo, t.estado.value, t.prioridad.value, t.categoria, formato_fecha(t.fecha_limite))

    def refresh_tree(self):
        q = self.search_var.get().strip()
        estado = self.estado_var.get()
        sort_key = self.sort_var.get()

        if q:
            tareas = self.gestor.buscar_por_texto(q)
        else:
            tareas = self.gestor.obtener_todas_tareas()

        if estado != 'Todos':
            tareas = [t for t in tareas if t.estado.value == estado]

        # ordenar
        if sort_key == 'fecha_limite':
            tareas = sorted(tareas, key=lambda x: x.fecha_limite or datetime.max)
        elif sort_key == 'fecha_creacion':
            tareas = sorted(tareas, key=lambda x: x.fecha_creacion)
        elif sort_key == 'prioridad':
            orden = {Prioridad.ALTA: 1, Prioridad.MEDIA: 2, Prioridad.BAJA: 3}
            tareas = sorted(tareas, key=lambda x: orden.get(x.prioridad, 4))
        elif sort_key == 'titulo':
            tareas = sorted(tareas, key=lambda x: x.titulo.lower())

        # refresh
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, t in enumerate(tareas):
            row = (t.id, t.titulo, t.estado.value, t.prioridad.value, t.categoria, formato_fecha(t.fecha_limite))
            tags = []
            # zebra
            tags.append('even' if idx % 2 else 'odd')
            # estado especial
            if t.estado == EstadoTarea.COMPLETADA:
                tags.append('completed')
            else:
                if t.fecha_limite and t.fecha_limite < datetime.now() and t.estado != EstadoTarea.COMPLETADA:
                    tags.append('overdue')
            self.tree.insert('', tk.END, values=row, tags=tags)

    def _selected_task_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        vals = self.tree.item(sel[0])['values']
        return int(vals[0])

    def view_selected(self):
        tid = self._selected_task_id()
        if not tid:
            messagebox.showinfo('Info', 'Selecciona una tarea')
            return
        tarea = self.gestor.obtener_tarea_por_id(tid)
        text = f"ID: {tarea.id}\nTítulo: {tarea.titulo}\nDescripción: {tarea.descripcion}\nCategoría: {tarea.categoria}\nEstado: {tarea.estado.value}\nPrioridad: {tarea.prioridad.value}\nCreada: {tarea.fecha_creacion}\nActualizada: {tarea.fecha_actualizacion}"
        if tarea.fecha_limite:
            text += f"\nFecha límite: {tarea.fecha_limite}"
        messagebox.showinfo(f'Tarea {tarea.id}', text)

    def edit_selected(self):
        tid = self._selected_task_id()
        if not tid:
            messagebox.showinfo('Info', 'Selecciona una tarea')
            return
        tarea = self.gestor.obtener_tarea_por_id(tid)
        # mostrar simple diálogo para editar título y descripción (puede extenderse)
        nuevo_titulo = simpledialog.askstring('Editar título', 'Título', initialvalue=tarea.titulo)
        if nuevo_titulo is None:
            return
        nueva_desc = simpledialog.askstring('Editar descripción', 'Descripción', initialvalue=tarea.descripcion)
        if nueva_desc is None:
            nueva_desc = tarea.descripcion
        self.gestor.actualizar_tarea(tid, titulo=nuevo_titulo, descripcion=nueva_desc)
        self.refresh_tree()

    def complete_selected(self):
        tid = self._selected_task_id()
        if not tid:
            messagebox.showinfo('Info', 'Selecciona una tarea')
            return
        self.gestor.actualizar_tarea(tid, estado=EstadoTarea.COMPLETADA)
        self.refresh_tree()

    def delete_selected(self):
        tid = self._selected_task_id()
        if not tid:
            messagebox.showinfo('Info', 'Selecciona una tarea')
            return
        if messagebox.askyesno('Confirmar', 'Eliminar tarea seleccionada?'):
            self.gestor.eliminar_tarea(tid)
            self.refresh_tree()

    def limpiar_completadas(self):
        n = self.gestor.limpiar_tareas_completadas()
        messagebox.showinfo('Limpiar', f'{n} tareas completadas eliminadas')
        self.refresh_tree()

    # --- Persistencia / estrategias ---
    def establecer_persistencia(self):
        tipo = self.persist_var.get()
        try:
            self.gestor.establecer_persistencia(tipo)
            messagebox.showinfo('Persistencia', f'Persistencia establecida: {tipo}')
        except Exception as e:
            messagebox.showwarning('Error', str(e))

    def guardar_tareas(self):
        archivo = self.entry_archivo.get().strip() or 'tareas.json'
        ok = self.gestor.guardar_tareas(archivo)
        messagebox.showinfo('Guardar', 'Guardado exitoso' if ok else 'Error al guardar')

    def cargar_tareas(self):
        archivo = self.entry_archivo.get().strip() or 'tareas.json'
        ok = self.gestor.cargar_tareas(archivo)
        messagebox.showinfo('Cargar', 'Tareas cargadas' if ok else 'No se cargaron tareas')
        self.refresh_tree()

    def _cargar_cache_estrategias(self):
        estrategias = self.gestor.obtener_estrategias_disponibles()
        opciones = [e.get_nombre() if hasattr(e, 'get_nombre') else e.__class__.__name__ for e in estrategias]
        menu = self.estr_menu['menu']
        menu.delete(0, 'end')
        for o in opciones:
            menu.add_command(label=o, command=lambda v=o: self.estr_var.set(v))
        if opciones:
            self.estr_var.set(opciones[0])
        self._estr_objetos = estrategias

    def aplicar_estrategia(self):
        nombre = self.estr_var.get()
        for e in self._estr_objetos:
            if (hasattr(e, 'get_nombre') and e.get_nombre() == nombre) or e.__class__.__name__ == nombre:
                self.gestor.establecer_estrategia_prioridad(e)
                self.gestor.aplicar_prioridad_inteligente()
                self.refresh_tree()
                messagebox.showinfo('Estrategia', f'Estrategia aplicada: {nombre}')
                return
        messagebox.showwarning('Estrategia', 'No se encontró la estrategia')


def main():
    root = tk.Tk()
    app = TareasApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

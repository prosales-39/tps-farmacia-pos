import tkinter as tk
from tkinter import ttk, messagebox
from controllers.ventas_controller import VentasController
from utils.helpers import formatear_precio

class VentasView:

    def __init__(self, contenedor, usuario_id):
        self.contenedor = contenedor
        self.usuario_id = usuario_id
        self.carrito = []  # lista de dicts con producto_id, nombre, cantidad, precio_unitario
        self.total = 0.0

        self.crear_interfaz()
        self.buscar_productos()

    def crear_interfaz(self):
        # Título
        tk.Label(
            self.contenedor,
            text="💰 Ventas",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=(10, 5))

        # Panel principal: izquierda (productos) y derecha (carrito)
        panel_principal = tk.Frame(self.contenedor, bg="white")
        panel_principal.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Panel izquierdo: búsqueda y lista de productos ---
        panel_izq = tk.Frame(panel_principal, bg="white", width=500)
        panel_izq.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Búsqueda
        frame_buscar = tk.Frame(panel_izq, bg="white")
        frame_buscar.pack(fill="x", pady=5)
        tk.Label(frame_buscar, text="Buscar producto:", bg="white").pack(side="left", padx=5)
        self.entry_busqueda = tk.Entry(frame_buscar, width=30)
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self.buscar_productos())
        tk.Button(
            frame_buscar,
            text="Buscar",
            command=self.buscar_productos,
            bg="#1565C0",
            fg="white",
            relief="flat"
        ).pack(side="left", padx=5)

        # Treeview de productos disponibles
        self.tree_productos = ttk.Treeview(
            panel_izq,
            columns=("codigo", "nombre", "stock", "precio"),
            show="headings",
            height=15
        )
        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Producto")
        self.tree_productos.heading("stock", text="Stock")
        self.tree_productos.heading("precio", text="Precio")
        self.tree_productos.column("codigo", width=80)
        self.tree_productos.column("nombre", width=180)
        self.tree_productos.column("stock", width=60)
        self.tree_productos.column("precio", width=80)
        self.tree_productos.pack(fill="both", expand=True, pady=5)

        # Botón agregar al carrito
        btn_agregar = tk.Button(
            panel_izq,
            text="Agregar al carrito",
            command=self.agregar_al_carrito,
            bg="#43A047",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        btn_agregar.pack(pady=5)

        # --- Panel derecho: carrito ---
        panel_der = tk.Frame(panel_principal, bg="white", width=400)
        panel_der.pack(side="right", fill="both", expand=True, padx=(5, 0))

        tk.Label(panel_der, text="Carrito de venta", font=("Segoe UI", 12, "bold"), bg="white").pack(pady=5)

        # Treeview del carrito
        self.tree_carrito = ttk.Treeview(
            panel_der,
            columns=("producto", "cantidad", "precio", "subtotal"),
            show="headings",
            height=12
        )
        self.tree_carrito.heading("producto", text="Producto")
        self.tree_carrito.heading("cantidad", text="Cant.")
        self.tree_carrito.heading("precio", text="Precio")
        self.tree_carrito.heading("subtotal", text="Subtotal")
        self.tree_carrito.column("producto", width=120)
        self.tree_carrito.column("cantidad", width=60)
        self.tree_carrito.column("precio", width=80)
        self.tree_carrito.column("subtotal", width=80)
        self.tree_carrito.pack(fill="both", expand=True, pady=5)

        # Botón eliminar del carrito
        btn_eliminar = tk.Button(
            panel_der,
            text="Eliminar seleccionado",
            command=self.eliminar_del_carrito,
            bg="#E53935",
            fg="white",
            relief="flat"
        )
        btn_eliminar.pack(pady=5)

        # Totales
        frame_totales = tk.Frame(panel_der, bg="white")
        frame_totales.pack(fill="x", pady=10)

        self.label_subtotal = tk.Label(frame_totales, text="Subtotal: $0", font=("Segoe UI", 11), bg="white")
        self.label_subtotal.pack(anchor="e")

        self.label_iva = tk.Label(frame_totales, text="IVA (19%): $0", font=("Segoe UI", 11), bg="white")
        self.label_iva.pack(anchor="e")

        self.label_total = tk.Label(frame_totales, text="Total: $0", font=("Segoe UI", 14, "bold"), fg="#1565C0", bg="white")
        self.label_total.pack(anchor="e")

        # Botón finalizar venta
        btn_finalizar = tk.Button(
            panel_der,
            text="Finalizar venta",
            command=self.finalizar_venta,
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=20,
            pady=8
        )
        btn_finalizar.pack(pady=10)

    def buscar_productos(self):
        termino = self.entry_busqueda.get().strip()
        productos = VentasController.obtener_productos_para_venta(termino)
        # Limpiar tree
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for p in productos:
            self.tree_productos.insert(
                "",
                "end",
                values=(p["codigo"], p["nombre"], p["stock"], formatear_precio(p["precio"])),
                tags=(p["id"],)
            )

    def agregar_al_carrito(self):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Seleccione un producto de la lista")
            return
        item = self.tree_productos.item(seleccion[0])
        producto_id = item["tags"][0]
        codigo = item["values"][0]
        nombre = item["values"][1]
        stock = item["values"][2]
        precio_str = item["values"][3].replace("$", "").replace(".", "")
        precio = float(precio_str)

        # Pedir cantidad
        ventana_cant = tk.Toplevel(self.contenedor)
        ventana_cant.title("Cantidad")
        ventana_cant.geometry("250x150")
        ventana_cant.resizable(False, False)
        ventana_cant.grab_set()

        tk.Label(ventana_cant, text=f"Producto: {nombre}", font=("Segoe UI", 10)).pack(pady=5)
        tk.Label(ventana_cant, text=f"Stock disponible: {stock}").pack()
        tk.Label(ventana_cant, text="Cantidad:").pack(pady=5)
        entry_cant = tk.Entry(ventana_cant, width=10)
        entry_cant.pack()

        def confirmar():
            try:
                cant = int(entry_cant.get())
                if cant <= 0:
                    raise ValueError
                if cant > stock:
                    messagebox.showerror("Error", "Cantidad excede el stock disponible")
                    return
                # Agregar al carrito
                # Si ya existe, sumar cantidad
                for item_carrito in self.carrito:
                    if item_carrito["producto_id"] == producto_id:
                        item_carrito["cantidad"] += cant
                        self.actualizar_carrito()
                        ventana_cant.destroy()
                        return
                # Nuevo item
                self.carrito.append({
                    "producto_id": producto_id,
                    "nombre": nombre,
                    "cantidad": cant,
                    "precio_unitario": precio
                })
                self.actualizar_carrito()
                ventana_cant.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        tk.Button(ventana_cant, text="Aceptar", command=confirmar, bg="#43A047", fg="white").pack(pady=10)

    def eliminar_del_carrito(self):
        seleccion = self.tree_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Seleccione un item del carrito")
            return
        # Obtener índice según selección
        item = self.tree_carrito.item(seleccion[0])
        # Buscar en el carrito por nombre y precio (asumiendo que es único)
        nombre = item["values"][0]
        precio = float(item["values"][2].replace("$", "").replace(".", ""))
        for i, car in enumerate(self.carrito):
            if car["nombre"] == nombre and car["precio_unitario"] == precio:
                del self.carrito[i]
                break
        self.actualizar_carrito()

    def actualizar_carrito(self):
        # Limpiar tree carrito
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)

        subtotal = 0.0
        for item in self.carrito:
            sub = item["cantidad"] * item["precio_unitario"]
            subtotal += sub
            self.tree_carrito.insert(
                "",
                "end",
                values=(
                    item["nombre"],
                    item["cantidad"],
                    formatear_precio(item["precio_unitario"]),
                    formatear_precio(sub)
                )
            )

        iva = subtotal * 0.19
        total = subtotal + iva
        self.label_subtotal.config(text=f"Subtotal: {formatear_precio(subtotal)}")
        self.label_iva.config(text=f"IVA (19%): {formatear_precio(iva)}")
        self.label_total.config(text=f"Total: {formatear_precio(total)}")

    def finalizar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Carrito vacío", "No hay productos en el carrito")
            return

        # Confirmar
        if not messagebox.askyesno("Confirmar venta", "¿Registrar esta venta?"):
            return

        try:
            # Preparar datos para el controlador
            items = []
            for item in self.carrito:
                items.append({
                    "producto_id": item["producto_id"],
                    "cantidad": item["cantidad"],
                    "precio_unitario": item["precio_unitario"]
                })
            venta_id = VentasController.realizar_venta(self.usuario_id, items)
            messagebox.showinfo("Venta registrada", f"Venta #{venta_id} realizada con éxito.")
            # Limpiar carrito
            self.carrito.clear()
            self.actualizar_carrito()
            # Refrescar lista de productos (stock actualizado)
            self.buscar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la venta: {e}")
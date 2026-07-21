-- Crear tabla facturas
CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    numero_factura TEXT NOT NULL UNIQUE,
    fecha_emision DATE NOT NULL,
    subtotal REAL NOT NULL,
    iva REAL NOT NULL,
    total REAL NOT NULL,
    cliente_nombre TEXT,
    cliente_documento TEXT,
    estado TEXT DEFAULT 'ACTIVA',

    FOREIGN KEY (venta_id)
        REFERENCES ventas(id)
);

-- Crear índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_facturas_venta_id ON facturas(venta_id);
CREATE INDEX IF NOT EXISTS idx_facturas_numero ON facturas(numero_factura);
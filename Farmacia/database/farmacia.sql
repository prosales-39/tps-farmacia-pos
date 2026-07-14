PRAGMA foreign_keys = ON;

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    usuario TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    rol_id INTEGER NOT NULL,
    estado INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (rol_id)
        REFERENCES roles(id)
);

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento TEXT UNIQUE,
    nombre TEXT NOT NULL,
    telefono TEXT,
    direccion TEXT
);

CREATE TABLE proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    correo TEXT,
    direccion TEXT
);

CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE,
    nombre TEXT NOT NULL,
    categoria TEXT,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    stock_minimo INTEGER NOT NULL DEFAULT 10,
    fecha_vencimiento DATE,
    lote TEXT,
    requiere_receta INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proveedor_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    total REAL NOT NULL,

    FOREIGN KEY (proveedor_id)
        REFERENCES proveedores(id),

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
);

CREATE TABLE detalle_compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compra_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,

    FOREIGN KEY (compra_id)
        REFERENCES compras(id),

    FOREIGN KEY (producto_id)
        REFERENCES productos(id)
);

CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    usuario_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    subtotal REAL NOT NULL,
    iva REAL NOT NULL,
    total REAL NOT NULL,

    FOREIGN KEY (cliente_id)
        REFERENCES clientes(id),

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
);

CREATE TABLE detalle_venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,

    FOREIGN KEY (venta_id)
        REFERENCES ventas(id),

    FOREIGN KEY (producto_id)
        REFERENCES productos(id)
);

CREATE TABLE recetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    medico TEXT NOT NULL,
    numero_receta TEXT NOT NULL,
    fecha DATE NOT NULL,

    FOREIGN KEY (cliente_id)
        REFERENCES clientes(id),

    FOREIGN KEY (producto_id)
        REFERENCES productos(id)
);

INSERT INTO roles (nombre) VALUES
('Administrador'),
('Empleado');

INSERT INTO usuarios (nombre, usuario, password, rol_id)
VALUES
('Administrador General', 'admin', 'admin123', 1);

INSERT INTO productos (codigo, nombre, categoria, precio, stock, stock_minimo, fecha_vencimiento, lote, requiere_receta)
VALUES
('MED001', 'Acetaminofén 500 mg', 'Analgésico', 2500, 50, 10, '2027-12-20', 'L001', 0),
('MED002', 'Ibuprofeno 400 mg', 'Antiinflamatorio', 3500, 25, 10, '2028-03-15', 'L002', 0),
('MED003', 'Amoxicilina 500 mg', 'Antibiótico', 9800, 15, 5, '2027-08-10', 'L003', 1),
('MED004', 'Loratadina', 'Antialérgico', 4200, 18, 5, '2027-11-05', 'L004', 0),
('MED005', 'Omeprazol', 'Gastrointestinal', 5600, 35, 10, '2028-05-18', 'L005', 0);


INSERT INTO proveedores (nombre, telefono, correo, direccion) VALUES
('Distribuidora Farmacéutica S.A.', '3001234567', 'ventas@dfsa.com', 'Calle 1 #2-3, Bogotá'),
('Laboratorios Vital', '3009876543', 'contacto@vital.com', 'Carrera 4 #5-6, Medellín'),
('Droguería Cruz Azul', '3004567890', 'cruzazul@email.com', 'Avenida 7 #8-9, Cali');
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

INSERT INTO proveedores (nombre, telefono, correo, direccion) VALUES
('Distribuidora Farmacéutica S.A.', '3001234567', 'ventas@dfsa.com', 'Calle 1 #2-3, Bogotá'),
('Laboratorios Vital', '3009876543', 'contacto@vital.com', 'Carrera 4 #5-6, Medellín'),
('Droguería Cruz Azul', '3004567890', 'comercial@drogueriacruzazul.com.co', 'Avenida 7 #8-9, Cali'),
('Genfar S.A.', '3104567812', 'ventas@genfar.com', 'Zona Industrial, Bogotá'),
('Tecnoquímicas S.A.', '3115678923', 'clientes@tecnoquimicas.com', 'Calle 70 #45-20, Cali'),
('Laboratorios La Santé', '3126789034', 'comercial@lasante.com.co', 'Carrera 68 #24-15, Bogotá'),
('Procaps S.A.', '3137890145', 'ventas@procapslaboratorios.com', 'Vía 40 #85-470, Barranquilla'),
('Abbott Colombia', '3148901256', 'servicio.cliente@abbott.com', 'Calle 100 #11-60, Bogotá'),
('Pfizer Colombia', '3159012367', 'atencion.clientes@pfizer.com', 'Carrera 9 #115-06, Bogotá'),
('Sanofi Colombia', '3160123478', 'contacto@sanofi.com', 'Calle 93A #13-24, Bogotá'),
('Bayer S.A. Colombia', '3171234589', 'servicio.clientes@bayer.com', 'Carrera 58 #10-76, Bogotá'),
('Johnson & Johnson Colombia', '3182345690', 'consumidores@jnj.com', 'Calle 90 #19-41, Bogotá'),
('Nestlé Health Science', '3193456701', 'ventas.health@nestle.com', 'Calle 98 #22-64, Bogotá');

INSERT INTO productos (codigo, nombre, categoria, precio, stock, stock_minimo, fecha_vencimiento, lote, requiere_receta) VALUES

-- ============ MEDICAMENTOS PRINCIPALES ============
-- Analgésicos y Antiinflamatorios (Versiones más comerciales)
('MED-ACET-500-001','Acetaminofén 500 mg (Caja x 100)','Analgésico',5000,95,15,'2028-07-10','L1001',0),
('MED-ACET-JAR-002','Acetaminofén Jarabe Infantil 150mg/5ml','Analgésico',8500,60,10,'2028-06-20','L1002',0),
('MED-IBUP-400-003','Ibuprofeno 400 mg','Antiinflamatorio',6000,85,12,'2028-10-20','L2003',0),
('MED-IBUP-600-004','Ibuprofeno 600 mg','Antiinflamatorio',8500,70,10,'2028-11-10','L2004',0),
('MED-NAP-500-005','Naproxeno 500 mg','Antiinflamatorio',9000,75,10,'2029-01-15','L3005',1),
('MED-DICL-50-006','Diclofenaco 50 mg','Antiinflamatorio',5000,80,10,'2029-02-20','L4006',1),

-- Antibióticos
('MED-AMOX-500-007','Amoxicilina 500 mg','Antibiótico',12000,50,10,'2028-04-15','L5007',1),
('MED-AMOX-SUSP-008','Amoxicilina Suspensión 250mg/5ml','Antibiótico',15000,40,8,'2028-05-20','L5008',1),
('MED-AZIT-500-009','Azitromicina 500 mg (3 tabs)','Antibiótico',15000,35,5,'2028-06-25','L6009',1),
('MED-CEFA-500-010','Cefalexina 500 mg','Antibiótico',16000,30,5,'2028-07-30','L7010',1),

-- Gastrointestinales y Antialérgicos
('MED-OME-20-011','Omeprazol 20 mg','Gastrointestinal',6000,100,15,'2028-08-10','L8011',0),
('MED-ESO-40-012','Esomeprazol 40 mg','Gastrointestinal',14000,70,10,'2028-10-20','L9012',0),
('MED-LORA-10-013','Loratadina 10 mg','Antialérgico',4500,90,15,'2028-11-25','L10013',0),
('MED-CETI-10-014','Cetirizina 10 mg','Antialérgico',5500,85,12,'2028-12-30','L11014',0),

-- Crónicos y Especialidades
('MED-SALB-100-015','Salbutamol Inhalador 100 mcg','Broncodilatador',18000,40,5,'2029-01-10','L12015',1),
('MED-METF-850-016','Metformina 850 mg','Antidiabético',9500,50,8,'2029-03-20','L13016',1),
('MED-LOSA-50-017','Losartán 50 mg','Antihipertensivo',9000,70,10,'2029-04-25','L14017',1),
('MED-ENAL-20-018','Enalapril 20 mg','Antihipertensivo',6500,65,10,'2029-06-10','L15018',1),
('MED-PRED-20-019','Prednisolona 20 mg','Corticoide',9500,40,5,'2028-07-15','L16019',1),
('MED-FLUC-150-020','Fluconazol 150 mg','Antimicótico',8500,45,5,'2028-10-30','L19020',1),
('MED-SERT-50-021','Sertralina 50 mg','Antidepresivo',22000,25,5,'2029-01-05','L20021',1),
('MED-ATOR-20-022','Atorvastatina 20 mg','Hipolipemiante',14000,25,5,'2029-02-28','L95022',1),

-- ============ SALUD SEXUAL Y ANTICONCEPCIÓN ============
('SEX-COND-3PK-023','Condones Today Clásico (3 unid)','Salud Sexual',12000,60,10,'2029-06-30','L20023',0),
('SEX-COND-RET-024','Condones Durex Retardante (3 unid)','Salud Sexual',15000,50,10,'2029-07-15','L20024',0),
('SEX-LUB-100-025','Lubricante íntimo a base de agua 100 ml','Salud Sexual',18000,40,8,'2029-08-10','L20025',0),
('SEX-PUL-EMERG-026','Píldora del día después (Levonorgestrel)','Salud Sexual',16000,35,5,'2028-12-20','L20026',0),
('SEX-PRUEB-EMB-027','Prueba de embarazo en tira','Salud Sexual',8500,80,12,'2029-01-15','L20027',0),

-- ============ HIGIENE FEMENINA ============
('HIG-TOA-DIA-028','Toallas higiénicas tela suave (10 unid)','Higiene Femenina',7000,100,15,'2029-10-10','L21028',0),
('HIG-TOA-NOC-029','Toallas higiénicas nocturnas (8 unid)','Higiene Femenina',8500,80,12,'2029-10-15','L21029',0),
('HIG-TAMP-10-030','Tampones regulares (10 unid)','Higiene Femenina',11000,60,10,'2029-11-20','L21030',0),
('HIG-JAB-INT-031','Jabón íntimo femenino 200 ml','Higiene Femenina',16000,50,8,'2028-09-30','L21031',0),
('HIG-PROT-RAD-032','Protectores diarios (30 unid)','Higiene Femenina',8000,90,15,'2029-08-05','L21032',0),

-- ============ NUTRICIÓN E HIDRATACIÓN ============
('NUT-PEDIA-500-033','Suero oral / Pedialyte 500 ml','Nutrición e Hidratación',8500,100,15,'2028-08-20','L28033',0),
('NUT-ELECT-350-034','Electrolitos en polvo (sobre)','Nutrición e Hidratación',3000,150,20,'2029-02-10','L28034',0),
('NUT-ENSU-400-035','Suplemento nutricional Ensure 400 g','Nutrición e Hidratación',48000,30,5,'2028-11-15','L28035',0),
('NUT-GLUC-400-036','Suplemento nutricional Glucerna 400 g','Nutrición e Hidratación',52000,25,5,'2028-12-10','L28036',0),

-- ============ VITAMINAS Y SUPLEMENTOS ============
('VIT-C-500-037','Vitamina C 500 mg (100 tabs)','Vitaminas',12000,80,15,'2028-11-10','L22037',0),
('VIT-D3-1000-038','Vitamina D3 1000 UI','Vitaminas',14000,75,15,'2028-12-15','L22038',0),
('VIT-COMPLEX-039','Complejo B jarabe 240 ml','Vitaminas',13000,70,12,'2029-01-20','L23039',0),
('VIT-MAG-040','Citrato de Magnesio 400 mg','Vitaminas',22000,60,10,'2029-02-25','L24040',0),
('VIT-OMEGA-041','Omega 3 1000 mg (60 cápsulas)','Vitaminas',25000,60,10,'2029-04-10','L26041',0),
('VIT-CAL-042','Calcio 600 mg + Vitamina D3','Vitaminas',16000,70,12,'2029-05-15','L27042',0),

-- ============ CUIDADO FACIAL Y DERMATOLÓGICO ============
('FAC-AGUA-043','Agua micelar 400 ml','Cuidado Facial',19000,50,10,'2028-06-15','L38043',0),
('FAC-LIMP-044','Limpiador facial espumoso 150 ml','Cuidado Facial',18000,60,10,'2028-07-20','L39044',0),
('FAC-SER-C-045','Sérum vitamina C 30 ml','Cuidado Facial',28000,40,5,'2028-09-30','L41045',0),
('FAC-SER-HA-046','Sérum ácido hialurónico 30 ml','Cuidado Facial',32000,35,5,'2028-10-10','L42046',0),
('FAC-PROT-047','Protector solar toque seco FPS 50+ 50 ml','Cuidado Facial',35000,45,8,'2028-11-15','L43047',0),

-- ============ CREMAS Y CORPORAL ============
('CRE-HID-400-048','Crema hidratante corporal 400 ml','Crema',24000,50,8,'2028-07-25','L28048',0),
('CRE-MANOS-049','Crema para manos y uñas 100 ml','Crema',9000,70,12,'2028-08-30','L29049',0),
('CRE-CALEN-050','Crema de caléndula 50 ml','Crema',10000,55,10,'2028-09-10','L30050',0),
('CRE-DERMAT-051','Crema con hidrocortisona 1% 30 g','Crema',12000,35,5,'2028-11-20','L32051',1),
('CRE-PAÑAL-052','Crema nystatina + zinc para pañalitis 100 g','Crema',14000,65,10,'2028-12-25','L33052',0),
('CRE-UREA-053','Crema corporal con urea 10% 200 g','Crema',18000,50,8,'2029-02-10','L34053',0),

-- ============ HIGIENE ORAL ============
('HIO-CEP-054','Cepillo dental cerdas suaves','Higiene Oral',5500,120,15,'2029-02-28','L46054',0),
('HIO-CREM-100-055','Crema dental anticaries 100 ml','Higiene Oral',6500,100,15,'2029-04-15','L48055',0),
('HIO-CREM-BLA-056','Crema dental blanqueadora 100 ml','Higiene Oral',9500,60,10,'2029-03-20','L121056',0),
('HIO-SEDA-057','Seda dental con cera 50 m','Higiene Oral',7500,90,12,'2029-06-25','L49057',0),
('HIO-ENJU-058','Enjuague bucal antiséptico 500 ml','Higiene Oral',14000,70,10,'2029-07-30','L50058',0),

-- ============ CUIDADO CAPILAR Y PERSONAL ============
('CAP-CHAMP-ANTI-059','Champú anticaspa 350 ml','Cuidado Capilar',16000,60,10,'2028-09-15','L52059',0),
('CAP-ACOND-060','Acondicionador hidratante 350 ml','Cuidado Capilar',15000,65,10,'2028-11-25','L54060',0),
('CAP-TRAT-061','Tratamiento capilar gusano de seda 250 ml','Cuidado Capilar',18000,40,8,'2028-12-30','L55061',0),
('DES-ROLL-062','Desodorante roll-on sin alcohol 50 ml','Cuidado Personal',9500,80,12,'2029-05-10','L56062',0),
('DES-SPRAY-063','Desodorante en aerosol 150 ml','Cuidado Personal',14000,70,10,'2029-06-15','L56063',0),

-- ============ BEBÉS Y MATERNIDAD ============
('BEB-PAÑAL-G-064','Pañales etapa 3 / Talla G (50 unid)','Bebés',29000,60,10,'2029-02-15','L57064',0),
('BEB-TOALL-065','Toallitas húmedas con aloe vera (80 unid)','Bebés',8000,80,15,'2029-04-25','L58065',0),
('BEB-CHAMP-066','Champú para bebé no más lágrimas 250 ml','Bebés',12000,65,10,'2029-06-10','L60066',0),
('BEB-BIBE-067','Biberón anticólicos 250 ml','Bebés',16000,50,8,'2029-07-15','L61067',0),
('BEB-FORM-1-068','Fórmula infantil Etapa 1 400 g','Bebés',38000,30,5,'2028-10-20','L62068',0),
('BEB-COMP-069','Compota de frutas mixtas 113 g','Bebés',3500,100,15,'2028-08-30','L62069',0),

-- ============ PRIMEROS AUXILIOS, OFTALMOLOGÍA Y OTORRINO ============
('AUX-ALCOHOL-070','Alcohol antiséptico 70% 500 ml','Primeros Auxilios',5000,80,15,'2028-10-30','L64070',0),
('AUX-OXIGEN-071','Agua oxigenada 250 ml','Primeros Auxilios',3500,90,15,'2028-11-10','L65071',0),
('AUX-GASA-072','Gasas estériles (10 unid)','Primeros Auxilios',4500,70,12,'2028-12-15','L66072',0),
('AUX-CURITA-073','Curitas adhesivas surtidas (20 unid)','Primeros Auxilios',3500,100,15,'2029-01-20','L67073',0),
('AUX-SUERO-074','Suero fisiológico 0.9% 500 ml','Primeros Auxilios',4500,60,10,'2029-05-15','L71074',0),
('OFT-LAGR-15-075','Lágrimas artificiales / Gotas oftálmicas 15 ml','Oftalmología',14000,50,8,'2028-09-10','L72075',0),
('OFT-SUER-NAS-076','Solución salina en spray nasal 50 ml','Otorrino',16000,45,8,'2028-11-10','L72076',0),

-- ============ DISPOSITIVOS MÉDICOS ============
('DIS-TERM-077','Termómetro digital de rápida lectura','Dispositivo Médico',18000,40,5,NULL,'L73077',0),
('DIS-TENS-078','Tensiómetro digital de brazo','Dispositivo Médico',85000,25,5,NULL,'L73078',0),
('DIS-GLUC-079','Glucómetro con kit de inicio','Dispositivo Médico',65000,20,5,NULL,'L74079',0),
('DIS-TIRAS-080','Tiras reactivas para glucómetro (50 unid)','Dispositivo Médico',32000,35,5,NULL,'L76080',0),
('DIS-OXIM-081','Oxímetro de pulso para dedo','Dispositivo Médico',45000,20,5,NULL,'L78081',0),
('DIS-TAPAB-082','Tapabocas termosellados (50 unid)','Dispositivo Médico',12000,70,10,NULL,'L80082',0),

-- ============ PRODUCTOS NATURALES E INFUSIONES ============
('NAT-MANZA-083','Té de manzanilla (20 bolsitas)','Productos Naturales',5500,80,15,'2028-12-10','L81083',0),
('NAT-VALE-084','Gotas de Valeriana 30 ml','Productos Naturales',8500,60,10,'2029-01-15','L82084',0),
('NAT-ALOE-085','Gel refrescante Aloe Vera 200 ml','Productos Naturales',11000,60,10,'2029-02-20','L83085',0),
('NAT-COCO-086','Aceite de coco extravirgen 250 ml','Productos Naturales',14000,50,8,'2029-03-25','L84086',0),
('NAT-CURC-087','Cúrcuma + Jengibre en cápsulas (60 caps)','Productos Naturales',18000,35,5,'2029-01-10','L119087',0);
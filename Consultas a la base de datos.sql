-- 1. Crear la base de datos (opcional, si aún no la tienes)
-- Usamos utf8mb4 para soportar emojis y caracteres especiales correctamente
CREATE DATABASE IF NOT EXISTS tienda_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. Seleccionar la base de datos para trabajar en ella
USE tienda_db;

-- 3. Crear la tabla PRODUCTO
-- Almacena la información de cada artículo disponible para la venta.
CREATE TABLE IF NOT EXISTS PRODUCTO (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL,
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 0
) ENGINE=InnoDB;

-- 4. Crear la tabla VENTA
-- Almacena la información de la "cabecera" de la venta (cuándo ocurrió).
CREATE TABLE IF NOT EXISTS VENTA (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 5. Crear la tabla DETALLE_VENTA (que implementa la relación 'CONTIENE')
-- Esta tabla une VENTAS y PRODUCTOS. Guarda cada línea de una venta:
-- qué producto se vendió, en qué cantidad y a qué precio en ese momento.
CREATE TABLE IF NOT EXISTS DETALLE_VENTA (
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    
    -- Definimos una clave primaria compuesta.
    -- Esto evita que el mismo producto se añada dos veces a la misma venta.
    PRIMARY KEY (id_venta, id_producto),
    
    -- Definimos las claves foráneas (Foreign Keys) para mantener la integridad
    CONSTRAINT fk_detalle_venta
        FOREIGN KEY (id_venta) 
        REFERENCES VENTA(id_venta)
        ON DELETE CASCADE -- Si se borra una venta, se borra su detalle
        ON UPDATE CASCADE,
        
    CONSTRAINT fk_detalle_producto
        FOREIGN KEY (id_producto) 
        REFERENCES PRODUCTO(id_producto)
        ON DELETE RESTRICT -- No permite borrar un producto si ya está en una venta
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS MEDIO_PAGO (
    id_medio_pago INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    facturar TINYINT(1) DEFAULT 0, -- 0: No factura, 1: Factura AFIP
    eliminado TINYINT(1) DEFAULT 0 -- Borrado lógico
) ENGINE=InnoDB;

SELECT * FROM PRODUCTO;

-- Asegúrate de estar usando la base de datos correcta
USE tienda_db;

SELECT
	*
FROM
	PRODUCTO
WHERE
	codigo = 'VAR-002';

-- Inserción de múltiples productos de librería y artículos escolares
INSERT INTO PRODUCTO 
    (codigo, nombre, descripcion, precio_venta, stock_actual, stock_minimo)
VALUES
    ('ESC-001', 'Cuaderno Rivadavia A4 Tapa Dura Rayado', 'Cuaderno A4 tapa dura, 100 hojas rayadas.', 8500.00, 150, 25),
    ('ESC-002', 'Birome BIC Trazo Fino Azul', 'Birome clásica BIC, color azul, trazo fino 1.0mm.', 1100.50, 500, 50),
    ('ESC-003', 'Lápiz Negro Faber-Castell HB', 'Lápiz de grafito HB, ideal para escritura y dibujo.', 950.00, 400, 50),
    ('ESC-004', 'Goma de Borrar Staedtler Blanca', 'Goma de borrar blanca de alta calidad, no deja mancha.', 1400.00, 300, 40),
    ('ESC-005', 'Resaltador Stabilo Boss Amarillo', 'Resaltador color amarillo fluorescente, punta biselada.', 2800.00, 200, 30),
    ('ESC-006', 'Carpeta 3 Anillos A4 Color Liso', 'Carpeta de 3 anillos tamaño A4, cubierta plástica color rojo.', 6200.00, 100, 15),
    ('ESC-007', 'Repuesto Hojas Rivadavia N°3 Rayado', 'Bloque de 96 hojas rayadas N°3 con banda reforzada.', 4500.00, 250, 30),
    ('ESC-008', 'Tijera Escolar Maped 13cm Punta Redonda', 'Tijera de 13cm con punta redonda, segura para niños.', 3100.00, 80, 10),
    ('LIB-001', 'El Aleph - Jorge Luis Borges', 'Colección de cuentos por Jorge Luis Borges. Edición de bolsillo.', 25500.00, 30, 5),
    ('LIB-002', 'Cien Años de Soledad - G. García Márquez', 'Novela clásica de Gabriel García Márquez. Tapa blanda.', 27800.00, 25, 5),
    ('VAR-001', 'Mochila Escolar Jansport Negra', 'Mochila Jansport clásica, color negro, un compartimento.', 95000.00, 20, 3),
    ('VAR-002', 'Cartuchera Canopla 2 Cierres', 'Cartuchera tipo canopla con dos compartimentos y cierres.', 18000.00, 60, 10),
    ('ESC-009', 'Sacapuntas Maped con Depósito', 'Sacapuntas plástico con depósito para virutas.', 1950.00, 150, 20),
    ('ESC-010', 'Set 12 Lápices de Colores Largos Faber-Castell', 'Caja de 12 lápices de colores, mina resistente.', 7200.00, 100, 15);

INSERT INTO PRODUCTO (codigo, nombre, descripcion, precio_venta, stock_actual, stock_minimo) VALUES
('NOTE-A4-100', 'Cuaderno A4 100 hojas', 'Cuaderno rayado de tamaño A4 con 100 hojas blancas', 450.00, 120, 10),
('NOTE-A5-70', 'Cuaderno A5 70 hojas', 'Cuaderno con tapas blandas y hojas lisas', 320.00, 200, 20),
('PEN-BIC-RT', 'Bolígrafo Bic Round Stic', 'Esfera negra con tinta azul', 80.00, 500, 50),
('PEN-PILOT-G2', 'Bolígrafo Pilot G2 0.7mm', 'Tinta gel suave y recargable', 250.00, 150, 30),
('PENC-FABER-CASTELL', 'Lápiz Faber-Castell 2B', 'Lápiz de grafito para dibujo y escritura', 70.00, 300, 40),
('MARK-STABILO-POINT88', 'Marcador Stabilo Point 88', 'Puntiagudo fino para subrayado y notas', 150.00, 180, 20),
('HIGHL-LUCI-FLUO', 'Resaltador Luci Fluo Amarillo', 'Alta visibilidad para resaltar textos', 110.00, 220, 30),
('GLUE-PATEX-50', 'Pegamento en barra Patex 50g', 'Barrita de pegamento sin olor', 130.00, 140, 25),
('SCIS-BOXER-13', 'Tijera Boxer 13 cm', 'Tijera pequeña con mango ergonómico', 95.00, 90, 15),
('ERAS-KOOL-PLAST', 'Goma de borrar Kool Plast', 'Goma blanda que no daña el papel', 60.00, 250, 30),
('SHARP-FABER-CASTELL', 'Sacapuntas Faber-Castell con depósito', 'Sacapuntas metálico con contenedor de viruta', 180.00, 110, 15),
('BOOK-BORGES-FICCION', 'Libro "Ficciones" de Borges', 'Colección de cuentos de JORGE LUIS BORGES', 1200.00, 50, 5),
('BOOK-CORTAZAR-RAYUELA', 'Libro "Rayuela" de Cortázar', 'Novela emblemática de JULIO CORTÁZAR', 1300.00, 40, 5),
('NOTE-QUILL-SKETCH', 'Cuaderno para dibujo Quill Sketch', 'Hojas de papel grueso para lápiz y acuarela', 850.00, 90, 10),
('COPY-PAPER-A4-500', 'Resma papel A4 500 hojas', 'Hoja blanca para impresora o copias', 3200.00, 30, 5);

INSERT INTO VENTA (fecha_hora) VALUES
('2025-11-01 09:15:00'),
('2025-11-01 17:40:00'),
('2025-11-02 10:05:00'),
('2025-11-03 14:30:00'),
('2025-11-04 11:22:00'),
('2025-11-05 18:45:00'),
('2025-11-06 08:55:00'),
('2025-11-07 19:10:00'),
('2025-11-08 12:40:00'),
('2025-11-10 16:25:00'),
('2025-11-12 09:50:00'),
('2025-11-14 13:15:00'),
('2025-11-18 11:05:00'),
('2025-11-20 17:55:00'),
('2025-11-25 10:33:00');

DELETE
FROM
	VENTA
WHERE
	id_venta NOT IN (SELECT
						DISTINCT id_venta
					FROM
						DETALLE_VENTA);

-- Nota: Asumimos que los id_venta 13-22 fueron creados en la tabla VENTA.
-- La columna 'precio_unitario' debe coincidir con el precio de venta del producto en ese momento.

SELECT * FROM VENTA;

SET SQL_SAFE_UPDATES = 0;

UPDATE PRODUCTO 
SET ventas_acumuladas = 0 
WHERE ventas_acumuladas IS NULL;

SET SQL_SAFE_UPDATES = 1;

SELECT
	V.id_venta,
    DV.id_producto
FROM
	DETALLE_VENTA AS DV
JOIN
	VENTA AS V ON V.id_venta = DV.id_venta;


SELECT * FROM PRODUCTO;

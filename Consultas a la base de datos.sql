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

SELECT * FROM PRODUCTO;

-- Asegúrate de estar usando la base de datos correcta
USE tienda_db;

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
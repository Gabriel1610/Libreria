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
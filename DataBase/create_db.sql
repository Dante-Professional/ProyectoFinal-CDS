USE notibolt;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    contrasegna VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS noticias (
    id_noticia INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_noticia DATE NOT NULL,
    autor VARCHAR(100),
    url VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS busquedas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fecha_busqueda DATE NOT NULL,
    id_usuario INT,
    id_noticia INT,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_noticia) REFERENCES noticias(id_noticia)
);
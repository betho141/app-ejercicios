import sqlite3

# Conectar a la base de datos (la crea si no existe)
conn = sqlite3.connect("rutinas_personalizadas.db")
cur = conn.cursor()

# Crear tabla de usuarios si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    nombre_clave TEXT PRIMARY KEY
)
""")

# Crear tabla de rutinas si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS rutinas (
    nombre_clave TEXT,
    id_ejercicio INTEGER,
    repeticiones INTEGER,
    series INTEGER,
    FOREIGN KEY (nombre_clave) REFERENCES usuarios(nombre_clave)
)
""")

conn.commit()
conn.close()

print("Base de datos inicializada correctamente.")

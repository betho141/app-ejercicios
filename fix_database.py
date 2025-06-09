import sqlite3

conn = sqlite3.connect("rutinas_personalizadas.db")
cur = conn.cursor()

# Mostrar tablas existentes
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = [row[0] for row in cur.fetchall()]
print("Tablas actuales:")
for t in tablas:
    print("-", t)

# Crear tabla usuarios si falta
if 'usuarios' not in tablas:
    cur.execute("""
    CREATE TABLE usuarios (
        nombre_clave TEXT PRIMARY KEY
    )
    """)
    print("✅ Tabla 'usuarios' creada.")

# Crear tabla rutinas si falta
if 'rutinas' not in tablas:
    cur.execute("""
    CREATE TABLE rutinas (
        nombre_clave TEXT,
        id_ejercicio INTEGER,
        repeticiones INTEGER,
        series INTEGER,
        FOREIGN KEY (nombre_clave) REFERENCES usuarios(nombre_clave)
    )
    """)
    print("✅ Tabla 'rutinas' creada.")

conn.commit()
conn.close()
print("✅ Base de datos lista para usarse.")

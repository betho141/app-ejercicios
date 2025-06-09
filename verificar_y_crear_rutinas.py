import sqlite3

conn = sqlite3.connect("rutinas_personalizadas.db")
cur = conn.cursor()

# Mostrar tablas existentes
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cur.fetchall()
print("Tablas actuales en la base de datos:")
for t in tablas:
    print("-", t[0])

# Crear tabla rutinas si no existe
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

print("Verificación completada. La tabla 'rutinas' existe o ha sido creada.")

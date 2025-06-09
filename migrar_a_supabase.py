
import sqlite3
import psycopg2

# Conexión a la base de datos SQLite local
sqlite_conn = sqlite3.connect("rutinas_personalizadas.db")
sqlite_cur = sqlite_conn.cursor()

# Leer datos de usuarios
sqlite_cur.execute("SELECT nombre_clave FROM usuarios")
usuarios = sqlite_cur.fetchall()

# Leer datos de rutinas
sqlite_cur.execute("SELECT nombre_clave, id_ejercicio, repeticiones, series FROM rutinas")
rutinas = sqlite_cur.fetchall()

sqlite_conn.close()

# Conexión a Supabase PostgreSQL
supabase_conn = psycopg2.connect(
    host="db.nwjuqqfsquvytbwslqrw.supabase.co",
    dbname="postgres",
    user="postgres",
    password="Dibujolavida141",
    port=5432
)
supabase_cur = supabase_conn.cursor()

# Insertar usuarios (ignorar duplicados)
for (nombre_clave,) in usuarios:
    try:
        supabase_cur.execute("INSERT INTO usuarios (nombre_clave) VALUES (%s) ON CONFLICT DO NOTHING", (nombre_clave,))
    except Exception as e:
        print("Error al insertar usuario:", nombre_clave, e)

# Insertar rutinas (ignorar duplicados exactos)
for nombre_clave, id_ejercicio, repeticiones, series in rutinas:
    try:
        supabase_cur.execute("""
        INSERT INTO rutinas (nombre_clave, id_ejercicio, repeticiones, series)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        """, (nombre_clave, id_ejercicio, repeticiones, series))
    except Exception as e:
        print("Error al insertar rutina:", nombre_clave, e)

supabase_conn.commit()
supabase_cur.close()
supabase_conn.close()

print("✅ Migración completada con éxito.")

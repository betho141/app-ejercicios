
import streamlit as st
import psycopg2
import pandas as pd
import webbrowser

# --- CONFIGURACIÓN DE CONEXIÓN A SUPABASE ---
def get_connection():
    return psycopg2.connect(
        host="aws-0-us-east-2.pooler.supabase.com",
        dbname="postgres",
        user="postgres.nwjuqqfsquvytbwslqrw",
        password="Dibujolavida141",
        port=6543
    )

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="App Rutinas Supabase", layout="wide")

# --- CARGAR EJERCICIOS DESDE SUPABASE ---
@st.cache_data
def cargar_ejercicios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, url, zona_corporal, implemento, articularidad FROM ejercicios")
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=colnames)
    cur.close()
    conn.close()
    return df

df_ejercicios = cargar_ejercicios()

# --- OBTENER RUTINA DE USUARIO ---
def obtener_rutina(nombre_clave):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_ejercicio, repeticiones, series FROM rutinas WHERE nombre_clave = %s", (nombre_clave,))
    datos = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(datos, columns=["id_ejercicio", "repeticiones", "series"])

# --- INICIO APP ---
modo = st.sidebar.radio("Selecciona el modo:", ["Usuario", "Administrador"])

if modo == "Usuario":
    nombre_usuario = st.sidebar.text_input("Ingresa tu nombre_clave")
    if nombre_usuario:
        st.title(f"Rutina personalizada para {nombre_usuario}")
        df_rutina = obtener_rutina(nombre_usuario)
        if not df_rutina.empty:
            df_final = df_rutina.merge(df_ejercicios, left_on="id_ejercicio", right_on="id")
            for _, row in df_final.iterrows():
                st.markdown(f"**{row['nombre']}**")
                st.markdown(f"Repeticiones: {row['repeticiones']} | Series: {row['series']}")
                st.markdown(f"[🔗 Ver video de {row['nombre']}]({row['url']})", unsafe_allow_html=True)
                # if st.button(f"Ver Video de {row['nombre']}", key=row['id']):
                #    webbrowser.open_new_tab(row['url'])
        else:
            st.warning("No se encontraron ejercicios asignados.")

elif modo == "Administrador":
    password = st.sidebar.text_input("Contraseña secreta", type="password")
    if password == "dioses123":
        st.title("Panel de Administrador")
        conn = get_connection()
        cur = conn.cursor()

        # Crear nuevo usuario
        st.markdown("### ➕ Crear nuevo usuario")
        nuevo_nombre = st.text_input("Nombre_clave nuevo")
        if st.button("Agregar usuario"):
            if nuevo_nombre:
                try:
                    cur.execute("INSERT INTO usuarios (nombre_clave) VALUES (%s) ON CONFLICT DO NOTHING", (nuevo_nombre,))
                    conn.commit()
                    st.success(f"Usuario '{nuevo_nombre}' creado.")
                except Exception as e:
                    st.error("Error al crear usuario: " + str(e))

        # Cargar usuarios
        cur.execute("SELECT nombre_clave FROM usuarios")
        usuarios = [row[0] for row in cur.fetchall()]

        # Eliminar usuario
        st.markdown("### ❌ Eliminar usuario")
        usuario_eliminar = st.selectbox("Seleccionar usuario", usuarios)
        if st.button("Eliminar usuario"):
            cur.execute("DELETE FROM rutinas WHERE nombre_clave = %s", (usuario_eliminar,))
            cur.execute("DELETE FROM usuarios WHERE nombre_clave = %s", (usuario_eliminar,))
            conn.commit()
            st.success(f"Usuario '{usuario_eliminar}' eliminado.")

        # Asignar rutina
        st.markdown("### ✏️ Asignar ejercicios personalizados")
        usuario_seleccionado = st.selectbox("Selecciona usuario", usuarios, key="mod")

        zona_filtro = st.selectbox("Filtrar por zona corporal", ["Todas"] + sorted(df_ejercicios["zona_corporal"].dropna().unique()))
        implemento_filtro = st.selectbox("Filtrar por implemento", ["Todos"] + sorted(df_ejercicios["implemento"].dropna().unique()))

        df_filtrado = df_ejercicios.copy()
        if zona_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado["zona_corporal"] == zona_filtro]
        if implemento_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado["implemento"] == implemento_filtro]

        ejercicios_seleccionados = st.multiselect("Selecciona ejercicios", df_filtrado["nombre"].tolist())
        repeticiones = st.number_input("N° Repeticiones", min_value=1, max_value=100, value=10)
        series = st.number_input("N° Series", min_value=1, max_value=20, value=3)

        if st.button("Guardar rutina personalizada"):
            cur.execute("DELETE FROM rutinas WHERE nombre_clave = %s", (usuario_seleccionado,))
            for nombre_ejercicio in ejercicios_seleccionados:
                id_ej = int(df_ejercicios[df_ejercicios["nombre"] == nombre_ejercicio]["id"].values[0])
                cur.execute("INSERT INTO rutinas (nombre_clave, id_ejercicio, repeticiones, series) VALUES (%s, %s, %s, %s)",
                            (usuario_seleccionado, id_ej, repeticiones, series))
            conn.commit()
            st.success("Rutina guardada exitosamente.")

        cur.close()
        conn.close()
    else:
        st.warning("Contraseña incorrecta")

import streamlit as st
import json
from datetime import datetime

def generar_backup_completo(db):
    data = {
        "usuarios": db.get_usuarios(),
        "fases": db.get_fases(),
        "partidos": db.get_partidos(),
        "resultados": db.get_resultados(),
        "prodes": db.get_prodes(),
        "especiales": db.get_especiales(),
        "resultados_especiales": db.get_resultados_especiales(),
        "config": db.get_config(),
        "consumo_log": db.get_consumo_log(),
        "actividad": db.get_actividad(),
    }
    return data

def generar_backup_fase(db, fase_id):
    data = {
        "fase_id": fase_id,
        "partidos": db.get_partidos(fase_id),
        "resultados": db.get_resultados(fase_id),
        "prodes": db.get_prodes(fase_id),
        "especiales": db.get_especiales(fase_id),
        "resultados_especiales": db.get_resultados_especiales(fase_id),
    }
    return data

def restaurar_backup(db, data):
    if "usuarios" in data:
        db.replace_usuarios(data["usuarios"])
    if "fases" in data:
        db.replace_fases(data["fases"])
    if "partidos" in data:
        db.replace_partidos(data["partidos"])
    if "resultados" in data:
        db.replace_resultados(data["resultados"])
    if "prodes" in data:
        db.replace_prodes(data["prodes"])
    if "especiales" in data:
        db.replace_especiales(data["especiales"])
    if "resultados_especiales" in data:
        db.replace_resultados_especiales(data["resultados_especiales"])
    if "config" in data:
        db.replace_config(data["config"])
    if "consumo_log" in data:
        db.replace_consumo_log(data["consumo_log"])
    if "actividad" in data:
        db.replace_actividad(data["actividad"])

def render_admin_exportar(db):
    st.title("Exportar / Backups")

    st.subheader("Backup completo")
    if st.button("Descargar backup completo (JSON)"):
        data = generar_backup_completo(db)
        json_str = json.dumps(data, indent=2, ensure_ascii=False)

        st.download_button(
            label="Descargar archivo",
            data=json_str,
            file_name=f"backup_completo_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json",
            mime="application/json"
        )

    st.subheader("Backup por fase")
    fases = db.get_fases()
    fase_dict = {f["nombre"]: f["id"] for f in fases}

    fase_nombre = st.selectbox("Seleccionar fase", list(fase_dict.keys()))

    if st.button("Descargar backup de fase"):
        fase_id = fase_dict[fase_nombre]
        data = generar_backup_fase(db, fase_id)
        json_str = json.dumps(data, indent=2, ensure_ascii=False)

        st.download_button(
            label="Descargar archivo fase",
            data=json_str,
            file_name=f"backup_fase_{fase_nombre}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json",
            mime="application/json"
        )

    st.subheader("Restaurar backup")
    uploaded_file = st.file_uploader("Subir archivo JSON", type=["json"])

    confirm = st.text_input("Escribí RESTAURAR para confirmar")

    if uploaded_file and confirm == "RESTAURAR":
        data = json.load(uploaded_file)
        restaurar_backup(db, data)
        st.success("Backup restaurado correctamente")

import streamlit as st
import json
from datetime import datetime

def generar_backup_completo(db):
    return {
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

def generar_backup_fase(db, fase_id):
    return {
        "fase_id": fase_id,
        "partidos": db.get_partidos(fase_id),
        "resultados": db.get_resultados(fase_id),
        "prodes": db.get_prodes(fase_id),
        "especiales": db.get_especiales(fase_id),
        "resultados_especiales": db.get_resultados_especiales(fase_id),
    }

def restaurar_backup(db, data):
    if "usuarios" in data: db.replace_usuarios(data["usuarios"])
    if "fases" in data: db.replace_fases(data["fases"])
    if "partidos" in data: db.replace_partidos(data["partidos"])
    if "resultados" in data: db.replace_resultados(data["resultados"])
    if "prodes" in data: db.replace_prodes(data["prodes"])
    if "especiales" in data: db.replace_especiales(data["especiales"])
    if "resultados_especiales" in data: db.replace_resultados_especiales(data["resultados_especiales"])
    if "config" in data: db.replace_config(data["config"])
    if "consumo_log" in data: db.replace_consumo_log(data["consumo_log"])
    if "actividad" in data: db.replace_actividad(data["actividad"])

def pantalla_admin(db):
    st.title("Backups")

    st.subheader("Backup completo")
    data = generar_backup_completo(db)
    st.download_button(
        "Descargar backup completo",
        json.dumps(data, indent=2, ensure_ascii=False),
        file_name=f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json",
        mime="application/json"
    )

    st.subheader("Backup por fase")
    fases = db.get_fases()
    if fases:
        fdict = {f["nombre"]: f["id"] for f in fases}
        nombre = st.selectbox("Fase", list(fdict.keys()))
        data_f = generar_backup_fase(db, fdict[nombre])
        st.download_button(
            "Descargar backup fase",
            json.dumps(data_f, indent=2, ensure_ascii=False),
            file_name=f"backup_fase_{nombre}.json",
            mime="application/json"
        )

    st.subheader("Restaurar backup")
    file = st.file_uploader("Subir JSON", type=["json"])
    confirm = st.text_input("Escribí RESTAURAR")

    if file and confirm == "RESTAURAR":
        restaurar_backup(db, json.load(file))
        st.success("Backup restaurado")

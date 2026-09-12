import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Informe Ejecutivo de Producción", layout="wide"
)

st.title("📊 Panel de Control y Producción")
st.markdown("Visualización en tiempo real del archivo de Excel institucional.")

# Ruta de tu archivo excel en el repositorio
archivo_excel = "informebimbo.xlsx"

# Cargar todas las hojas del archivo
try:
  excel_data = pd.read_excel(archivo_excel, sheet_name=None)
  nombres_hojas = list(excel_data.keys())

  # Crear pestañas en Streamlit basadas en las hojas del Excel
  pestanas = st.tabs(nombres_hojas)

  for i, nombre_hoja in enumerate(nombres_hojas):
    with pestanas[i]:
      st.subheader(f"Vista de la hoja: {nombre_hoja}")
      df = excel_data[nombre_hoja]

      # Mostrar la tabla de datos de la hoja correspondiente
      st.dataframe(df, use_container_width=True)

      # Si es la hoja de informe ejecutivo, puedes destacar métricas
      if "INFORME" in nombre_hoja.upper() or "RESUMEN" in nombre_hoja.upper():
        st.info(
            "Sección clave del informe ejecutivo cargada correctamente desde"
            " la nube."
        )

except Exception as e:
  st.error(
      f"Error al cargar el archivo de Excel. Asegúrate de que esté en la"
      f" ruta correcta. Detalle: {e}"
  )

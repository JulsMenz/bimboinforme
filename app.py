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

      # Si es la hoja de RESUMEN o INFORME, aplicamos estilos de semáforo
      if (
          "RESUMEN" in nombre_hoja.upper()
          or "INFORME" in nombre_hoja.upper()
      ):
        st.markdown(
            "(Vista con formato condicional tipo semáforo aplicado)"
        )

        # Intentamos aplicar colores estilo semáforo a columnas numéricas
        # Puedes ajustar 'cmap' (ej. 'RdYlGn' rojo-amarillo-verde o 'Greens')
        try:
          # st.dataframe acepta estilos de pandas Styler
          df_estilizado = df.style.background_gradient(
              cmap="RdYlGn", subset=df.select_dtypes(include="number").columns
          )
          st.dataframe(df_estilizado, use_container_width=True)
        except Exception:
          # Si falla por algún tipo de dato, muestra la tabla normal
          st.dataframe(df, use_container_width=True)
      else:
        # Mostrar la tabla estándar para las demás hojas
        st.dataframe(df, use_container_width=True)

except Exception as e:
  st.error(
      f"Error al cargar el archivo de Excel. Asegúrate de que esté en la"
      f" ruta correcta. Detalle: {e}"
  )

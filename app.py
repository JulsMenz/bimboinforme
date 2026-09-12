import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Informe Ejecutivo de Producción", layout="wide"
)

st.title("📊 Panel de Control y Producción")
st.markdown("Visualización en tiempo real del archivo de Excel institucional.")

archivo_excel = "informebimbo.xlsx"


# Función para aplicar colores tipo semáforo personalizados
def aplicar_semaforo(val):
  """Aplica color de fondo verde o rojo según el texto o valor numérico."""
  if isinstance(val, str):
    val_upper = val.upper()
    if (
        "CUMPLE" in val_upper
        and "NO" not in val_upper
        and "ALERTA" not in val_upper
    ):
      return "background-color: #d4edda; color: #155724; font-weight: bold;"  # Verde suave
    elif "ALERTA" in val_upper or "NO CUMPLE" in val_upper:
      return "background-color: #f8d7da; color: #721c24; font-weight: bold;"  # Rojo suave
  return ""


try:
  excel_data = pd.read_excel(archivo_excel, sheet_name=None)
  nombres_hojas = list(excel_data.keys())

  pestanas = st.tabs(nombres_hojas)

  for i, nombre_hoja in enumerate(nombres_hojas):
    with pestanas[i]:
      st.subheader(f"Vista de la hoja: {nombre_hoja}")
      df = excel_data[nombre_hoja]

      if (
          "RESUMEN" in nombre_hoja.upper()
          or "INFORME" in nombre_hoja.upper()
      ):
        st.markdown(
            "(Vista con formato condicional de semáforo aplicado)"
        )
        try:
          # Aplicamos el estilo de semáforo a todo el DataFrame buscando palabras clave como CUMPLE / ALERTA
          df_estilizado = df.style.map(aplicar_semaforo)
          st.dataframe(df_estilizado, use_container_width=True)
        except Exception as e:
          # Fallback por si la versión de pandas es anterior y usa .applymap() en lugar de .map()
          try:
            df_estilizado = df.applymap(aplicar_semaforo)
            st.dataframe(df_estilizado, use_container_width=True)
          except Exception:
            st.dataframe(df, use_container_width=True)
      else:
        st.dataframe(df, use_container_width=True)

except Exception as e:
  st.error(
      f"Error al cargar el archivo de Excel. Asegúrate de que esté en la"
      f" ruta correcta. Detalle: {e}"
  )

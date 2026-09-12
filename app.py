import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Informe Ejecutivo de Producción", layout="wide"
)

st.title("📊 Panel de Control y Producción")
st.markdown("Visualización en tiempo real del archivo de Excel institucional.")

archivo_excel = "informebimbo.xlsx"


def aplicar_semaforo_general(val):
  """Evalúa cualquier celda: si encuentra texto de estado o números críticos los colorea."""
  if pd.isna(val):
    return ""

  val_str = str(val).strip().upper()

  # 1. Validación por texto de estado
  if "CUMPLE" in val_str and "NO" not in val_str and "ALERTA" not in val_str:
    return "background-color: #d4edda; color: #155724; font-weight: bold;"  # Verde
  elif "ALERTA" in val_str or "NO CUMPLE" in val_str:
    return "background-color: #f8d7da; color: #721c24; font-weight: bold;"  # Rojo

  # 2. Validación numérica opcional para porcentajes o resultados bajos/altos si es necesario
  try:
    num = float(val)
    # Si detecta valores menores a 1 (ej. porcentajes de desperdicio altos o cumplimiento bajo)
    # Puedes ajustar esta regla según la lógica de tus métricas
  except ValueError:
    pass

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
            "*(Vista con formato condicional de semáforo aplicado)*"
        )
        try:
          # Limpiamos un poco el dataframe para asegurarnos de que aplique el estilo
          df_estilizado = df.style.map(aplicar_semaforo_general)
          st.dataframe(df_estilizado, use_container_width=True)
        except Exception:
          try:
            df_estilizado = df.applymap(aplicar_semaforo_general)
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

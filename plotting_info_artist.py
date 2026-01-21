import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import re

# === Función para nombres de hoja coherentes ===
def safe_sheet_name(base, suffix):
    name = re.sub(r'[\\/*?:\[\]]', '', base).strip()[:15]  # solo primeros 15 caracteres
    full_name = f"{name}_{suffix}"
    return full_name

# Obtener nombre de la carpeta desde argumentos (GitHub Actions)
folder_name = sys.argv[1] if len(sys.argv) > 1 else "pdf_artistas"

archivo = "top10_artistas_detalle.xlsx"
xls = pd.ExcelFile(archivo)
os.makedirs(folder_name, exist_ok=True)

# --- Detectar artistas automáticamente ---
artistas = {}
for sheet in xls.sheet_names:
    if "_" in sheet:
        artista, tipo = sheet.rsplit("_", 1)
        if artista not in artistas:
            artistas[artista] = {}
        artistas[artista][tipo] = sheet

# --- Generar PDFs ---
for artista, hojas in artistas.items():
    if all(k in hojas for k in ["visitas", "ciudades", "canciones"]):
        try:
            df_visitas = pd.read_excel(archivo, sheet_name=safe_sheet_name(artista, "visitas"))
            df_ciudades = pd.read_excel(archivo, sheet_name=safe_sheet_name(artista, "ciudades"))
            df_canciones = pd.read_excel(archivo, sheet_name=safe_sheet_name(artista, "canciones"))

            pdf_path = os.path.join(folder_name, f"{artista.replace('/', '_')}.pdf")
            with PdfPages(pdf_path) as pdf:

                # --- Gráfico 1: Visitas ---
                plt.figure(figsize=(20,10))

                # Diccionario para traducir meses de Español a Inglés
                meses_map = {
                    'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr', 
                    'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug', 
                    'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
                }

                # Función auxiliar para limpiar y traducir la fecha
                def limpiar_fecha(fecha):
                    if pd.isna(fecha): return fecha
                    fecha = str(fecha).replace('.', '').lower() # Quitar puntos y pasar a minúsculas
                    for mes_es, mes_en in meses_map.items():
                        if mes_es in fecha:
                            return fecha.replace(mes_es, mes_en)
                    return fecha

                # 1. Aplicar la traducción
                df_visitas["Fecha_Str"] = df_visitas["Fecha"].apply(limpiar_fecha)

                # 2. Convertir a datetime usando los meses en inglés
                df_visitas["Fecha"] = pd.to_datetime(
                    df_visitas["Fecha_Str"], 
                    format="%d %b %Y", 
                    errors='coerce'
                )
                
                # Verificar si hay datos válidos antes de graficar
                df_visitas = df_visitas.dropna(subset=["Fecha"])
                
                if not df_visitas.empty:
                    # Ordenar por fecha 
                    df_visitas = df_visitas.sort_values("Fecha")
                    
                    # Convertir Visitas a numérico limpiando separadores de miles
                    def limpiar_visitas(valor):
                        if pd.isna(valor):
                            return float('nan')
                        valor = str(valor).strip()
                        # Las comas son separadores de miles, simplemente removerlas
                        valor = valor.replace(',', '')
                        try:
                            return float(valor)
                        except:
                            return float('nan')
                    
                    df_visitas["Visitas_num"] = df_visitas["Visitas"].apply(limpiar_visitas)
                    
                    
                    # Filtrar solo filas con datos válidos en fecha y visitas
                    df_valido = df_visitas.dropna(subset=["Fecha", "Visitas_num"]).copy()
                    
                    if not df_valido.empty:
                        df_valido["Dia_Mes"] = df_valido["Fecha"].dt.strftime("%d-%m")
                        
                        # Graficar
                        plt.figure(figsize=(20, 10))
                        # Convertir a millones para mejor visualización
                        visitas_millones = df_valido["Visitas_num"] / 1_000_000
                        plt.plot(range(len(df_valido)), visitas_millones.values, marker='o', linewidth=2)
                        plt.title(f"Visitas Diarias - {artista}", fontsize=16)
                        plt.xlabel("Fecha", fontsize=12)
                        plt.ylabel("Visitas (Millones)", fontsize=12)
                        
                        # Mostrar etiquetas de fecha cada N puntos para evitar saturación
                        step = max(1, len(df_valido) // 10)
                        plt.xticks(range(0, len(df_valido), step), 
                                  df_valido["Dia_Mes"].values[::step], rotation=45)
                        plt.grid(True, alpha=0.3)
                        plt.tight_layout()
                        pdf.savefig()
                    else:
                        print(f"⚠️ Aviso: No hay datos válidos de visitas para {artista}")
                    
                    plt.close()


                # --- Gráfico 2: Ciudades ---
                plt.figure(figsize=(16,10))
                
                def convertir_visitas(valor):
                    if pd.isna(valor):
                        return 0
                    valor = str(valor).strip().upper()
                    try:
                        if 'K' in valor:
                            return float(valor.replace('K', '')) * 1000
                        elif 'M' in valor:
                            return float(valor.replace('M', '')) * 1_000_000
                        else:
                            return float(valor)
                    except:
                        return 0
                
                df_ciudades["Visitas"] = df_ciudades["Visitas"].apply(convertir_visitas)
                df_ciudades.rename(columns={"Visitas": "Visitas(en millones)"}, inplace=True)
                sns.barplot(data=df_ciudades, x="Ciudad", y="Visitas(en millones)", hue="Ciudad")
                plt.title(f"Top 10 Ciudades - {artista}")
                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig()
                plt.close()

                # --- Gráfico 3: Canciones ---
                plt.figure(figsize=(16,10))
                
                def convertir_visitas(valor):
                    if pd.isna(valor):
                        return 0
                    valor = str(valor).strip().upper()
                    try:
                        if 'K' in valor:
                            return float(valor.replace('K', '')) * 1000
                        elif 'M' in valor:
                            return float(valor.replace('M', '')) * 1_000_000
                        else:
                            return float(valor)
                    except:
                        return 0
                
                df_canciones["Visitas"] = df_canciones["Visitas"].apply(convertir_visitas)
                sns.barplot(data=df_canciones, y="Canción", x="Visitas", hue="Canción", legend=False)
                plt.title(f"Top 10 Canciones - {artista}")
                plt.tight_layout()
                pdf.savefig()
                plt.close()

            print(f"✅ PDF creado: {pdf_path}")

        except Exception as e:
            print(f"⚠️ Error con artista {artista}: {e}")
    else:
        print(f"⚠️ Saltando {artista}: faltan hojas completas")

print("✅ Todos los PDFs generados.")

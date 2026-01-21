# YouTube Charts Scraping - Colombia 🎵

Automatiza la extracción de datos de [YouTube Charts Colombia](https://charts.youtube.com/charts/TopArtists/co/weekly) generando gráficos y reportes PDF de los artistas más populares.

## 🎯 Características

- 📊 Extrae el **top 10 artistas semanales** de Colombia
- 📈 Genera **visualizaciones y PDFs** con datos por artista
- 🤖 Se ejecuta **automáticamente cada martes** en GitHub Actions
- 📁 Organiza datos en **Excel con múltiples hojas** (visitas, ciudades, canciones)
- 📦 Guarda PDFs en **carpetas incrementales** para histórico

## 📋 Requisitos

- Python 3.10+
- Las dependencias listadas en `requirements.txt`
- Git (para subir a GitHub)

```

## 🚀 Uso

El proyecto tiene 3 scripts que se ejecutan en orden:

### 1️⃣ Extraer artistas top 10
```bash
python extract_info_artists.py
```
**Salida:** `top_colombia_weekly_artists.csv`

### 2️⃣ Extraer datos detallados por artista
```bash
python extract_info_per_artist.py
```
**Salida:** `top10_artistas_detalle.xlsx` (múltiples hojas por artista)

### 3️⃣ Generar PDFs con gráficos
```bash
python plotting_info_artist.py
```
O con carpeta personalizada:
```bash
python plotting_info_artist.py "pdf_artistas_custom"
```
**Salida:** PDFs en carpeta `pdf_artistas/`

### ▶️ Ejecutar todo de una vez
```bash
python extract_info_artists.py && python extract_info_per_artist.py && python plotting_info_artist.py
```

## 🤖 Automatización en GitHub

El proyecto incluye un **workflow automático** que se ejecuta:
- **Cada martes a las 5:00 PM (hora Colombia)**
- **Manualmente**: GitHub → Actions → "Automatizar scripts de artistas" → "Run workflow"



El workflow automáticamente:
- ✅ Clona el repo
- ✅ Instala dependencias
- ✅ Ejecuta los 3 scripts
- ✅ Crea carpetas incremental (pdf_artistas1, pdf_artistas2, etc.)
- ✅ Sube PDFs al repositorio
- ✅ Guarda artefactos descargables


```

## 📊 Datos Generados


### top10_artistas_detalle.xlsx
Múltiples hojas por artista:
- **Visitas**: Datos diarios de visualizaciones
- **Ciudades**: Top 10 ciudades con más visualizaciones
- **Canciones**: Top 10 canciones del artista

### pdf_artistas/
PDFs con 3 gráficos por artista:
1. 📈 **Gráfico de Visitas**: Evolución diaria
2. 📊 **Gráfico de Ciudades**: Top 10 ciudades
3. 🎵 **Gráfico de Canciones**: Top 10 canciones

## 🔧 Tecnologías Usadas

- **Playwright**: Web scraping automatizado
- **Pandas**: Procesamiento de datos
- **Matplotlib & Seaborn**: Visualizaciones
- **XlsxWriter**: Generación de Excel
- **GitHub Actions**: Automatización

## 📝 Notas

- Los datos se extraen de YouTube Charts oficial
- Las carpetas de PDF se crean incrementalmente (pdf_artistas1, pdf_artistas2, etc.)
- El script maneja automáticamente errores de conexión
- Genera logs con ✅ y ⚠️ para seguimiento fácil


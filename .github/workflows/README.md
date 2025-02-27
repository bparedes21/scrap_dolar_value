# 🌐 Web Scraping Automation

Este proyecto automatiza la extracción de datos del dólar blue mediante el uso de scripts de scraping y GitHub Actions. Los datos obtenidos se procesan y representan visualmente para proporcionar información útil sobre los valores actuales y su evolución histórica.

- **Acceso a los datos crudos (JSON):** [Dólar Blue JSON](https://raw.githubusercontent.com/bparedes21/scrap_dolar_value/main/dolar_data.json)
- **Aplicación que consume los datos:** [Valor del Dólar Ambito Financiero](https://flask-ambito-usd-venta.vercel.app/)


## ✨ Funcionalidades Principales

- 🛠️ Extracción automática de datos a través de scripts Python.
- 🤖 Automatización de ejecución mediante GitHub Actions.
- 📊 Generación de gráficos representativos para analizar tendencias.
- 🌈 Clasificación de valores en diferentes rangos y colores para facilitar la interpretación.

## 🔧 Requisitos Previos

- 🐍 Python 3.9 o superior.
- 📦 Dependencias instaladas:
  - `playwright`

## ⚙️ Ejecución Automática

El flujo de trabajo de GitHub Actions se ejecuta automáticamente cada hora entre las 09:00 y las 19:00 UTC-3 (12:00 y 22:00 UTC). La configuración del cronograma está definida de la siguiente manera:

```yaml
on:
  schedule:
    - cron: '0 12 * * *'  # Ejecución cada hora entre 12:00 y 21:00 UTC
    - cron: '0 13 * * *'
    - cron: '0 14 * * *'
    - cron: '0 15 * * *'
    - cron: '0 16 * * *'
    - cron: '0 17 * * *'
    - cron: '0 18 * * *'
    - cron: '0 19 * * *'
```

## 🃏 Clasificación de las Tarjetas

Las tarjetas son una representación visual de los datos procesados, y se utilizan para resaltar información importante de manera intuitiva. Cada tarjeta incluye los valores procesados y se clasifica en diferentes categorías según rangos definidos, utilizando colores específicos para facilitar su identificación:

### 🔴 card alto (rojo)
Indica un valor crítico o elevado, correspondiente a valores iguales o superiores a 1200.
- **Ejemplo de uso**: Cuando la venta supera el umbral de 1200, se clasifica como "alto".

### 🟡 card medio (amarillo)
Representa valores moderados dentro del rango de 1100 a 1199.99.
- **Ejemplo de uso**: El promedio del dólar se encuentra en el rango medio.

### 🟢 card bajo (verde)
Señala valores considerados bajos, es decir, menores a 1100.
- **Ejemplo de uso**: Si el valor de compra está por debajo de este umbral.

### ⚪ card no-disponible (gris)
Se asigna cuando no se puede determinar un valor válido, como en casos de datos faltantes o errores en el formato.
- **Ejemplo de uso**: Si no se encuentra información sobre el valor de venta o compra.

#### Ejemplo visual:

| 🃏 Tarjeta          | 💰 Valor | 🌈 Color |
|--------------------|----------|----------|
| Venta (alto)       | 1250     | 🔴 Rojo  |
| Promedio (medio)   | 1150     | 🟡 Amarillo |
| Compra (bajo)      | 1050     | 🟢 Verde  |
| Venta (no disponible) | -        | ⚪ Gris   |


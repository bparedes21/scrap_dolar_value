# 🌐 Web Scraping Automation

Este proyecto automatiza la extracción de datos del dólar blue de **AmbitoFinanciero.com** mediante el uso de scripts de scraping y **GitHub Actions**. Los datos obtenidos se procesan y representan visualmente para proporcionar información útil sobre los valores actuales y su evolución histórica.

## ✨ Funcionalidades Principales

- 🛠️ **Extracción automática** de datos a través de scripts Python.
- 🤖 **Automatización de ejecución** mediante **GitHub Actions**.

## 🌟 Proyecto Complementario
Este proyecto de web scraping está complementado por una 👉 [****aplicación web en Flask****](https://github.com/bparedes21/flask-ambito-usd-venta) que permite consultar el valor actual del dólar blue, visualizar su histórico y explorar gráficos interactivos. 

Puedes acceder a la aplicación web en vivo aquí:  
👉 [**App Web en Flask**](https://flask-ambito-usd-venta.vercel.app/)

Este complemento permite una experiencia completa donde los datos extraídos son presentados de manera visual y dinámica.

## 🔧 Requisitos Previos

- 🐍 **Python 3.9** o superior.
- 📦 Dependencias instaladas:
  - `playwright`

## ⚙️ Ejecución Automática

El flujo de trabajo de **GitHub Actions** se ejecuta automáticamente cada hora entre las 09:00 y las 19:00 UTC-3 (12:00 y 22:00 UTC). La configuración del cronograma está definida de la siguiente manera:

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

import json
import os
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

# Ruta del archivo para guardar los datos
FILE_PATH = "dolar_data.txt"
LAST_DATE_FILE = "last_date.txt"

def get_current_date():
    """Obtiene la fecha actual en formato AAAA-MM-DD (UTC-3)."""
    utc_now = datetime.utcnow()
    utc_minus_3 = utc_now - timedelta(hours=3)
    return utc_minus_3.strftime('%Y-%m-%d')

def clear_file_if_new_day():
    """Borra el archivo si ha cambiado el día."""
    current_date = get_current_date()

    # Verificar si existe el archivo de fecha
    if os.path.exists(LAST_DATE_FILE):
        with open(LAST_DATE_FILE, mode="r", encoding="utf-8") as date_file:
            last_date = date_file.read().strip()
    else:
        last_date = None

    # Si es un nuevo día, limpiar el archivo y guardar la nueva fecha
    if current_date != last_date:
        open(FILE_PATH, mode="w", encoding="utf-8").close()  # Limpiar contenido del archivo
        with open(LAST_DATE_FILE, mode="w", encoding="utf-8") as date_file:
            date_file.write(current_date)

def append_data_to_file(data):
    """Agrega los datos al archivo de texto."""
    with open(FILE_PATH, mode="a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")

def scrape_website():
    try:
        clear_file_if_new_day()  # Verificar si se necesita reiniciar el archivo

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            url = 'https://www.ambito.com/contenidos/dolar.html'
            print(f"📡 Cargando la página: {url}")
            
            for attempt in range(5):
                try:
                    page.goto(url, timeout=120000, wait_until="load")
                    page.wait_for_selector('.variation-max-min__value.data-valor.data-compra', timeout=60000)
                    break
                except Exception as e:
                    print(f"🔁 Reintentando la carga de la página ({attempt+1}/5)...")
                    if attempt == 4:
                        raise e

            compra = page.locator(".variation-max-min__value.data-valor.data-compra").first.text_content()
            venta = page.locator(".variation-max-min__value.data-valor.data-venta").first.text_content()

            print(f'💸 Valor de compra: {compra}')
            print(f'💸 Valor de venta: {venta}')

            # Capturar la hora actual en UTC-3
            fecha_hora_utc3 = datetime.utcnow() - timedelta(hours=3)
            fecha_hora_utc3_str = fecha_hora_utc3.strftime('%Y-%m-%d %H:%M:%S')

            # Estructura del archivo
            data = {
                'fecha_hora_utc3': fecha_hora_utc3_str,
                'compra': compra,
                'venta': venta
            }

            # Agregar al archivo de texto
            append_data_to_file(data)

            print(f"✅ Datos guardados en '{FILE_PATH}' con la fecha/hora {fecha_hora_utc3_str}")

    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

if __name__ == '__main__':
    scrape_website()

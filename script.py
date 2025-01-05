import json
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

def scrape_website():
    try:
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
            utc_now = datetime.utcnow()
            utc_minus_3 = utc_now - timedelta(hours=3)
            fecha_hora_utc3 = utc_minus_3.strftime('%Y-%m-%d %H:%M:%S')

            # Estructura del archivo JSON
            nuevo_dato = {
                'fecha_hora_utc3': fecha_hora_utc3,
                'compra': compra,
                'venta': venta
            }
            try:
                # Leer el archivo JSON existente
                with open('dolar_data.json', "r") as archivo:
                    datos = json.load(archivo)
                
                # Asegurarse de que es una lista para poder agregar datos
                if not isinstance(datos, list):
                    raise ValueError("El archivo JSON no contiene una lista.")

            except (FileNotFoundError, json.JSONDecodeError):
                # Si el archivo no existe o está vacío, creamos una lista nueva
                datos = []

            # Añadir el nuevo dato a la lista
            datos.append(nuevo_dato)


            # Exportar a JSON
            with open('dolar_data.json', mode='w', encoding='utf-8') as file:
                file.write(json.dumps(datos, ensure_ascii=False, indent=4))  # Agrega la entrada con saltos de línea

            print(f"✅ Datos exportados correctamente a 'dolar_data.json' con la fecha/hora {fecha_hora_utc3}")

    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

if __name__ == '__main__':
    scrape_website()
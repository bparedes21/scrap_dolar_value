from playwright.sync_api import sync_playwright

def scrape_website():
    try:
        with sync_playwright() as p:
            # Cambiar a headless=True para evitar la necesidad de X11
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            )
            # Crear una nueva página
            page = context.new_page()

            url = 'https://www.ambito.com/contenidos/dolar.html'
            print(f"📡 Cargando la página: {url}")
            
            for attempt in range(5):  # Intentar 3 veces
                try:

                    page.goto(url, timeout=120000, wait_until="load")
                    page.wait_for_selector('.variation-max-min__value.data-valor.data-compra', timeout=60000)
                    break  # Salir si la página se carga correctamente
                except Exception as e:
                    print(f"🔁 Reintentando la carga de la página ({attempt+1}/5)...")
                    if attempt == 4:  # Último intento
                        raise e

            # Extraer datos
            compra = page.locator(".variation-max-min__value.data-valor.data-compra").first.text_content()
            venta = page.locator(".variation-max-min__value.data-valor.data-venta").first.text_content()

            print(f'💸 Valor de compra: {compra}')
            print(f'💸 Valor de venta: {venta}')

    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

if __name__ == '__main__':
    scrape_website()

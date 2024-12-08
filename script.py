from playwright.sync_api import sync_playwright

def scrape_website():
    try:
        with sync_playwright() as p:
            # Abrir el navegador
            browser = p.chromium.launch(headless=False)  # Ver la ejecución
            page = browser.new_page()

            # Bloquear imágenes, fuentes y estilos
            page.route("**/*", lambda route: route.abort() if route.request.resource_type in ['image', 'stylesheet', 'font'] else route.continue_())

            # Cambiar el User-Agent
            page.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')

            # Intentar cargar la página con reintentos
            url = 'https://www.ambito.com/contenidos/dolar.html'
            print(f"📡 Cargando la página: {url}")
            
            for attempt in range(3):  # Intentar 3 veces
                try:
                    page.goto(url, timeout=120000, wait_until="load")  # Esperar "load" en lugar de "networkidle"
                    page.wait_for_selector('.variation-max-min__value.data-valor.data-compra', timeout=60000)
                    break
                except Exception as e:
                    print(f"🔁 Reintentando la carga de la página ({attempt+1}/3)...")
                    if attempt == 2:  # Último intento
                        raise e

            # Extraer el texto del valor de compra y venta
            compra = page.locator(".variation-max-min__value.data-valor.data-compra").first.text_content()
            venta = page.locator(".variation-max-min__value.data-valor.data-venta").first.text_content()

            print(f'💸 Valor de compra: {compra}')
            print(f'💸 Valor de venta: {venta}')

    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

    finally:
        try:
            browser.close()
        except Exception as e:
            print(f"⚠️ No se pudo cerrar el navegador: {e}")

if __name__ == '__main__':
    scrape_website()

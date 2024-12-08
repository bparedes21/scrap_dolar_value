from playwright.sync_api import sync_playwright

def scrape_website():
    try:
        with sync_playwright() as p:
            # Lanzar el navegador
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            # Cargar la URL con tiempo de espera extendido y asegurarse de que la red esté inactiva
            url = 'https://www.ambito.com/contenidos/dolar.html'
            print(f"📡 Cargando la página: {url}")
            page.goto(url, timeout=60000, wait_until="networkidle")  # Espera a que no haya solicitudes de red activas
            
            # Esperar hasta que los elementos dinámicos estén visibles
            print("⌛ Esperando a que el elemento de 'compra' esté disponible...")
            page.wait_for_selector('.variation-max-min__value.data-valor.data-compra', timeout=60000)
            page.wait_for_selector('.variation-max-min__value.data-valor.data-venta', timeout=60000)
            
            # Extraer el texto de compra y venta
            compra = page.locator(".variation-max-min__value.data-valor.data-compra").first().text_content()
            venta = page.locator(".variation-max-min__value.data-valor.data-venta").first().text_content()

            print(f'💰 Valor de COMPRA: {compra}')
            print(f'💰 Valor de VENTA: {venta}')

            # Extraer una lista de otros elementos de la página
            print("📄 Extrayendo lista de elementos de la página...")
            items = page.locator('span').all_inner_texts()
            print(f'📋 Lista de items extraídos: {items[:5]} (mostrando los primeros 5)')

    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

    finally:
        try:
            browser.close()
            print("🛑 Navegador cerrado correctamente.")
        except Exception as e:
            print(f"⚠️ No se pudo cerrar el navegador: {e}")

if __name__ == '__main__':
    scrape_website()

    scrape_website()

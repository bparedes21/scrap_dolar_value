from playwright.sync_api import sync_playwright

def scrape_website(max_retries=5):  # Cambia el número de reintentos aquí
    with sync_playwright() as p:
        for attempt in range(max_retries):
            try:
                print(f'📡 Cargando la página: https://www.ambito.com/contenidos/dolar.html (Intento {attempt + 1}/{max_retries})')
                
                # Abrir el navegador y la página
                browser = p.chromium.launch(headless=True)  # Usar headless=True para no mostrar la interfaz
                page = browser.new_page()
                
                # Evitar cargar imágenes, estilos y fuentes para acelerar la carga
                page.route("**/*", lambda route: route.abort() if route.request.resource_type in ['image', 'stylesheet', 'font'] else route.continue_())
                
                page.goto('https://www.ambito.com/contenidos/dolar.html', timeout=60000)  # Espera 60 segundos
                page.wait_for_selector('.variation-max-min__value.data-valor.data-compra', timeout=30000)  # Espera 30 segundos para el selector
                
                # Extraer los valores de compra y venta
                compra = page.locator('.variation-max-min__value.data-valor.data-compra').first.text_content()
                venta = page.locator('.variation-max-min__value.data-valor.data-venta').first.text_content()
                
                print(f'💸 Valor de compra: {compra}')
                print(f'💸 Valor de venta: {venta}')
                
                # Cerrar navegador y salir
                browser.close()
                break  # Salimos del bucle porque ya se cargaron los datos con éxito
            
            except Exception as e:
                print(f'❌ Error en el intento {attempt + 1}/{max_retries}: {e}')
                
                if attempt == max_retries - 1:  # Último intento fallido
                    print(f'⚠️ Se alcanzó el máximo de reintentos ({max_retries}). No se pudo cargar la página.')
                
                try:
                    browser.close()
                except Exception as e:
                    print(f'⚠️ No se pudo cerrar el navegador: {e}')
        
if __name__ == '__main__':
    scrape_website(max_retries=5)  # Puedes cambiar 5 a la cantidad de intentos que desees

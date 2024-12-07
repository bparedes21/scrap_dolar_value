from playwright.sync_api import sync_playwright

def scrape_website():
    with sync_playwright() as p:
        # Abrimos el navegador
        browser = p.chromium.launch(headless=True)  # headless=True para que sea "invisible"
        page = browser.new_page()
        
        # Cargar la URL
        url = 'https://www.ambito.com/contenidos/dolar.html'
        page.goto(url)
        
        # Esperar a que se cargue un elemento dinámico específico
        page.wait_for_selector('.variation-max-min__value.data-valor.data-compra')  # Espera hasta que esté disponible el elemento
        
        # Extraer el texto completo (incluyendo texto oculto)
        val1 = page.locator(".variation-max-min__value.data-valor.data-compra:nth-of-type(1)").text_content()
        print(f'val1 de la página (text_content): {val1}')
        
        # Extraer solo el texto visible
        #val2 = page.locator('.variation-max-min__value.data-valor.data-compra').inner_text()
        #print(f'val2 de la página (inner_text): {val2}')

        # Extraer otros elementos (ejemplo: lista de elementos)
        items = page.locator('span').all_inner_texts()
        print('Lista de items:', items)

        # Cerrar navegador
        browser.close()

if __name__ == '__main__':
    scrape_website()

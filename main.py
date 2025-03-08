from src.drivers.driver_manager import WebDriverFactory
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time

driver = WebDriverFactory.get_driver()
base_page = BasePage(driver)

base_page.open_url("")

# Iniciar sesión
base_page.enter_text(By.CSS_SELECTOR, "body > div.page-login > div > div.login-right > div > div > div.page-content.ng-isolate-scope.content > form > div > div:nth-child(2) > div.field.ng-scope > div > input", "avalon")
base_page.enter_text(By.CSS_SELECTOR, "body > div.page-login > div > div.login-right > div > div > div.page-content.ng-isolate-scope.content > form > div > div:nth-child(3) > div.field.ng-scope > div > input", "*Avalon*")
base_page.click_element(By.CSS_SELECTOR, "body > div.page-login > div > div.login-right > div > div > div.page-content.ng-isolate-scope.content > form > ul > li > a")

# Esperar que la tabla cargue
if base_page.element_exists(By.CSS_SELECTOR, "div.grid-rows", timeout=120):
    
    filas = base_page.get_elements(By.CSS_SELECTOR, "div.grid-rows > div.grid-row", timeout=120)
    
    print(f"Se encontraron {len(filas)} filas en la tabla.")

    for i, fila in enumerate(filas, start=1):
        try:
            # Obtener nombre y número de identificación
            nombre = fila.find_element(By.CSS_SELECTOR, "div.grid-cell.w-4.wg-3 span").text.strip()
            identificacion = fila.find_element(By.CSS_SELECTOR, "div.grid-cell.w-4.wg-3 div.box-sty-subtitle").text.strip()

            print(f"📌 Fila {i} - Nombre: {nombre}, ID: {identificacion}")

            # Buscar y hacer clic en el botón "Ver estudio"
            # boton = fila.find_element(By.XPATH, ".//a[contains(text(), 'Ver estudio')]")
            # boton.click()
            # print(f"✅ Clic en 'Ver estudio' de la fila {i}")

            # Puedes agregar aquí una pausa si la página cambia después del clic
            # time.sleep(2)

            # Regresar a la página anterior si es necesario
            # driver.back()
            # time.sleep(2)  # Espera que la página se recargue

        except Exception as e:
            print(f"⚠️ No se pudo procesar la fila {i}: {e}")

time.sleep(500)

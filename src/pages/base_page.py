from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)  # Espera predeterminada

    def open_url(self, url):
        """Abre una URL en el navegador."""
        self.driver.get(url)

    def element_exists(self, by, value, timeout=5):
        """Verifica si un elemento existe en la página."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((by, value)))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def enter_text(self, by, value, text, timeout=5):
        """Encuentra un campo de entrada y escribe texto en él."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            print(f"❌ No se encontró el campo de entrada: {value}")
            return False

    def click_element(self, by, value, timeout=5):
        """Encuentra un elemento y hace clic en él."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except TimeoutException:
            print(f"❌ No se pudo hacer clic en el elemento: {value}")
            return False

    def get_elements(self, by, value, timeout=5):
        """Devuelve una lista de elementos dentro de un contenedor."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
        except TimeoutException:
            print(f"❌ No se encontraron elementos con selector: {value}")
            return []

    def get_elements_count(self, by, value, timeout=5):
        """Devuelve la cantidad de elementos dentro de un contenedor."""
        if not self.element_exists(by, value, timeout):
            return 0
        try:
            elements = self.get_elements(by, value, timeout)
            return len(elements)
        except Exception as e:
            print(f"⚠️ Error al contar elementos: {e}")
            return 0

import os
import pytesseract
import cv2
import time
import numpy as np
import pandas as pd
from src.drivers.driver_manager import WebDriverFactory
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def procesar_imagen_para_ocr(imagen_path):
    image = cv2.imread(imagen_path)

    if image is None:
        return ""

    x, y, w, h = 150, 50, 250, 45
    cropped_image = image[y:y+h, x:x+w]

    upscale_factor = 2
    high_res = cv2.resize(cropped_image, (w * upscale_factor, h * upscale_factor), interpolation=cv2.INTER_CUBIC)

    processed_path = imagen_path.replace(".png", "_processed.png")
    cv2.imwrite(processed_path, high_res)

    text = pytesseract.image_to_string(high_res, lang="eng+spa")

    return text.strip()

driver = WebDriverFactory.get_driver()
base_page = BasePage(driver)

base_page.open_url("")

base_page.enter_text(By.CSS_SELECTOR, "body > div.page-login > div > div.login-right > div > div > div.page-content.ng-isolate-scope.content > form > div > div:nth-child(2) > div.field.ng-scope > div > input", "")
base_page.enter_text(By.CSS_SELECTOR, "body > div.page-login > div > div.login-right > div > div > div.page-content.ng-isolate-scope.content > form > div > div:nth-child(3) > div.field.ng-scope > div > input", "")
base_page.click_element(By.CSS_SELECTOR, "body > div.page-login > div > div.login-right > div > div > div.page-content.ng-isolate-scope.content > form > ul > li > a")

resultados = []

if base_page.element_exists(By.CSS_SELECTOR, "div.grid-rows", timeout=120):
    filas = base_page.get_elements(By.CSS_SELECTOR, "div.grid-rows > div.grid-row", timeout=120)

    for index, fila in enumerate(filas):
        try:
            nombre = fila.find_element(By.CSS_SELECTOR, "div.grid-cell.w-4.wg-3 span").text.strip()
            identificacion = fila.find_element(By.CSS_SELECTOR, "div.grid-cell.w-4.wg-3 div.box-sty-subtitle").text.strip()

            print(f"📌 ({index+1}/{len(filas)}) Nombre: {nombre}, ID: {identificacion}")

            boton = fila.find_element(By.XPATH, ".//a[contains(text(), 'Ver estudio')]")
            base_page.wait.until(lambda d: boton.is_displayed() and boton.is_enabled())
            boton.click()

            time.sleep(2)
            ventanas = driver.window_handles
            if len(ventanas) < 2:
                print("❌ No se detectó una nueva pestaña.")
            else:
                driver.switch_to.window(ventanas[-1])

                base_page.wait.until(lambda d: base_page.element_exists(By.TAG_NAME, "canvas", timeout=60))
                print("✅ Imagen en canvas detectada.")

                os.makedirs("capturas", exist_ok=True)

                intentos = 0
                max_intentos = 3
                coincidencia_confirmada = False

                while intentos < max_intentos and not coincidencia_confirmada:
                    intentos += 1
                    screenshot_path = f"capturas/estudio_{index}_try{intentos}.png"
                    driver.save_screenshot(screenshot_path)

                    text = procesar_imagen_para_ocr(screenshot_path)

                    print(f"📝 Intento {intentos}: Texto extraído:\n{text}")

                    nombre_coincide = nombre.lower() in text.lower()
                    id_coincide = identificacion in text

                    if nombre_coincide and id_coincide:
                        coincidencia_confirmada = True
                    elif intentos < max_intentos:
                        print(f"⚠️ OCR no coincidió, reintentando... ({intentos}/{max_intentos})")
                        time.sleep(2)

                resultados.append({
                    "Nombre en página": nombre,
                    "ID en página": identificacion,
                    "Texto en estudio": text.strip(),
                    "Nombre coincide": "✅" if nombre_coincide else "❌",
                    "ID coincide": "✅" if id_coincide else "❌",
                    "Intentos OCR": intentos
                })

                driver.close()
                driver.switch_to.window(ventanas[0])

                base_page.wait.until(lambda d: base_page.element_exists(By.CSS_SELECTOR, "div.grid-rows", timeout=60))

        except Exception as e:
            print(f"⚠️ Error en fila {index+1}: {e}")

driver.quit()

df = pd.DataFrame(resultados)
df.to_excel("resultados.xlsx", index=False)
print("🚀 Proceso completado y resultados guardados en resultados.xlsx")

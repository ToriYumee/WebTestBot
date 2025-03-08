from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class WebDriverFactory:
    @staticmethod
    def get_driver(headless=False):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument("--headless")
            
        sevice = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=sevice, options=options)

        
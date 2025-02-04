from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

import telebot
import datetime
import locale
import os

def run_script():
    load_dotenv()

    token = os.getenv("TELEGRAM_TOKEN")
    user_id = os.getenv("USER_ID")

    bot = telebot.TeleBot(token)
    locale.setlocale(locale.LC_TIME, 'es_AR.UTF-8')

    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        driver.get("https://www.movistararena.com.ar/show/e69127ec-55d8-4a59-b6c5-a7fdaa536615")

        wait = WebDriverWait(driver, 10)
        events = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "evento-row")))

        tickets = 0
        hour = datetime.datetime.now()
        formattedHour = hour.strftime('el %d-%m-%Y a las %H:%M')

        for event in events:
            try:
                status = event.find_element(By.CSS_SELECTOR, ".btn-comprar .mud-button-label").text
                day = event.find_element(By.CSS_SELECTOR, ".fecha p").text
                month = event.find_element(By.CSS_SELECTOR, ".fecha span").text

                if status and status != 'Agotado' and day == '14':
                    tickets += 1
                    bot.send_message(chat_id=user_id, text=f'Hay entradas para el día {day} de {month} ahora {formattedHour}')
            except Exception as e:
                print(f"Error al procesar un evento: {e}")

        if tickets == 0:
            bot.send_message(chat_id=user_id, text=f'No hay entradas para ver a Duki {formattedHour}')

    except Exception as e:
        print(f"Error al procesar la página: {e}")
        bot.send_message(chat_id=user_id, text=f"Hubo un error al intentar obtener la información: {e}")
    
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"No se pudo cerrar el driver correctamente: {e}")

if __name__ == "__main__":
    try:
        run_script()
    except Exception as e:
        print(f"Error inesperado: {e}")

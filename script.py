from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from datetime import datetime

import telebot
import pytz
import os

app = Flask(__name__)

def run_script():

    load_dotenv()

    token = os.getenv("TELEGRAM_TOKEN")
    user_id = os.getenv("USER_ID")

    bot = telebot.TeleBot(token)

    buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')

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

        now = datetime.now(buenos_aires_tz)
        formattedHour = now.strftime('el %d-%m-%Y a las %H:%M')

        for event in events:

            try:
                status = event.find_element(By.CSS_SELECTOR, ".btn-comprar .mud-button-label").text
                day = event.find_element(By.CSS_SELECTOR, ".fecha p").text
                month = event.find_element(By.CSS_SELECTOR, ".fecha span").text

                if status and status != 'Agotado' and day == '14':
                    tickets += 1
                    print(f'Hay entradas para el día {day} de {month} ahora {formattedHour}')
                    bot.send_message(chat_id=user_id, text=f'Hay entradas para el día {day} de {month} ahora {formattedHour}')

            except Exception as e:
                print(f"Error al procesar un evento: {e}")

        # if tickets == 0:
        #     print(f'No hay entradas para ver a Duki {formattedHour}')
        #     bot.send_message(chat_id=user_id, text=f'No hay entradas para ver a Duki {formattedHour}')

    except Exception as e:
        print(f"Error al procesar la página: {e}")
        bot.send_message(chat_id=user_id, text=f"Hubo un error al intentar obtener la información: {e}")
    
    finally:

        try:
            driver.quit()

        except Exception as e:
            print(f"No se pudo cerrar el driver correctamente: {e}")

@app.route('/run-script', methods=['GET'])

def run_script_route():

    try:
        run_script()
        print("Script ejecutado con éxito")
        return "Script ejecutado con éxito", 200
    
    except Exception as e:
        print(f"Hubo un error al ejecutar el script: {e}")
        return f"Hubo un error al ejecutar el script: {e}", 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
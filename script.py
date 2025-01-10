from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

import telebot
from datetime import datetime
import pytz
import os

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def run_script():
    load_dotenv()

    token = os.getenv("TELEGRAM_TOKEN")
    user_id = os.getenv("USER_ID")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    bot = telebot.TeleBot(token)

    driver.get("https://www.movistararena.com.ar/show/e69127ec-55d8-4a59-b6c5-a7fdaa536615")

    try:
        wait = WebDriverWait(driver, 10)
        events = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "evento-row")))

        tickets = 0

        buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        now = datetime.now(buenos_aires_tz)
        formattedHour = now.strftime('el %d-%m-%Y a las %H:%M')
        
        for event in events:
            try:
                status = event.find_element(By.CSS_SELECTOR, ".btn-comprar .mud-button-label").text
                day = event.find_element(By.CSS_SELECTOR, ".fecha p").text
                month = event.find_element(By.CSS_SELECTOR, ".fecha span").text

                if status and status != 'Agotado':
                    tickets+=1
                    bot.send_message(chat_id=user_id, text=f'Hay entradas para el día {day} de {month} ahora {formattedHour}')
            except Exception as e:
                print(f"Error al procesar un evento: {e}")

        if tickets == 0:
            bot.send_message(chat_id=user_id, text=f'No hay entradas para ver a Duki {formattedHour}')

    except Exception as e:
        print("Error al encontrar los elementos:", e)

    driver.quit()

    return 'Proceso realizado con éxito'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

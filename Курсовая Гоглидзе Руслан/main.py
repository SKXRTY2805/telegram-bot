import logging

import requests

from telegram import Update

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

GOOGLE_MAPS_API_KEY = "AIzaSyBhTawap-A4oTZMYOGcZ5pJ6_DZTK472HY"

TELEGRAM_TOKEN = "8516169604:AAH1Uuv0pRrB6jbgI8cSQTs_xLUle-5y4us"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

ADDRESS_FROM, ADDRESS_TO = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

await update.message.reply_text("Привет! Я помогу построить маршрут.\nВведите адрес, откуда ехать:")

return ADDRESS_FROM

async def address_from(update: Update, context: ContextTypes.DEFAULT_TYPE):

context.user_data["address_from"] = update.message.text

await update.message.reply_text("Спасибо! Теперь напишите адрес, куда ехать:")

return ADDRESS_TO

def geocode(address):

try:

    url = f"https://maps.googleapis.com/maps/api/geocode/json"

    params = {"address": address, "key": GOOGLE_MAPS_API_KEY}

    resp = requests.get(url, params=params, timeout=10)

    resp.raise_for_status()

    data = resp.json()

    if data["status"] != "OK" or not data["results"]:

        print(f"Геокодирование неудачно: {data}")

        return None

    loc = data["results"][0]["geometry"]["location"]

    return [loc["lat"], loc["lng"]]

except Exception as ex:

    print("Ошибка геокодирования:", ex)

    return None

def get_route(coord_from, coord_to):

try:

    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {

        "origin": f"{coord_from[0]},{coord_from[1]}",

        "destination": f"{coord_to[0]},{coord_to[1]}",

        "mode": "driving",

        "key": GOOGLE_MAPS_API_KEY,

        "language": "ru"

    }

    resp = requests.get(url, params=params, timeout=20)

    resp.raise_for_status()

    routes_data = resp.json()

    if routes_data["status"] != "OK" or not routes_data["routes"]:

        print("Нет маршрутов:", routes_data)

        return None, None



    leg = routes_data["routes"][0]["legs"][0]

    # в расстояние в метрах время в секундах

    distance_km = leg["distance"]["value"] / 1000

    duration_min = leg["duration"]["value"] / 60



    return distance_km, duration_min

except Exception as ex:

    print("Ошибка маршрутизации:", ex)

    return None, None

async def address_to(update: Update, context: ContextTypes.DEFAULT_TYPE):

address_from = context.user_data.get("address_from")

address_to = update.message.text



coord_from = geocode(address_from)

coord_to = geocode(address_to)



if not coord_from or not coord_to:

    await update.message.reply_text("Не удалось определить координаты одного из адресов. Попробуйте еще раз.")

    return ConversationHandler.END



dist, dur = get_route(coord_from, coord_to)

if dist is None or dur is None:

    await update.message.reply_text("Не удалось построить маршрут. Попробуйте позже.")

    return ConversationHandler.END



await update.message.reply_text(

    f"🚗 Маршрут от '{address_from}' до '{address_to}':\n"

    f"📏 Расстояние: {dist:.2f} км\n"

    f"⏳ Время в пути: {dur:.1f} мин"

)

return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

await update.message.reply_text("Диалог отменён.")

return ConversationHandler.END

def main():

application = Application.builder().token(TELEGRAM_TOKEN).build()



conv_handler = ConversationHandler(

    entry_points=[CommandHandler("start", start)],

    states={

        ADDRESS_FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, address_from)],

        ADDRESS_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, address_to)],

    },

    fallbacks=[CommandHandler("cancel", cancel)],

)



application.add_handler(conv_handler)

application.run_polling()

if name == "main":

main()
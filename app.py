import logging

import httpx
from telegram import Update, constants
from telegram.ext import (
    filters,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

weatherAPIkey = "bb91b7e5d70d4ffc873205937241310"
botToken = "1213907579:AAGQkqsS5DGb3CCgeCjPCGGR-nPnpK69jRw"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет. Я расскажу о погоде в любом доступном городе. \nВведи название города.)",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def get_weather():
        message_text = update.message.text
        try:
            response = httpx.get(
                f"http://api.weatherapi.com/v1/current.json?key={weatherAPIkey}&q={message_text}&aqi=no"
            ).json()
            city = response["location"]["name"]
            country = response["location"]["country"]
            local_time = response["location"]["localtime"]
            temperature = response["current"]["temp_c"]
            feels_like = response["current"]["feelslike_c"]
            wind_speed = response["current"]["wind_kph"]
            condition = response["current"]["condition"]["icon"]
            condition_text = response["current"]["condition"]["text"]
            response = f"""
            Текущая погода в городе {city}
            Страна: {country}
            Местное время: {local_time}
            Температура: {temperature}
            Ощущается как: {feels_like}
            Скорость ветра: {wind_speed}
            На улице: <tg-spoiler>{'https:'+condition}</tg-spoiler>"""
        except Exception as err:
            response = (
                f"Ошибка при выполнении запроса.\nПроверьте название города.\n{err}"
            )
        return response

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_weather(),
        parse_mode=constants.ParseMode.HTML,
    )


if __name__ == "__main__":
    echo_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND),
        echo,
    )

    app = ApplicationBuilder().token(token=botToken).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(echo_handler)
    app.run_polling()

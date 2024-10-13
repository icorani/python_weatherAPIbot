import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hi! I'm tell you about weather in any city :)")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text,
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token("1213907579:AAGQkqsS5DGb3CCgeCjPCGGR-nPnpK69jRw").build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

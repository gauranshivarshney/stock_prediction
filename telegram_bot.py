import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

def get_stock_prediction():
    return "Predicted price: ₹2,134.56 (example)"

TELEGRAM_BOT_TOKEN = '7751495937:AAGzL-nUMajGs6TdDdaKydIyNyYcEMI9yDE'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /predict to get stock prediction.")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_stock_prediction()
    await update.message.reply_text(result)

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
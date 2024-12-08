from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ORGANIZER_CHAT_ID = os.getenv("ORGANIZER_CHAT_ID")

EXCURSION, PEOPLE_COUNT, DATE, NAME, PHONE = range(5)

async def start(update: Update, context):
    await update.message.reply_text(
        "Добро пожаловать! Напишите, какую экскурсию вы хотите забронировать."
    )
    return EXCURSION

async def excursion(update: Update, context):
    context.user_data["excursion"] = update.message.text
    await update.message.reply_text("Сколько человек будет участвовать?")
    return PEOPLE_COUNT

async def people_count(update: Update, context):
    context.user_data["people_count"] = update.message.text
    await update.message.reply_text("Укажите желаемую дату экскурсии (в формате ДД.ММ.ГГГГ).")
    return DATE

async def date(update: Update, context):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("Как вас зовут?")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Пожалуйста, напишите свой номер телефона:")
    return PHONE

async def phone(update: Update, context):
    context.user_data["phone"] = update.message.text

    booking_info = (
        f"Новая бронь!\n"
        f"Экскурсия: {context.user_data['excursion']}\n"
        f"Количество человек: {context.user_data['people_count']}\n"
        f"Дата: {context.user_data['date']}\n"
        f"Имя: {context.user_data['name']}\n"
        f"Телефон: {context.user_data['phone']}"
    )
    context.bot.send_message(chat_id=ORGANIZER_CHAT_ID, text=booking_info)

    await context.bot.send_message(chat_id=ORGANIZER_CHAT_ID, text=booking_info)
    await update.message.reply_text("Спасибо! Мы скоро свяжемся с вами для уточнения деталей.")
    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text("Вы отменили процесс бронирования.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EXCURSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, excursion)],
            PEOPLE_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, people_count)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, date)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()


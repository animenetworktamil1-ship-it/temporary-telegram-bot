import os
from datetime import datetime, timedelta, timezone
from threading import Thread

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

app = Flask(__name__)


@app.route("/")
def home():
    return "Temporary Join Request Bot is running!"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🔗 Get Join Request Link",
                callback_data="get_link"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Tap the button below to generate a temporary "
        "Channel Join Request link.\n\n"
        "⏳ Link validity: 2 minutes",
        reply_markup=reply_markup
    )


async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    try:

        # Current time + 2 minutes
        expire_time = (
            datetime.now(timezone.utc)
            + timedelta(minutes=2)
        )

        invite = await context.bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            expire_date=expire_time,
            creates_join_request=True
        )

        await query.edit_message_text(
            "📩 Join Request Link Created!\n\n"
            f"🔗 {invite.invite_link}\n\n"
            "⏳ This link expires automatically after 2 minutes.\n\n"
            "⚠️ Click the link and send a Join Request."
        )

    except Exception as error:

        print("ERROR:", error)

        await query.edit_message_text(
            "❌ Couldn't create the Join Request link.\n\n"
            "Please check that the bot is an administrator "
            "of the channel and has permission to manage "
            "invite links."
        )


def run_server():

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )


def main():

    # Start Flask server for Render
    Thread(
        target=run_server,
        daemon=True
    ).start()

    # Start Telegram bot
    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(
            get_link,
            pattern="^get_link$"
        )
    )

    print("Bot started!")

    application.run_polling()


if __name__ == "__main__":
    main()

#Hi

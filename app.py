import os
from flask import Flask
from threading import Thread
from datetime import datetime, timedelta, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

app = Flask(__name__)


@app.route("/")
def home():
    return "Telegram Temporary Link Bot is running!"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=2)

        invite = await context.bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            name="2 Minute Link",
            expire_date=expire_time,
            member_limit=1
        )

        await update.message.reply_text(
            "🔐 Temporary Link Generated\n\n"
            f"🔗 {invite.invite_link}\n\n"
            "⏳ This link is valid for 2 minutes.\n"
            "👤 Maximum 1 user can use it.\n\n"
            "⚠️ After 2 minutes, the link automatically expires."
        )

    except Exception as e:

        await update.message.reply_text(
            "❌ Could not create the link.\n\n"
            "Please make sure the bot is an administrator "
            "of the channel/group."
        )

        print("ERROR:", e)


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


def main():

    Thread(target=run_flask, daemon=True).start()

    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))

    print("Bot started...")

    bot.run_polling()


if __name__ == "__main__":
    main()

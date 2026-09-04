import os
import sqlite3
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

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.environ["BOT_TOKEN"]

# Your Telegram user ID.
# Example: 123456789
ADMIN_ID = int(os.environ["ADMIN_ID"])

DB_FILE = "channels.db"

app = Flask(__name__)


# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            username TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_channel(chat_id, title, username):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO channels
        (chat_id, title, username)
        VALUES (?, ?, ?)
        """,
        (str(chat_id), title, username)
    )

    conn.commit()
    conn.close()


def remove_channel(chat_id):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM channels WHERE chat_id = ?",
        (str(chat_id),)
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0


def get_channels():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT chat_id, title, username FROM channels ORDER BY id"
    )

    channels = cursor.fetchall()

    conn.close()

    return channels


# =========================
# FLASK
# =========================

@app.route("/")
def home():
    return "Multi Channel Telegram Bot is running!"


def run_server():

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )


# =========================
# ADMIN CHECK
# =========================

def is_admin(update: Update):

    return (
        update.effective_user
        and update.effective_user.id == ADMIN_ID
    )


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    channels = get_channels()

    if not channels:

        await update.message.reply_text()

#Hi

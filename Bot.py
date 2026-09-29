import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

notes = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "I am your Notes Bot.\n\n"
        "Commands:\n"
        "/save your note - Save a note\n"
        "/notes - Show your notes\n"
        "/clear - Clear your notes"
    )


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    note = " ".join(context.args)

    if not note:
        await update.message.reply_text(
            "Please write a note after /save.\n\n"
            "Example:\n"
            "/save Buy a new charger"
        )
        return

    notes.setdefault(user_id, []).append(note)

    await update.message.reply_text("✅ Note saved!")


async def show_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_notes = notes.get(user_id, [])

    if not user_notes:
        await update.message.reply_text("📭 You don't have any saved notes.")
        return

    message = "📝 Your notes:\n\n"

    for number, note in enumerate(user_notes, 1):
        message += f"{number}. {note}\n"

    await update.message.reply_text(message)


async def clear_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    notes[user_id] = []

    await update.message.reply_text("🗑️ All your notes have been cleared.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("save", save))
    app.add_handler(CommandHandler("notes", show_notes))
    app.add_handler(CommandHandler("clear", clear_notes))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

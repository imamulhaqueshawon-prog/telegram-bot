import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = "8772873196:AAF3J3l_OhVHLoD2Uhc5wgER0nUhsWAXXPk"
GROQ_API_KEY = "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"

chat_histories = {}

def ask_groq(messages):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": 1024}
    r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    return r.json()["choices"][0]["message"]["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম! আমি AI Assistant। যেকোনো প্রশ্ন করুন!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    if user_id not in chat_histories:
        chat_histories[user_id] = [{"role": "system", "content": "তুমি একজন সহায়ক AI। বাংলায় কথা বললে বাংলায় উত্তর দাও।"}]
    chat_histories[user_id].append({"role": "user", "content": user_message})
    reply = ask_groq(chat_histories[user_id])
    chat_histories[user_id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()

import os
import logging
from urllib.parse import urlparse
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ALLOWED_HOSTS = {h.strip().lower() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()}
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def is_admin(uid):
    return ADMIN_ID != 0 and uid == ADMIN_ID

def safe_url(url):
    try:
        p = urlparse(url)
        host = (p.hostname or "").lower()
        return p.scheme == "https" and host and any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS)
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Authorized Media Bot\n\n"
        "এই বট আপনার নিজের বা বিতরণের অনুমতি থাকা সরাসরি মিডিয়া লিংক শেয়ার করে।\n"
        "এটি ShemarooMe-এর পেইড/DRM-সুরক্ষিত ভিডিও ডাউনলোড বা সুরক্ষা বাইপাস করে না।\n\n"
        "/help — সাহায্য\n/links — অনুমোদিত লিংক তালিকা\n"
        "Admin: /addlink Title | https://your-authorized-domain.example/file.mp4"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Admin: .env-এ BOT_TOKEN, ADMIN_ID, ALLOWED_HOSTS সেট করুন।\n"
        "/addlink Title | https://your-authorized-domain.example/file.mp4\n"
        "/links — লিংক দেখুন\n"
        "ShemarooMe-এর অফলাইন দেখার জন্য অ্যাপের নিজস্ব Download সুবিধা ব্যবহার করুন।"
    )

async def addlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Admin only.")
        return
    raw = update.message.text.partition(" ")[2].strip()
    if "|" not in raw:
        await update.message.reply_text("ব্যবহার: /addlink Title | https://your-authorized-domain.example/file.mp4")
        return
    title, url = [x.strip() for x in raw.split("|", 1)]
    if not title or not safe_url(url):
        await update.message.reply_text("❌ HTTPS URL দিন এবং নিশ্চিত করুন ডোমেইনটি ALLOWED_HOSTS-এ আছে।")
        return
    items = context.application.bot_data.setdefault("links", [])
    items.append({"title": title[:100], "url": url})
    await update.message.reply_text(f"✅ লিংক যোগ হয়েছে: {title}")

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = context.application.bot_data.get("links", [])
    if not items:
        await update.message.reply_text("এখনও কোনো লিংক যোগ করা হয়নি।")
        return
    for item in items[-20:]:
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("▶️ Open authorized link", url=item["url"])]])
        await update.message.reply_text("🎬 " + item["title"], reply_markup=markup)

async def download_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "এই বট DRM বা পেইড OTT স্ট্রিম ডাউনলোড করে না। "
        "যোগ্য কনটেন্ট অফলাইনে দেখতে ShemarooMe অ্যাপের নিজস্ব Download সুবিধা ব্যবহার করুন।"
    )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing in .env")
    if not ADMIN_ID:
        raise RuntimeError("ADMIN_ID is missing in .env")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("addlink", addlink))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("download", download_info))
    log.info("Bot started")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

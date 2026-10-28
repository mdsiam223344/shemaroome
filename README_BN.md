# ShemarooMe-related Authorized Link Bot

এই বট কেবল আপনার নিজের বা বিতরণের অনুমতি থাকা সরাসরি মিডিয়া লিংক শেয়ার করে। এটি ShemarooMe-এর private API, paid stream, login session বা DRM bypass করে না।

## Termux setup
1. ZIP Extract করুন।
2. Termux-এ চালান: `pkg update && pkg upgrade -y && pkg install python -y`
3. এই ফোল্ডারে যান।
4. `pip install -r requirements.txt`
5. `cp .env.example .env && nano .env`
6. @BotFather থেকে BOT_TOKEN নিন; ADMIN_ID-তে আপনার numeric Telegram user ID দিন; ALLOWED_HOSTS-এ নিজের অনুমোদিত ফাইল হোস্টের domain দিন।
7. চালান: `python bot.py`

## Commands
- `/start`
- `/help`
- Admin: `/addlink Title | https://your-authorized-domain.example/file.mp4`
- `/links`
- `/download`

নোট: লিংকগুলো এই starter version-এ memory-তে থাকে, restart করলে মুছে যাবে। ShemarooMe-এর যোগ্য কনটেন্ট অফলাইনে দেখতে অফিসিয়াল অ্যাপের Download ফিচার ব্যবহার করুন অথবা লিখিত অনুমতি নিন।

import os
import re
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GOOGLE_API_KEY:
    print("Missing TELEGRAM_BOT_TOKEN or GOOGLE_API_KEY in environment.")
    exit(1)

# Configure Gemini (Google Generative AI)
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Load CSV from GitHub
CSV_URL = "https://github.com/19BCS4520/GENAI-AUTOMATION/raw/3dc4d8bdcc3859697263e646c73f92f7a55a446a/issue.csv"
try:
    df_issues = pd.read_csv(CSV_URL)
    if 'Date Occurred' in df_issues.columns:
        df_issues['Date Occurred'] = pd.to_datetime(df_issues['Date Occurred'], errors='coerce')
except Exception as e:
    print(f"Error loading issue CSV: {e}")
    df_issues = pd.DataFrame()

# --------- Utility Functions ---------

def is_today_query(message):
    return "today" in message.lower()

def extract_issue_number(message):
    match = re.search(r'issue\s*#?(\d+)', message.lower())
    return int(match.group(1)) if match else None

def create_issue_context(df, max_chars=8000):
    context = []
    for idx, row in df.iterrows():
        date = row.get('Date Occurred', 'N/A')
        desc = row.get('Issue Description', 'No description')
        expl = row.get('Brief Explanation (2–3 Points) and suggest the soluction', '')
        context.append(f"Issue #{idx+1} | Date: {date}\nDescription: {desc}\nExplanation: {expl}\n")
    joined = "\n".join(context)
    return joined[:max_chars] + "\n...[truncated]..." if len(joined) > max_chars else joined

def build_prompt(user_query, context_text):
    return f"""
You are an intelligent assistant helping with production issue analysis.

The following issues have been reported:

{context_text}

User query: \"{user_query}\"

Determine the user's intent. Possible intents:
1. List today's issues.
2. Provide detailed explanation of a specific issue (by number or topic).
3. Summarize all or filter based on keyword.

Instructions:
- If the user is asking about today's issues, return a list of those issues with date & 1-line summary.
- If the user asks for explanation of an issue (e.g. "Explain issue 2" or "What happened with database timeout"), provide full detail and suggested solution.
- If no matching issues are found, reply with "No matching issues found."

Make the response clear and easy to understand.
"""

def filter_and_summarize_issues_with_llm(user_query, df):
    context_text = create_issue_context(df)
    prompt = build_prompt(user_query, context_text)
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

# --------- Telegram Bot Handlers ---------

def start(update, context):
    update.message.reply_text(
        "👋 Hi! I'm your Issue Summary Bot.\n"
        "You can ask me:\n"
        "- 'summarize all issues'\n"
        "- 'what are today's issues?'\n"
        "- 'explain issue 3'\n"
        "- 'show database issues'\n"
        "Go ahead and type your question!"
    )

def handle_message(update, context):
    user_message = update.message.text.strip()
    chat_id = update.message.chat_id

    if df_issues.empty:
        update.message.reply_text("❌ No issue data is currently loaded.")
        return

    try:
        # 1. Check for today's issues
        if is_today_query(user_message):
            today = pd.Timestamp.now().normalize()
            today_issues = df_issues[df_issues['Date Occurred'].dt.normalize() == today]

            if today_issues.empty:
                update.message.reply_text("✅ No issues reported today.")
            else:
                response = "🗓️ *Today's Issues:*\n"
                for _, row in today_issues.iterrows():
                    response += f"• {row['Issue Description']} (Date: {row['Date Occurred'].date()})\n"
                update.message.reply_text(response)
            return

        # 2. Check for issue number request
        issue_num = extract_issue_number(user_message)
        if issue_num and 1 <= issue_num <= len(df_issues):
            row = df_issues.iloc[issue_num - 1]
            response = (
                f"📌 *Issue #{issue_num}*\n"
                f"🗓️ Date: {row.get('Date Occurred', 'N/A')}\n"
                f"📝 Description: {row.get('Issue Description', 'N/A')}\n"
                f"💡 Explanation: {row.get('Brief Explanation (2–3 Points) and suggest the soluction', 'N/A')}"
            )
            update.message.reply_text(response)
            return

        # 3. Default → Gemini LLM summarization
        ai_response = filter_and_summarize_issues_with_llm(user_message, df_issues)
        update.message.reply_text(ai_response)

    except Exception as e:
        print(f"❌ Error: {e}")
        update.message.reply_text("Sorry, I couldn't process your request.")

# --------- Bot Startup ---------

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("✅ Bot is running. Press Ctrl+C to stop.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_USER_ID = int(os.getenv('TELEGRAM_USER_ID'))
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

if not TELEGRAM_TOKEN or not HUGGINGFACE_TOKEN:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN and HUGGINGFACE_TOKEN in .env file")

# Initialize AI client
client = InferenceClient(token=HUGGINGFACE_TOKEN)

# Load knowledge base
def load_knowledge_base():
    kb_path = "knowledge_base"
    knowledge = {}
    
    for filename in os.listdir(kb_path):
        if filename.endswith(".md"):
            filepath = os.path.join(kb_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                knowledge[filename] = content
    
    return knowledge

knowledge_base = load_knowledge_base()

# Create system prompt
def create_context():
    context = "You are a CSM Operations expert assistant. Use the following documentation to answer questions:\n\n"
    for filename, content in knowledge_base.items():
        context += f"=== {filename} ===\n{content}\n\n"
    return context

SYSTEM_PROMPT = create_context() + """
Instructions:
- Answer questions based on the documentation provided above
- Be specific and cite the relevant document when answering
- If the answer is not in the documentation, say so briefly
- For troubleshooting questions, provide step-by-step guidance
- Include SLA information when relevant
- Keep responses concise for mobile readability
"""

# Store conversations per user
conversations = {}

def is_allowed_user(user_id):
    return user_id == ALLOWED_USER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_allowed_user(user_id):
        await update.message.reply_text("⛔ Sorry, you're not authorized to use this bot.")
        return
    
    await update.message.reply_text(
        "👋 Hello! I'm your CSM Ops Knowledge Assistant.\n\n"
        "I can help with:\n"
        "• CloudERP troubleshooting\n"
        "• S/4HANA alerts\n"
        "• IBP issues\n"
        "• Server management\n"
        "• Incident response\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/clear - Clear conversation\n"
        "/help - Example questions\n\n"
        "Just send me your question!"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_allowed_user(user_id):
        return
    
    if user_id in conversations:
        conversations[user_id] = []
    
    await update.message.reply_text("🗑️ Conversation cleared!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_allowed_user(user_id):
        return
    
    await update.message.reply_text(
        "💡 Example Questions:\n\n"
        "• What should I do if CPU is above 90% on S4HANA?\n"
        "• How do I handle HDB_HOST_STATUS_ALERT_INST?\n"
        "• What is the SLA for P1 incidents?\n"
        "• IBP system not accessible troubleshooting\n"
        "• Filesystem full on /hana/backup\n\n"
        "Just type your question!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_allowed_user(user_id):
        await update.message.reply_text("⛔ Sorry, you're not authorized.")
        return
    
    user_message = update.message.text
    
    if user_id not in conversations:
        conversations[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    conversations[user_id].append({"role": "user", "content": user_message})
    
    await update.message.chat.send_action(action="typing")
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=conversations[user_id],
            max_tokens=800
        )
        
        bot_reply = response.choices[0].message.content
        conversations[user_id].append({"role": "assistant", "content": bot_reply})
        
        if len(conversations[user_id]) > 21:
            conversations[user_id] = [conversations[user_id][0]] + conversations[user_id][-20:]
        
        if len(bot_reply) > 4000:
            chunks = [bot_reply[i:i+4000] for i in range(0, len(bot_reply), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(bot_reply)
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    print("🤖 Starting CSM Ops Telegram Bot...")
    print(f"📚 Loaded {len(knowledge_base)} knowledge base documents")
    print(f"✅ Bot is ready! Send messages on Telegram.\n")
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
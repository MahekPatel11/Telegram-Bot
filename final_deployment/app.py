# import os
# import re
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import Application , CommandHandler , MessageHandler, filters, ContextTypes
# from  langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# load_dotenv()

# # os.environ["HF_TOKEN"] =  os.getenv("HF_TOKEN")
# os.environ["LANGCHAIN_API_KEY"] =  os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_PROJECT"] =  os.getenv("LANGCHAIN_PROJECT")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# groq_api_key = os.getenv("GROQ_API_KEY")

# def setup_llm_chain(topic="technology"):
#     prompt = ChatPromptTemplate.from_messages([
#         ("system" , "you are a joking ai/ give me only one funny joke on given topic"),
#         ("user",f"generate a joke on topic:{topic}")
#     ])

#     llm = ChatGroq(
#         model="Gemma2-9b-It",
#         groq_api_key=groq_api_key
#     )

#     return prompt|llm|StrOutputParser()

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("hiee! Mention me with a topic like '@Unique_joke_Bot python ' ,to get a joke ")

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(" Mention me with a topic like '@Unique_joke_Bot python ', to get some funny jokes ")

# async def genearte_joke(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
#     await update.message.reply_text(f"Generating joke about {topic}")
#     joke= setup_llm_chain(topic).invoke({}).strip()
#     await update.message.reply_text(joke)

# async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     msg = update.message.text
#     bot_username = context.bot.username

#     if f'{bot_username}' in msg:
#         match = re.search(f'@{bot_username}\\s+(.*)', msg)
#         if match and match.group(1).strip():
#             await genearte_joke(update , context , match.group(1).strip())

#         else:
#             await update.message.reply_text("please specify a topic after mentioning me")

# def main():
#     token = os.getenv("TELEGRAM_API_KEY")
#     app = Application.builder().token(token).build()
#     app.add_handler(CommandHandler("start",start))
#     app.add_handler(CommandHandler("help",help_command))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

#     app.run_polling(allowed_updates=Update.ALL_TYPES)

# if __name__ == "__main__":
#     main()


import os
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from telegram.error import TelegramError
from telegram.ext import ApplicationHandlerStop

load_dotenv()
print("Loaded TELEGRAM_API_KEY:", os.getenv("TELEGRAM_API_KEY"))

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
groq_api_key = os.getenv("GROQ_API_KEY")

def setup_llm_chain(topic="technology"):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "you are a joking AI. Give me only one funny joke on a given topic."),
        ("user", f"generate a joke on topic: {topic}")
    ])
    llm = ChatGroq(
        model="Gemma2-9b-It",
        groq_api_key=groq_api_key
    )
    return prompt | llm | StrOutputParser()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Mention me with a topic like '@Unique_joke_Bot python' to get a joke.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Mention me with a topic like '@Unique_joke_Bot python' to get a joke.")

async def genearte_joke(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
    await update.message.reply_text(f"Generating joke about {topic}...")
    joke = setup_llm_chain(topic).invoke({}).strip()
    await update.message.reply_text(joke)
    
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Exception while handling an update: {context.error}")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return  # Ignore non-text or empty updates

    msg = update.message.text
    bot_username = context.bot.username

    if f'@{bot_username}' in msg:
        match = re.search(f'@{bot_username}\\s+(.*)', msg)
        if match and match.group(1).strip():
            await genearte_joke(update, context, match.group(1).strip())
        else:
            await update.message.reply_text("Please specify a topic after mentioning me.")


def main():
    token = "8099220237:AAHlYFOsyvCc_pq0ouON22WqVCaFd6yA2lo"
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    # Register error handler
    app.add_error_handler(error_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

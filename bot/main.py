from __future__ import annotations

import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .config import load_settings
from .handlers import BotContext, build_router, help_message, start_message
from .intents import build_default_intent_engine


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    app_ctx: BotContext = context.application.bot_data["ctx"]
    await update.message.reply_text(start_message(app_ctx))


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    app_ctx: BotContext = context.application.bot_data["ctx"]
    await update.message.reply_text(help_message(app_ctx))


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    app_ctx: BotContext = context.application.bot_data["ctx"]
    router = context.application.bot_data["router"]
    response = router(update, context)
    await update.message.reply_text(response)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled exception while processing update", exc_info=context.error)


def main() -> None:
    load_dotenv()

    settings = load_settings()
    intent_engine = build_default_intent_engine()
    app_ctx = BotContext(settings=settings, intent_engine=intent_engine)

    application = Application.builder().token(settings.bot_token).build()
    application.bot_data["ctx"] = app_ctx
    application.bot_data["router"] = build_router(app_ctx)

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    application.add_error_handler(error_handler)

    logger.info("Bot started and polling updates...")
    application.run_polling()


if __name__ == "__main__":
    main()

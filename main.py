import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
from os import getenv
from currency_rate_advisor import CurrencyRateAdvisor

class TelegramBot:
    def __init__(self, telegram_bot_API_token: str, openexchange_app_id: str) -> None:
        self.telegram_token = telegram_bot_API_token
        self.currency_rate_advisor = CurrencyRateAdvisor(openexchange_app_id=openexchange_app_id)


    def start(self) -> None:
        application = ApplicationBuilder().token(self.telegram_token).build()
        
        start_handler = CommandHandler('start', self.handle_start)
        application.add_handler(start_handler)
        
        show_rate_handler = CommandHandler('show_rate', self.handle_show_rate)
        application.add_handler(show_rate_handler)

        application.run_polling()    


    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


    async def handle_show_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        [base, target] = context.args
        rate = self.currency_rate_advisor.get_currency_rates(base, target)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{base}:{target} rate is {rate}")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    load_dotenv()
    bot = TelegramBot(telegram_bot_API_token=getenv("telegram_bot_API_token"),
                        openexchange_app_id=getenv("openexchange_app_id"))
    bot.start()

from aiogram.utils import executor
from bot.bot_init import add_handlers, dispatcher, startup, shutdown
from utils.load_local_variables import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT

# Entry point
if __name__ == '__main__':
    add_handlers()
    executor.start_webhook(
        dispatcher=dispatcher,
        webhook_path=WEBHOOK_PATH,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        on_startup=startup,
        on_shutdown=shutdown,
        skip_updates=True,
    )

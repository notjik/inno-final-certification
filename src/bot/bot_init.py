from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command, CommandStart, CommandHelp
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import db_session
from utils.load_local_variables import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH, DB_PATH
from utils.loggers import logger_status, logger_database_engine


# initializing the bot
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot, storage=storage)


async def startup(callback):
    """
    Logging the launch of the bot

    :param callback: dispatcher object
    :return: None
    """
    db_session.global_init(DB_PATH)
    await bot.set_webhook(WEBHOOK_HOST + WEBHOOK_PATH)
    me = await callback.bot.get_me()
    extra = {
        'bot': me.username,
        'bot_id': me.id,
    }
    logger_status.info('has been successfully launched.', extra=extra)


async def shutdown(callback):
    """
    Logging off the bot

    :param callback: dispatcher object
    :return: None
    """
    logger_database_engine.info('Closing the connection due to program shutdown.')
    await bot.delete_webhook()
    me = await callback.bot.get_me()
    extra = {
        'bot': me.username,
        'bot_id': me.id,
    }
    logger_status.info('is disabled.', extra=extra)


def add_handlers():
    from bot.handlers import start_message, help_message, library, store, passing, transfer, \
        receiving_location, pickup, delivery, process_pre_checkout_query, process_pay, push_close
    from bot.callbacks import cb_store, cb_buy
    from bot.states import FSMBuy
    dispatcher.register_message_handler(start_message, CommandStart())
    dispatcher.register_message_handler(help_message, CommandHelp())
    dispatcher.register_callback_query_handler(library, text='my_games')
    dispatcher.register_callback_query_handler(store, cb_store.filter())
    dispatcher.register_callback_query_handler(transfer, cb_buy.filter(), state=None)
    dispatcher.register_message_handler(receiving_location, content_types=['location'], state=FSMBuy.game_id)
    dispatcher.register_callback_query_handler(pickup, text='pickup', state=FSMBuy.delivery)
    dispatcher.register_callback_query_handler(delivery, text='courier', state=FSMBuy.delivery)
    dispatcher.register_pre_checkout_query_handler(process_pre_checkout_query)
    dispatcher.register_message_handler(process_pay, content_types=types.ContentType.SUCCESSFUL_PAYMENT)
    dispatcher.register_callback_query_handler(passing, text='pass')
    dispatcher.register_callback_query_handler(push_close, text='close')

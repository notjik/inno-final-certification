from aiogram import types
from aiogram.dispatcher import FSMContext
from database import db_session, users, games, usersgames, genres
from bot.keyboards import get_menu, get_store_menu, get_pay, get_close, get_chose_delivery
from bot.menu import set_starting_commands
from bot.bot_init import bot
from bot.states import FSMBuy
from utils.load_local_variables import BANK_TOKEN
from utils.loggers import logger_message


async def start_message(message: types.Message):
    await set_starting_commands(bot, message.chat.id)
    db_sess = db_session.create_session()
    q = db_sess.query(users.Users).filter_by(user_id=message.from_user.id)
    if not q.all():
        user = users.Users(user_id=message.from_user.id)
        db_sess.add(user)
        db_sess.commit()
    await message.answer('Welcome, <b>{}</b>!'.format(message.from_user.username),
                         reply_markup=get_menu())
    await message.delete()
    extra = {
        'user': message.from_user.username,
        'user_id': message.from_user.id,
        'content_type': '/start'
    }
    logger_message.info(message, extra=extra)


async def help_message(message: types.Message):
    await message.answer('This is a bot for buying games by genre.')
    extra = {
        'user': message.from_user.username,
        'user_id': message.from_user.id,
        'content_type': '/help'
    }
    logger_message.info(message, extra=extra)


async def library(callback: types.CallbackQuery):
    await callback.answer()
    db_sess = db_session.create_session()
    games_in_account = [(db_sess.query(games.Games).filter_by(id=i.game_id).first(), i.is_delivered)
                        for i in db_sess.query(usersgames.UsersGames).filter_by(
            user_id=db_sess.query(users.Users).filter_by(user_id=callback.from_user.id).first().id).all()]
    if games_in_account:
        await bot.edit_message_text(
            text='<b>{} games</b>\n\n'.format(callback.from_user.username) +
                 '\n'.join('<b>{}</b> <ins>[{}]</ins>: <em>{}</em>'.format(i[0].title,
                                                                           'delivered' if i[1]
                                                                           else 'not delivered',
                                                                           i[0].genres.title)
                           for i in games_in_account),
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=get_menu(my_games=False))
    else:
        await bot.edit_message_text(
            text='<b>There are no purchased games on the {} account😞</b>\n\n'.format(callback.from_user.username),
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=get_menu(my_games=False))
    extra = {
        'user': callback.from_user.username,
        'user_id': callback.from_user.id,
        'content_type': 'view library'
    }
    logger_message.info(callback.message, extra=extra)


async def store(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    genre_id = int(callback_data['genre_id'])
    db_sess = db_session.create_session()
    genre_name = db_sess.query(genres.Genres).filter_by(id=genre_id).first().title if genre_id != -1 else 'All'
    q = db_sess.query(games.Games)
    if genre_id != -1:
        q = q.filter_by(genre_id=genre_id)
    all_games = q.all()
    page = int(callback_data['page'])
    max_page = len(all_games)
    if page <= max_page:
        this_game = all_games[page - 1]
        await bot.edit_message_text(message_id=callback.message.message_id,
                                    chat_id=callback.message.chat.id,
                                    text='<b>Genre:</b> {}\n'
                                         '<b>Page:</b> {}\n\n'
                                         '<b>{}</b>\n'
                                         '{}\n'
                                         '<b>Price:</b> {} RUB'.format(
                                        genre_name,
                                        page,
                                        this_game.title,
                                        '<em>{}</em>\n'.format(
                                            this_game.description) if this_game.description else '',
                                        this_game.price),
                                    reply_markup=get_store_menu(callback.from_user.id,
                                                                genre_id,
                                                                page,
                                                                max_page,
                                                                this_game.id))
    else:
        await bot.edit_message_text(message_id=callback.message.message_id,
                                    chat_id=callback.message.chat.id,
                                    text='This page not found 👀',
                                    reply_markup=get_store_menu(callback.from_user.id,
                                                                genre_id,
                                                                page,
                                                                max_page,
                                                                -1))
    extra = {
        'user': callback.from_user.username,
        'user_id': callback.from_user.id,
        'content_type': 'load store'
    }
    logger_message.info(callback.message, extra=extra)


async def passing(callback: types.CallbackQuery):
    await callback.answer()


async def transfer(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await bot.edit_message_text(
        text='Send your geolocation to place an order',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=get_close())
    async with state.proxy() as data:
        data['game_id'] = int(callback_data['game_id'])
        data['message_id'] = callback.message.message_id
    await FSMBuy.game_id.set()
    extra = {
        'user': callback.from_user.username,
        'user_id': callback.from_user.id,
        'content_type': 'can buying'
    }
    logger_message.info(callback.message, extra=extra)


async def receiving_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lat'] = message.location.latitude
        data['lon'] = message.location.longitude
        await bot.edit_message_text(text='Choose a delivery option',
                                    chat_id=message.chat.id,
                                    message_id=data['message_id'],
                                    reply_markup=get_chose_delivery(message.location.latitude,
                                                                    message.location.longitude))
    await message.delete()
    await FSMBuy.next()
    extra = {
        'user': message.from_user.username,
        'user_id': message.from_user.id,
        'content_type': 'send location'
    }
    logger_message.info(message, extra=extra)


async def pickup(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    db_sess = db_session.create_session()
    async with state.proxy() as data:
        game = db_sess.query(games.Games).filter_by(id=data['game_id']).first()
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await bot.send_invoice(chat_id=callback.message.chat.id,
                           title=game.title,
                           description='Purchase of {}. Pickup.'.format(game.title),
                           payload=game.id,
                           provider_token=BANK_TOKEN,
                           currency='RUB',
                           start_parameter='pay',
                           prices=[{'label': 'Game', 'amount': int(game.price * 100)},
                                   {'label': 'Pickup', 'amount': 0}],
                           reply_markup=get_pay())
    await state.finish()
    extra = {
        'user': callback.from_user.username,
        'user_id': callback.from_user.id,
        'content_type': 'start payment'
    }
    logger_message.info(callback.message, extra=extra)


async def delivery(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    db_sess = db_session.create_session()
    async with state.proxy() as data:
        game = db_sess.query(games.Games).filter_by(id=data['game_id']).first()
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await bot.send_invoice(chat_id=callback.message.chat.id,
                           title=game.title,
                           description='Purchase of {}. Delivery.'.format(game.title),
                           payload=game.id,
                           provider_token=BANK_TOKEN,
                           currency='RUB',
                           start_parameter='pay',
                           prices=[{'label': 'Game', 'amount': int(game.price * 100)},
                                   {'label': 'Delivery', 'amount': 25000 + int(game.price)}],
                           reply_markup=get_pay())
    await state.finish()
    extra = {
        'user': callback.from_user.username,
        'user_id': callback.from_user.id,
        'content_type': 'start payment'
    }
    logger_message.info(callback.message, extra=extra)


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    db_sess = db_session.create_session()
    q = db_sess.query(usersgames.UsersGames).filter_by(user_id=pre_checkout_query.from_user.id,
                                                       game_id=pre_checkout_query.invoice_payload).all()
    if not q:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False,
                                            error_message='You already have this game in your library')
    extra = {
        'user': pre_checkout_query.from_user.username,
        'user_id': pre_checkout_query.from_user.id,
        'content_type': 'passed the pre checkout query'
    }
    logger_message.info(pre_checkout_query, extra=extra)


async def process_pay(message: types.Message):
    db_sess = db_session.create_session()
    account = db_sess.query(users.Users).filter_by(user_id=message.from_user.id).first()
    game = db_sess.query(games.Games).filter_by(id=message.successful_payment.invoice_payload).first()
    account.games.append(game)
    db_sess.add(account)
    db_sess.commit()
    await message.delete()
    await bot.send_message(message.from_user.id, 'Thank you for buying {} ❤️'.format(game.title),
                           reply_markup=get_menu())
    extra = {
        'user': message.from_user.username,
        'user_id': message.from_user.id,
        'content_type': 'purchase game ({})'.format(game.title)
    }
    logger_message.info(message, extra=extra)


async def push_close(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    extra = {
        'user': callback.from_user.username,
        'user_id': callback.from_user.id,
        'content_type': 'close purchase'
    }
    logger_message.info(callback.message, extra=extra)
